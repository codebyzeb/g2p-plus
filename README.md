# Corpus Phonemizers

This repository contains scripts for converting various corpora to a unified IPA format, with marked word and utterance boundaries, to prepare them for [training and evaluating small transformer-based language models](https://github.com/codebyzeb/TransformerSegmentation).

This code base was initially designed to prepare the CHILDES corpora for these experiments but now also contains the scripts that were used to prepare phonemized versions of the British National Corpus, the BabyLM training data and the BabyLM evaluation data. Each subdirectory in `/datasets` contains a copy of each generated dataset and the scripts used to generate the dataset. In some cases, analysis notebooks and scripts to train tokenizers are also included.

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
