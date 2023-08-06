# StanfordNLP: A Python NLP Library for Many Human Languages
## A [CLASSLA](http://www.clarin.si/info/k-centre/) Fork For Processing South Slavic Languages 

This is a fork of the [Stanford NLP Group's official Python NLP library](https://github.com/stanfordnlp/stanfordnlp). The main changes to the official library are
- possibility of training the tagger and lemmatiser on datasets which are not UD-parsed
- using an external dictionary while performing lemmatization
- looking up (word, upos, feats) triples in dictionaries during lemmatization, fallbacking to (word, upos)
- speeding up the seq2seq lemmatization training procedure by training only on instances occurring less than 5 times in the training data
- speeding up the lemmatization by seq2seqing only forms not seen in the lookup lexicon (implemented in stanfordnlp only in the pipeline)
- encoding POS information at the beginning of the sequence, improving significantly seq2seq lemmatization results

## Benchmarking results

This pipeline currently (January 2020) is the state-of-the-art in processing Slovenian, Croatian and Serbian, with the following (CoNLL-2018-shared-task) F1 metrics obtained on the [babushka-bench](https://github.com/clarinsi/babushka-bench) benchmarking platform (with gold segmentation and remaining preprocessing with the same pipeline):

|language|layer|F1|
|---|---|---|
|Slovenian|morphosyntax (XPOS)|96.72|
|Slovenian|lemmatization (LEMMA)|99.02|
|Slovenian|dependency parsing (LAS)|92.68|
|Croatian|morphosyntax (XPOS)|94.13|
|Croatian|lemmatization (LEMMA)|97.60|
|Croatian|dependency parsing (LAS)|85.86|
|Serbian|morphosyntax (XPOS)|95.23|
|Serbian|lemmatization (LEMMA)|97.89|
|Serbian|dependency parsing (LAS)|88.96|

## Installation
### pip
We recommend that you install Classla via pip, the Python package manager. To install, run:
```
pip install classla
```
This will also help to resolve all dependencies.

## Running the tool
### Getting started
To run your first Classla pipeline, follow these steps:
```
import classla
classla.download('sl')                            # to download models in Slovene
nlp = classla.Pipeline('sl')                      # to initialize default Slovene pipeline
doc = nlp("Janez Janša je rojen v Grosuplju.")    # to run pipeline
print(doc.conll_file.conll_as_string())           # to print output in conllu format
```

You can also look into ```pipeline_simple.py``` and ```pipeline_use.py``` files for usage examples.

### Tokenization

For tokenization of Slovenian, Croatian or Serbian, a rule-based tokenizer, [reldi-tokeniser](https://github.com/clarinsi/reldi-tokeniser) should be applied prior to further processing, producing CoNLL-U output.

For tokenization of Slovenian, compliant with standard training data and reference corpora, [Obeliks4J](https://github.com/clarinsi/Obeliks4J) should be used, again, by generating CoNLL-U output.

### Part-of-speech tagging

For now, there are available pre-trained models for part-of-speech tagging for 
- standard Slovenian http://hdl.handle.net/11356/1312 
- standard Croatian http://hdl.handle.net/11356/1252 
- standard Serbian http://hdl.handle.net/11356/1253
- standard Bulgarian http://hdl.handle.net/11356/1326

Once you placed the PoS-tagging model files into the ```models/pos/``` path, you can run the following commands (for (1) Slovenian, (2) Croatian, or (3) Serbian)

```
python -m classla.models.tagger --save_dir models/pos/ --save_name ssj500k --eval_file data/ssj500k.dev.conllu --output_file temp --gold_file data/ssj500k.dev.conllu --shorthand sl_ssj --mode predict
python -m classla.models.tagger --save_dir models/pos/ --save_name hr500k --eval_file data/hr500k.dev.conllu --output_file temp --gold_file data/hr500k.dev.conllu --shorthand hr_set --mode predict
python -m classla.models.tagger --save_dir models/pos/ --save_name SETimes.SR --eval_file data/SETimes.SR.dev.conllu --output_file temp --gold_file data/SETimes.SR.dev.conllu --shorthand sr_set --mode predict
```

If you do not want to evaluate the tagger, but just annotate a new file, you can leave out the ```--gold_file``` argument.

The input to part-of-speech tagging is a CONLLU-formated file.

### Lemmatisation

Similarly to PoS tagging, there are pre-trained models for lemmatisation available as well for
- standard Slovenian http://hdl.handle.net/11356/1286
- standard Croatian http://hdl.handle.net/11356/1287
- standard Serbian http://hdl.handle.net/11356/1288
- standard Bulgarian http://hdl.handle.net/11356/1327

Running the lemmatiser for Slovenian, if models are placed in the ```models/lemma/``` directory, can be performed as follows:
```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file ssj500k+Sloleks --eval_file data/pos.ssj500k.dev.conllu --output_file temp --gold_file data/pos.ssj500k.dev.conllu --mode predict
```

Similarly, for Croatian or Serbian, these are the corresponding commands:

```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file hr500k+hrLex --eval_file data/pos.hr500k.dev.conllu --output_file temp --gold_file data/pos.hr500k.dev.conllu --mode predict
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file SETimes.SR+srLex --eval_file data/pos.SETimes.SR.dev.conllu --output_file temp --gold_file data/pos.SETimes.SR.dev.conllu --mode predict
```

Again, leaving out the ```-gold_file``` argument, no evaluation will be performed.

The input to lemmatisation is a CONLLU-formated file which was previously part-of-speech tagged.

### Parsing

For UD depency parsing, the pre-trained models are also available for
- standard Slovenian http://hdl.handle.net/11356/1258
- standard Croatian http://hdl.handle.net/11356/1259
- standard Serbian http://hdl.handle.net/11356/1260
- standard Bulgarian http://hdl.handle.net/11356/1328

Parsing Slovenian data, once models are placed in the ```models/depparse/``` directory, can be performed as follows:

```
python -m classla.models.parser --save_dir models/depparse/ --save_name ssj500k_ud --eval_file data/pos.lemma.ssj500k_ud.dev.conllu --gold_file data/pos.lemma.ssj500k_ud.dev.conllu --shorthand sl_ssj --output_file temp --mode predict
```
Similarly, for Croatian or Serbian, these are the corresponding commands:

```
python -m classla.models.parser --save_dir models/depparse/ --save_name hr500k_ud --eval_file data/pos.lemma.hr500k_ud.dev.conllu --gold_file data/pos.lemma.hr500k_ud.dev.conllu --shorthand hr_set --output_file temp --mode predict
python -m classla.models.parser --save_dir models/depparse/ --save_name SETimes.SR_ud --eval_file data/pos.lemma.SETimes.SR_ud.dev.conllu --gold_file data/pos.lemma.SETimes.SR_ud.dev.conllu --shorthand sr_set --output_file temp --mode predict
```

Again, leaving out the ```-gold_file``` argument, no evaluation will be performed.

The input to lemmatisation is a CONLLU-formated file which was previously part-of-speech tagged and lemmatised.

### NER

```
python -m classla.models.ner_tagger --save_dir models/ner/ --save_name ssj500k --eval_file data/ssj500k.test.json --mode predict --output_file out.ner.sl
python -m classla.models.ner_tagger --save_dir models/ner/ --save_name hr500k --eval_file data/hr500k.test.json --mode predict --output_file out.ner.hr
```

## Training your own models

### Part-of-speech tagging

Below are examples for training models for standard Slovene, Croatian and Serbian, assuming (1) CLARIN.SI embeddings and (2) corresponding training datasets (ssj500k, hr500k, SETimes.SR) are in the specified locations. Training is performed on train+test data, while dev is used for evaluation.

```
python -m classla.models.tagger --save_dir models/pos/ --save_name ssj500k --wordvec_file ~/data/clarin.si-embed/embed.sl-token.ft.sg.vec.xz --train_file ../babushka-bench/datasets/sl/ssj500k/train+test.conllu --eval_file ../babushka-bench/datasets/sl/ssj500k/dev.conllu --gold_file ../babushka-bench/datasets/sl/ssj500k/dev.conllu --mode train --shorthand sl_ssj --output_file temp.sl
python -m classla.models.tagger --save_dir models/pos/ --save_name hr500k --wordvec_file ~/data/clarin.si-embed/embed.hr-token.ft.sg.vec.xz --train_file ../babushka-bench/datasets/hr/hr500k/train+test.conllu --eval_file ../babushka-bench/datasets/hr/hr500k/dev.conllu --gold_file ../babushka-bench/datasets/hr/hr500k/dev.conllu --mode train --shorthand hr_set --output_file temp.hr
python -m classla.models.tagger --save_dir models/pos/ --save_name SETimes.SR --wordvec_file ~/data/clarin.si-embed/embed.sr-token.ft.sg.vec.xz --train_file ../babushka-bench/datasets/sr/SETimes.SR/train+test.conllu --eval_file ../babushka-bench/datasets/sr/SETimes.SR/dev.conllu --gold_file ../babushka-bench/datasets/sr/SETimes.SR/dev.conllu --mode train --shorthand sr_set --output_file temp.sr
```

### Lemmatization

Given that the lemmatization process relies on XPOS, to make the training data as realistic as possible, we train the lemmatization process on automatically part-of-speech-tagged data. We also use external lexicons for lemmatization (Sloleks, hrLex and srLex).

The pre-tagging is performed as defined in the section of running part-of-speech tagging. The commands for training the lemmatizers are given below.

```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file ssj500k+Sloleks --train_file pretagged/pos.ssj500k.train+test.conllu --eval_file pretagged/pos.ssj500k.dev.conllu --output_file temp.lemma.sl --gold_file pretagged/pos.ssj500k.dev.conllu --external_dict ~/data/morphlex/Sloleks --mode train --num_epoch 30 --decay_epoch 20 --pos
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file hr500k+hrLex --train_file pretagged/pos.hr500k.train+test.conllu --eval_file pretagged/pos.hr500k.dev.conllu --output_file temp.lemma.hr --gold_file pretagged/pos.hr500k.dev.conllu --external_dict ~/data/morphlex/hrLex --mode train --num_epoch 30 --decay_epoch 20 --pos
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file SETimes.SR+srLex --train_file pretagged/pos.SETimes.SR.train+test.conllu --eval_file pretagged/pos.SETimes.SR.dev.conllu --output_file temp.lemma.sr --gold_file pretagged/pos.SETimes.SR.dev.conllu --external_dict ~/data/morphlex/srLex --mode train --num_epoch 30 --decay_epoch 20 --pos
```

### Parsing

Preparing the data to be automatically pretagged on morphosyntactic and lemma level:

```
# Slovene tagging
python -m classla.models.tagger --save_dir models/pos/ --save_name ssj500k --eval_file ../babushka-bench/datasets/sl/ssj500k/dev_ud.conllu --output_file pretagged/pos.ssj500k_ud.dev.conllu --gold_file ../babushka-bench/datasets/sl/ssj500k/dev_ud.conllu --shorthand sl_ssj --mode predict
cat ../babushka-bench/datasets/sl/ssj500k/train_ud.conllu ../babushka-bench/datasets/sl/ssj500k/test_ud.conllu > pretagged/ssj500k_ud.train+test.conllu
python -m classla.models.tagger --save_dir models/pos/ --save_name ssj500k --eval_file pretagged/ssj500k_ud.train+test.conllu --output_file pretagged/pos.ssj500k_ud.train+test.conllu --gold_file pretagged/ssj500k_ud.train+test.conllu --shorthand sl_ssj --mode predict
# Croatian tagging
python -m classla.models.tagger --save_dir models/pos/ --save_name hr500k --eval_file ../babushka-bench/datasets/hr/hr500k/dev_ud.conllu --output_file pretagged/pos.hr500k_ud.dev.conllu --gold_file ../babushka-bench/datasets/hr/hr500k/dev_ud.conllu --shorthand hr_set --mode predict
cat ../babushka-bench/datasets/hr/hr500k/train_ud.conllu ../babushka-bench/datasets/hr/hr500k/test_ud.conllu > pretagged/hr500k_ud.train+test.conllu
python -m classla.models.tagger --save_dir models/pos/ --save_name hr500k --eval_file pretagged/hr500k_ud.train+test.conllu --output_file pretagged/pos.hr500k_ud.train+test.conllu --gold_file pretagged/hr500k_ud.train+test.conllu --shorthand hr_set --mode predict
# Serbian tagging
python -m classla.models.tagger --save_dir models/pos/ --save_name SETimes.SR --eval_file ../babushka-bench/datasets/sr/SETimes.SR/dev_ud.conllu --output_file pretagged/pos.SETimes.SR_ud.dev.conllu --gold_file ../babushka-bench/datasets/sr/SETimes.SR/dev_ud.conllu --shorthand sr_set --mode predict
cat ../babushka-bench/datasets/sr/SETimes.SR/train_ud.conllu ../babushka-bench/datasets/sr/SETimes.SR/test_ud.conllu > pretagged/SETimes.SR_ud.train+test.conllu
(pytorch) nikolal@kt-gpu-vm-1TB:~/tools/classla-stanfordnlp$ python -m classla.models.tagger --save_dir models/pos/ --save_name SETimes.SR --eval_file pretagged/SETimes.SR_ud.train+test.conllu --output_file pretagged/pos.SETimes.SR_ud.train+test.conllu --gold_file pretagged/SETimes.SR_ud.train+test.conllu --shorthand sr_set --mode predict
# Slovene lemmatization
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file ssj500k+Sloleks --eval_file pretagged/pos.ssj500k_ud.dev.conllu --output_file pretagged/pos.lemma.ssj500k_ud.dev.conllu --gold_file pretagged/pos.ssj500k_ud.dev.conllu --mode predict
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file ssj500k+Sloleks --eval_file pretagged/pos.ssj500k_ud.train+test.conllu --output_file pretagged/pos.lemma.ssj500k_ud.train+test.conllu --gold_file pretagged/pos.ssj500k_ud.train+test.conllu --mode predict
# Croatian lemmatization
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file hr500k+hrLex --eval_file pretagged/pos.hr500k_ud.dev.conllu --output_file pretagged/pos.lemma.hr500k_ud.dev.conllu --gold_file pretagged/pos.hr500k_ud.dev.conllu --mode predict
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file hr500k+hrLex --eval_file pretagged/pos.hr500k_ud.train+test.conllu --output_file pretagged/pos.lemma.hr500k_ud.train+test.conllu --gold_file pretagged/pos.hr500k_ud.train+test.conllu --mode predict
# Serbian lemmatization
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file SETimes.SR+srLex --eval_file pretagged/pos.SETimes.SR_ud.dev.conllu --output_file pretagged/pos.lemma.SETimes.SR_ud.dev.conllu --gold_file pretagged/pos.SETimes.SR_ud.dev.conllu --mode predict
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file SETimes.SR+srLex --eval_file pretagged/pos.SETimes.SR_ud.train+test.conllu --output_file pretagged/pos.lemma.SETimes.SR_ud.train+test.conllu --gold_file pretagged/pos.SETimes.SR_ud.train+test.conllu --mode predict
```

Once you have all the training data preprocessed, you can train the parsers in the following manner:

```
python -m classla.models.parser --save_dir models/depparse/ --save_name ssj500k_ud --wordvec_file ~/data/clarin.si-embed/embed.sl-token.ft.sg.vec.xz --train_file pretagged/pos.lemma.ssj500k_ud.train+test.conllu --eval_file pretagged/pos.lemma.ssj500k_ud.dev.conllu --gold_file pretagged/pos.lemma.ssj500k_ud.dev.conllu --shorthand sl_ssj --output_file temp.depparse.sl --mode train
python -m classla.models.parser --save_dir models/depparse/ --save_name hr500k_ud --wordvec_file ~/data/clarin.si-embed/embed.hr-token.ft.sg.vec.xz --train_file pretagged/pos.lemma.hr500k_ud.train+test.conllu --eval_file pretagged/pos.lemma.hr500k_ud.dev.conllu --gold_file pretagged/pos.lemma.hr500k_ud.dev.conllu --shorthand hr_set --output_file temp.depparse.hr --mode train
python -m classla.models.parser --save_dir models/depparse/ --save_name SETimes.SR_ud --wordvec_file ~/data/clarin.si-embed/embed.sr-token.ft.sg.vec.xz --train_file pretagged/pos.lemma.SETimes.SR_ud.train+test.conllu --eval_file pretagged/pos.lemma.SETimes.SR_ud.dev.conllu --gold_file pretagged/pos.lemma.SETimes.SR_ud.dev.conllu --shorthand sr_set --output_file temp.depparse.sr --mode train
```

### NER

``` 
python -m classla.models.ner_tagger --wordvec_file ~/data/clarin.si-embed/embed.sl-token.ft.sg.vec.xz --train_file data/ssj500k.train+test.json --eval_file data/ssj500k.dev.json --lang sl --shorthand sl_ssj --mode train --save_dir models/ner/ --save_name ssj500k --scheme bio --batch_size 128
python -m classla.models.ner_tagger --wordvec_file ~/data/clarin.si-embed/embed.hr-token.ft.sg.vec.xz --train_file data/hr500k.train+test.json --eval_file data/hr500k.dev.json --lang hr --shorthand hr_set --mode train --save_dir models/ner/ --save_name hr500k --scheme bio --batch_size 128
python -m classla.models.ner_tagger --wordvec_file ~/data/clarin.si-embed/embed.sr-token.ft.sg.vec.xz --train_file data/SETimes.SR.train+test.json --eval_file data/SETimes.SR.dev.json --lang sr --shorthand sr_set --mode train --save_dir models/ner/ --save_name SETimes.SR --scheme bio --batch_size 128
```

## English training


### Tokenization
```
python classla/utils/prepare_tokenizer_data.py ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train+test.txt ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train+test.conllu -o ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train+test.toklabels -m ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train+test-mwt.json
python classla/utils/prepare_tokenizer_data.py ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train.txt ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train.conllu -o ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train.toklabels -m ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train-mwt.json
python classla/utils/prepare_tokenizer_data.py ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-dev.txt ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-dev.conllu -o ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-dev.toklabels -m ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-dev-mwt.json

python -m classla.models.tokenizer --label_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train+test.toklabels --txt_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train+test.txt --conll_file temp.tokenize.en --dev_label_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-dev.toklabels --dev_txt_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-dev.txt --dev_conll_gold ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-dev.conllu --lang en --save_dir models/tokenize --save_name ewt --mwt_json_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train+test-mwt.json --max_seqlen 300
python -m classla.models.tokenizer --mode predict --txt_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-dev.txt --save_dir models/tokenize/ --save_name ewt --conll_file temp
```

### Part-of-speech tagging

```
python -m classla.models.tagger --save_dir models/pos/ --save_name ewt --wordvec_file ~/data/conll17/English/en.vectors.xz --train_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train+test.conllu --eval_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-dev.conllu --gold_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-dev.conllu --mode train --shorthand en_ewt --output_file temp.en

python -m classla.models.tagger --save_dir models/pos/ --save_name ewt --eval_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train+test.conllu --output_file pretagged/pos.ewt.train+test.conllu --gold_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-train+test.conllu --shorthand en_ewt --mode predict
python -m classla.models.tagger --save_dir models/pos/ --save_name ewt --eval_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-dev.conllu --output_file pretagged/pos.ewt.dev.conllu --gold_file ~/data/conll18/ud-treebanks-v2.4/UD_English-EWT/en_ewt-ud-dev.conllu --shorthand en_ewt --mode predict
```

### Lemmatization

```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file ewt --train_file pretagged/pos.ewt.train+test.conllu --eval_file pretagged/pos.ewt.dev.conllu --output_file temp.lemma.en --gold_file pretagged/pos.ewt.dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos

python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file ewt --eval_file pretagged/pos.ewt.train+test.conllu --output_file pretagged/pos.lemma.ewt.train+test.conllu --gold_file pretagged/pos.ewt.train+test.conllu --mode predict
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file ewt --eval_file pretagged/pos.ewt.dev.conllu --output_file pretagged/pos.lemma.ewt.dev.conllu --gold_file pretagged/pos.ewt.dev.conllu --mode predict
```

### Parsing

```
python -m classla.models.parser --save_dir models/depparse/ --save_name ewt --wordvec_file ~/data/conll17/English/en.vectors.xz --train_file pretagged/pos.lemma.ewt.train+test.conllu --eval_file pretagged/pos.lemma.ewt.dev.conllu --gold_file pretagged/pos.lemma.ewt.dev.conllu --shorthand en_ewt --output_file temp.depparse.en --mode train

python -m classla.models.parser --save_dir models/depparse/ --save_name ewt --eval_file pretagged/pos.lemma.ewt.dev.conllu --gold_file pretagged/pos.lemma.ewt.dev.conllu --shorthand en_ewt --output_file pretagged/pos.lemma.depparse.ewt.dev.conllu --mode predict
```
