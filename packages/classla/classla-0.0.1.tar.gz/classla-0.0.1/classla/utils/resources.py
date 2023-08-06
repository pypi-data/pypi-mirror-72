"""
utilities for getting resources
"""

import os
import requests
import zipfile

from tqdm import tqdm
from pathlib import Path

# set home dir for default
HOME_DIR = str(Path.home())
DEFAULT_MODEL_DIR = os.path.join(HOME_DIR, 'classla_resources')
DEFAULT_MODELS_URL = 'https://www.clarin.si/repository/xmlui/bitstream/handle'
# DEFAULT_DOWNLOAD_VERSION = 'latest'

# list of language shorthands
conll_shorthands = ['sl_ssj', 'hr_hr500k', 'sr_set', 'bg_btb']

# all languages with mwt
mwt_languages = []

# default treebank for languages
default_treebanks = {'sl': 'sl_ssj', 'hr': 'hr_hr500k', 'sr': 'sr_set', 'bg': 'bg_btb'}

# map processor name to file ending
processor_to_ending = {'tokenize': 'tokenizer', 'mwt': 'mwt_expander', 'pos': 'tagger', 'lemma': 'lemmatizer',
                       'depparse': 'parser', 'ner': 'ner'}

model_links = {
    'sl_ssj': {
        '_tagger': '11356/1312/ssj500k',
        '_lemmatizer': '11356/1286/ssj500k+Sloleks_lemmatizer.pt',
        '_parser': '11356/1258/ssj500k_ud',
        '_ner': '11356/1321/ssj500k',
        '.pretrain': '11356/1312/ssj500k.pretrain.pt'
    },
    'hr_hr500k': {
        '_tagger': '11356/1252/hr500k',
        '_lemmatizer': '11356/1287/hr500k+hrLex_lemmatizer.pt',
        '_parser': '11356/1259/hr500k_ud',
        '_ner': '11356/1322/hr500k',
        '.pretrain': '11356/1252/hr500k.pretrain.pt'
    },
    'sr_set': {
        '_tagger': '11356/1253/SETimes.SR',
        '_lemmatizer': '11356/1288/SETimes.SR+srLex_lemmatizer.pt',
        '_parser': '11356/1260/SETimes.SR_ud',
        '_ner': '11356/1323/SETimes.SR',
        '.pretrain': '11356/1253/SETimes.SR.pretrain.pt'
    },
    'bg_btb': {
        '_tagger': '11356/1326/BTB',
        '_lemmatizer': '11356/1327/BTB_lemmatizer.pt',
        '_parser': '11356/1328/BTB_ud',
        '.pretrain': '11356/1326/BTB.pretrain.pt'
    }
}

# functions for handling configs


# given a language and models path, build a default configuration
def build_default_config(treebank, models_path):
    default_config = {}
    if treebank in mwt_languages:
        default_config['processors'] = 'tokenize,mwt,pos,lemma,depparse'
    else:
        default_config['processors'] = 'tokenize,ner,pos,lemma,depparse'
    if treebank == 'vi_vtb':
        default_config['lemma_use_identity'] = True
        default_config['lemma_batch_size'] = 5000
    treebank_dir = os.path.join(models_path, f"{treebank}_models")
    for processor in default_config['processors'].split(','):
        model_file_ending = f"{processor_to_ending[processor]}.pt"
        default_config[f"{processor}_model_path"] = os.path.join(treebank_dir, f"{treebank}_{model_file_ending}")
        if processor in ['pos', 'depparse']:
            default_config[f"{processor}_pretrain_path"] = os.path.join(treebank_dir, f"{treebank}.pretrain.pt")
        if processor in ['ner']:
            default_config[f"{processor}_pretrain_path"] = os.path.join(treebank_dir, f"{treebank}.pretrain.pt")
            default_config[f"{processor}_forward_charlm_path"] = None
            default_config[f"{processor}_backward_charlm_path"] = None
    return default_config


# load a config from file
def load_config(config_file_path):
    loaded_config = {}
    with open(config_file_path) as config_file:
        for config_line in config_file:
            config_key, config_value = config_line.split(':')
            loaded_config[config_key] = config_value.rstrip().lstrip()
    return loaded_config

# download a part of ud model (i.e. ner part, pos part)
def download_ud_model_part(download_file_path, download_url):
    print('Download location: ' + download_file_path)

    # initiate download
    r = requests.get(download_url, stream=True)
    with open(download_file_path, 'wb') as f:
        file_size = int(r.headers.get('content-length'))
        default_chunk_size = 67108864
        with tqdm(total=file_size, unit='B', unit_scale=True) as pbar:
            for chunk in r.iter_content(chunk_size=default_chunk_size):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    pbar.update(len(chunk))

# download a ud models zip file
def download_ud_model(lang_name, resource_dir=None, should_unzip=True, confirm_if_exists=False, force=False):
    # ask if user wants to download
    if resource_dir is not None and os.path.exists(os.path.join(resource_dir, f"{lang_name}_models")):
        if confirm_if_exists:
            print("")
            print(f"The model directory already exists at \"{resource_dir}/{lang_name}_models\". Do you want to download the models again? [y/N]")
            should_download = 'y' if force else input()
            should_download = should_download.strip().lower() in ['yes', 'y']
        else:
            should_download = False
    else:
        print('Would you like to download the models for: '+lang_name+' now? (Y/n)')
        should_download = 'y' if force else input()
        should_download = should_download.strip().lower() in ['yes', 'y', '']
    if should_download:
        # set up data directory
        if resource_dir is None:
            print('')
            print('Default download directory: ' + DEFAULT_MODEL_DIR)
            print('Hit enter to continue or type an alternate directory.')
            where_to_download = '' if force else input()
            if where_to_download != '':
                download_dir = where_to_download
            else:
                download_dir = DEFAULT_MODEL_DIR
        else:
            download_dir = resource_dir
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        lang_dir = os.path.join(download_dir, lang_name + '_models')
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)

        print('')
        print('Downloading models for: '+lang_name)
        for model_part_type, download_url_part in model_links[lang_name].items():
            model_part_file_name = f'{lang_name}{model_part_type}.pt'
            download_url = f'{DEFAULT_MODELS_URL}/{download_url_part}'
            download_file_path = os.path.join(lang_dir, model_part_file_name)
            download_ud_model_part(download_file_path, download_url)

        # unzip models file
        print('')
        print('Download complete.  Models saved to: '+lang_dir)


# unzip a ud models zip file
def unzip_ud_model(lang_name, zip_file_src, zip_file_target):
    print('Extracting models file for: '+lang_name)
    with zipfile.ZipFile(zip_file_src, "r") as zip_ref:
        zip_ref.extractall(zip_file_target)


# main download function
def download(download_label, resource_dir=None, confirm_if_exists=False, force=False):
    if download_label in conll_shorthands:
        download_ud_model(download_label, resource_dir=resource_dir, confirm_if_exists=confirm_if_exists, force=force)
    elif download_label in default_treebanks:
        print(f'Using the default treebank "{default_treebanks[download_label]}" for language "{download_label}".')
        download_ud_model(default_treebanks[download_label], resource_dir=resource_dir,
                          confirm_if_exists=confirm_if_exists, force=force)
    else:
        raise ValueError(f'The language or treebank "{download_label}" is not currently supported by this function. Please try again with other languages or treebanks.')
