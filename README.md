# CHILDES Processor

Scripts for extracting files from [CHILDES](https://childes.talkbank.org/) and processing them. The `/childes` folder contains example corpora downloaded from CHILDES and the `processed` folder contains example age-ordered child and adult utterances extracted from these corpora.

## Installation

To run the scripts, first install the required packages in `requirements.txt` by creating a conda environment or otherwise:

```
conda create --name childes_processor python=3.10 pip
conda activate childes_processor
pip install -r requirements.txt
```

If you are using the `download` command, make sure you have R installed.

If you are using the `phonemize` command, you will need to install the [espeak](https://github.com/espeak-ng/espeak-ng) backend. Note that on mac, you may need to point you may need to find where the dylib file was installed and make sure that phonemizer can find it by doing something like:

```
brew install espeak
export PHONEMIZER_ESPEAK_LIBRARY=/opt/homebrew/Cellar/espeak/1.48.04_1/lib/libespeak.dylib
```

## Usage

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
python childes_processor.py download Warren Eng-NA -o childes
```

This will save the utterances to `childes/Eng-NA/Warren.csv`. If `-s` is used, the data will be separated by speaker.

### Extract

The *extract* mode will process downloaded CSVs from CHILDES (those downloaded from the **download** tool) and extract the child and adult utterances, ordering them by child age. This takes advantage of the [AOCHILDES](https://github.com/UIUCLearningLanguageLab/AOCHILDES) library, which also does some basic pre-processing. For example, to extract all downloaded _Eng-NA_ corpora, run the following:

```
python childes_processor.py extract childes/Eng-NA -o processed/Eng-NA
```

This will take all the CSVs in the `childes/Eng-NA` folder and create two text files, `child.txt` and `adult.txt` in the `processed/Eng-NA` folder specified. These correspond to the age-ordered child and adult utterances, respectively. If the path provided is a CSV instead of a folder, just that CSV will be processed.

### Phonemize

The **phonemize** mode will take a text file of utterances and convert them into phonemes using IPA. This takes advantage of the *espeak* back-end and the language to phonemize to needs to be specified. For example, to phonemize the child utterances produced by the extract tool, run the following:

```
python childes_processor.py phonemize processed/Eng-NA/child.txt en-us -o phonemized/child.txt
```

This will phonome the child utterances found at `processed/Eng-NA/child.txt` and phonemize them using the `en-us` backend for espeak, placing the phonemized file into `phonemized/child.txt`. You can also use the `-s` option to split the utterances using a test-valid-train split of 90-5-5. When doing this, provide a directory instead of a file for the out path. For example:

```
python childes_processor.py phonemize processed/Eng-NA/child.txt en-us -o phonemized/Eng-NA -s
```
