# Corpus Phonemizers

This repository contains scripts for converting a series of corpora to a unified IPA format, with marked word and utterance boundaries. 

The `childes_processor.py` script allows for extracing files from [CHILDES](https://childes.talkbank.org/) and processing them. The `/childes` folder contains example corpora downloaded, processed and extracted from CHILDES. The `/childes/CHILDES-dataset` folder is a repository hosted on Huggingface containing the dataset in an easily loadable format.

The `bnc_processor.py` script extracts and phonemizes [Audio BNC](http://www.phon.ox.ac.uk/AudioBNC). Running this script will convert the Audio BNC phonemic transcriptions to IPA and split the transcriptions into utterances by aligning with the associated orthographic transcriptions. The `/bnc` folder contains example downloaded corpora. The `/bnc/BNC-dataset` folder is a repository hosted on Huggingface containing the dataset in an easily loadable format.

## Installation

To run the scripts, first create a virtual environment for the project by running `setup.sh`.

```
./setup.sh
source setup.sh
```

If you are using the `download` command from the CHILDES processor, make sure you have R installed.

If you are using the `process` command from the CHILDES processor, you will need to install the [espeak](https://github.com/espeak-ng/espeak-ng) backend. Note that on mac, you may need to point you may need to find where the dylib file was installed and make sure that phonemizer can find it by doing something like:

```
brew install espeak
export PHONEMIZER_ESPEAK_LIBRARY=/opt/local/lib/libespeak-ng.dylib
```
