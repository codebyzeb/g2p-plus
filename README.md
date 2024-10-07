# Corpus Phonemizers

This repository contains scripts for converting various corpora to a unified IPA format, with marked word and utterance boundaries, to prepare them for [training and evaluating small transformer-based language models](https://github.com/codebyzeb/TransformerSegmentation).

The main entry point is `corpus_phonemizer.py` (see below for usage). This repository also contains scripts used to prepare phonemized versions of specific corpora in `/datasets`, including:

* CHILDES
* BabyLM training data
* BabyLM evaluation data (including BLiMP, BLiMP Supplement, GLUE, EWoK)
* British National Corpus (BNC)

In some cases, analysis notebooks and scripts to train tokenizers are also included.

## Installation

To run the scripts, first create a virtual environment for the project by running `setup.sh`.

```
./setup.sh
source setup.sh
```

### Additional dependencies

The `corpus_phonemizer.py` with the `phonemizer` backend requires [`espeak-ng`](https://github.com/espeak-ng/espeak-ng) to be installed.

On mac, the backend requires `PHONEMIZER_ESPEAK_LIBRARY` to be set in the local environment. This will be read automatically from `.env`. You can add a line as follows to `.env` file and it will be applied automatically when you source `setup.sh`, e.g:

```
export PHONEMIZER_ESPEAK_LIBRARY=/opt/local/lib/libespeak-ng.dylib
```

The `epitran` backend with Mandarin requires [CEDICT](https://www.mdbg.net/chinese/dictionary?page=cedict) to be downloaded and placed in `/data/cedict_ts.u8`. 

The `epitran` backend with English requires Flite to be installed. See instructions [here](https://github.com/dmort27/epitran#installation-of-flite-for-english-g2p). 

## Usage

The `corpus_phonemizer.py` script is the main entry point for converting corpora to a unified IPA format. It supports multiple backends, including [epitran](https://github.com/dmort27/epitran) and [phonemizer](https://github.com/bootphon/phonemizer), each of which supports multiple languages. The help menu (`-h`) describes usage and the languages supported by each backend. The script reads lines from an input file (using `-i`) and saves space-separated IPA phonemes to an output file (using `-o`) or reads/writes to/from STDIN/STDOUT if files are not provided. Word boundaries are provided between words using `-k` using a `WORD_BOUNDARY` token.

For many languages, the underlying transcription tool does not output phoneme sets that match typical phoneme inventories for that language. As such, we have implemented "folding" dictionaries for many languages that attempt to map the output of a backend for a language to a standard phoneme inventory. See `src/dicts.py` for these dictionaries. This "folding" can be turned off using `-u`. 

Example usage:

```
> python phonemize.py phonemizer en-gb -k
hello there!
h ə l əʊ WORD_BOUNDARY ð eə WORD_BOUNDARY
```

