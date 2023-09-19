# Corpus Phonemizers

This repository contains scripts for converting a series of corpora to a unified IPA format, with marked word and utterance boundaries. 

The `childes_processor.py` script allows for extracing files from [CHILDES](https://childes.talkbank.org/) and processing them. The `/childes` folder contains example corpora downloaded, processed and phonemized from CHILDES. The `/childes/CHILDES-dataset` folder is a repository hosted on Huggingface containing the dataset in an easily loadable format.

The `bnc_processor.py` script extracts and phonemizes [Audio BNC](http://www.phon.ox.ac.uk/AudioBNC). Running this script will convert the Audio BNC phonemic transcriptions to IPA and split the transcriptions into utterances by aligning with the associated orthographic transcriptions. The `/bnc` folder contains example downloaded corpora. The `/bnc/BNC-dataset` folder is a repository hosted on Huggingface containing the dataset in an easily loadable format.

## Installation

To run the scripts, first create a virtual environment for the project by running `setup.sh`.

```
./setup.sh
source setup.sh
```

If you are using the `download` command from the CHILDES processor, make sure you have R installed.

If you are using the `phonemize` command from the CHILDES processor, you will need to install the [espeak](https://github.com/espeak-ng/espeak-ng) backend. Note that on mac, you may need to point you may need to find where the dylib file was installed and make sure that phonemizer can find it by doing something like:

```
brew install espeak
export PHONEMIZER_ESPEAK_LIBRARY=/opt/homebrew/lib/libespeak.dylib
```

## CHILDES Processor Usage

The entry point is `childes_processor.py`, which has three modes: *download*, *extract* and *phonemize*. To bring up the help menu, simply type:

```
python childes_processor.py -h
```

Or for each mode, there is also a help menu:

```
python childes_processor.py extract -h
```

### Download

The **download** mode allows for corpora to be downloaded from CHILDES. For example, to download the _Warren_ corpus from the _Eng-NA_ collection, run the following:

```
python childes_processor.py download Eng-NA --corpus Warren -o downloaded
```

This will save the utterances to `downloaded/Eng-NA/Warren.csv`. If `-s` is used, the data will be separated by speaker. The command can also be run without the corpus provided, downloading all corpora available in the collection:

```
python childes_processor.py download Eng-NA -o downloaded
```

### Extract

The *extract* mode will process downloaded CSVs from CHILDES (those downloaded from the **download** tool) and extract the child and adult utterances, ordering them by child age. This takes advantage of the [AOCHILDES](https://github.com/UIUCLearningLanguageLab/AOCHILDES) library, which also does some basic pre-processing. For example, to extract all downloaded _Eng-NA_ corpora, run the following:

```
python childes_processor.py extract downloaded/Eng-NA -o processed/Eng-NA
```

This will take all the CSVs in the `downloaded/Eng-NA` folder and create two text files, `child.txt` and `adult.txt` in the `processed/Eng-NA` folder specified. These correspond to the age-ordered child and adult utterances, respectively. If the path provided is a CSV instead of a folder, just that CSV will be processed.

### Phonemize

The **phonemize** mode will take a text file of utterances and convert them into phonemes using IPA. This takes advantage of the *espeak* back-end and the language to phonemize to needs to be specified. For example, to phonemize the child utterances produced by the extract tool, run the following:

```
python childes_processor.py phonemize processed/Eng-NA/adult.txt en-us -o phonemized/adult.txt
```

This will phonome the adult utterances found at `processed/Eng-NA/adult.txt` and phonemize them using the `en-us` backend for espeak, placing the phonemized file into `phonemized/adult.txt`. You can also use the `-s` option to split the utterances using a test-valid-train split of 90-5-5. When doing this, provide a directory instead of a file for the out path. For example:

```
python childes_processor.py phonemize processed/Eng-NA/adult.txt en-us -o phonemized/Eng-NA -s
```

## BNC Processor Usage

The BNC processor script has two modes. The first downloads the phonetic transcripts from AudioBNC and saves both the phonemes (converted to IPA) and the words in two files, `bnc_phonemes.txt` and `bnc_words.txt` respectively. Using the `--split` option, the `bnc_phonemes.txt` file will be split into train, validation and test files using a 90-5-5 split, sequentially:

```
python bnc_processor.py download --split -o bnc
```

The second mode is used to create a phonemic transcription from the orthographic transcription produced in `bnc_words.txt` by the `download` command. It is intended to compare the phonetic transcription produced by humans and a phonetic transcription created by the `phonemizer` tool. It also has the same split option:

```
python bnc_processor.py phonemize bnc/bnc_words.txt -s -o bnc
```
