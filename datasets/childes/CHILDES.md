# CHILDES Phonemized Dataset

The `childes_processor.py` script allows for extracing files from [CHILDES](https://childes.talkbank.org/) and processing them. The `/childes` folder contains example corpora downloaded, processed and extracted from CHILDES. The `/childes/CHILDES-dataset` folder is a repository hosted on Huggingface containing the dataset in an easily loadable format.

This directory contains the `childes_processor.py` script which can download, process and phonemize corpora from [CHILDES](https://childes.talkbank.org/). The `/childes` folder contains example corpora downloaded, processed and extracted from CHILDES. The scripts `/scripts/create_all_childes` which was used to create the phonemized CHILDES dataset used in the TransformerSegmentation experiments. A copy of the dataset can be found found in `/CHILDES-dataset`.

## Installation

See [README](../../README.md) for the main installation.

If you are using the `download` command from the CHILDES processor, make sure you have R installed.

# CHILDES Processor Usage

The `childes_processor.py` has three modes: *download*, *process* and *extract*, allowing the user to download and phonemize the CHILDES dataset. 

To bring up the help menu, simply type:

```
python childes_processor.py -h
```

Or for each mode, there is also a help menu:

```
python childes_processor.py extract -h
```

## Download

The **download** mode allows for corpora to be downloaded from CHILDES. For example, to download the _Warren_ corpus from the _Eng-NA_ collection, run the following:

```
python childes_processor.py download Eng-NA --corpus Warren -o childes/downloaded
```

This will save the utterances to `downloaded/Eng-NA/Warren.csv`. If `-s` is used, the data will be separated by speaker. The command can also be run without the corpus provided, downloading all corpora available in the collection:

```
python childes_processor.py download Eng-NA -o downloaded
```

## Process

The *process* mode will process downloaded CSVs from CHILDES (those downloaded from the **download** tool) and provide a new CSV with additional columns and utterances sorted by child age. The additional columns are as follows:

| Column | Description |
|:----|:-----|
| `is_child`| Whether the utterance was spoken by a child or not. Note that unless the `-k` or `--keep` flag is set, all child utterances will be dicarded so this column will only contain `False`. |
| `processed_gloss`| The pre-processed orthographic utterance. This includes lowercasing, fixing English spelling and adding punctuation marks. This is based on the [AOChildes](https://github.com/UIUCLearningLanguageLab/AOCHILDES) preprocessing.|
| `phonemized_utterance`| A phonemic transcription of the utterance in IPA, space-separated with word boundaries marked with the `WORD_BOUNDARY` token. This uses the espeak backend (or segments for japanese). |
| `language_code`| Language code used for producing the phonemic transcriptions. May not match the `language` column provided by CHILDES (e.g. Eng-NA and Eng-UK tend to be transcribed with eng-us and eng-gb). |
| `character_split_utterance`| A space separated transcription of the utterance, produced simply by splitting the processed gloss by character. This is intended to have a very similar format to `phonemized_utterance` for studies comparing phonetic to orthographic transcriptions. |

The first required argument is the CSV or folder of CSVs to process. The second argument is the language that will be used for producing the phonetic transcription. To view supported languages, use `-h`. 

The `-k` or `--keep` flag is used to keep child utterances. The `-s` or `--split` flag is used to split the resulting dataset into training set and a validation set containin 10,000 utterances. The `-m` or `--max_age` flag is used to discard all utterances produced when the child's age greater than the provided number of months.

For example, to process all downloaded _Eng-NA_ corpora, run the following:

```
python childes_processor.py process downloaded/Eng-NA EnglishNA -o processed/Eng-NA -s
```

This will take all the CSVs in the `downloaded/Eng-NA` folder and create two new CSVs, `train.csv` and `valid.csv` in the `processed/Eng-NA` folder specified containing processed utterances and additional useful information. These datasets contain phonemic transcriptions of each utterance that have been produced using the `en-us` language backend. If the path provided is a CSV instead of a folder, just that CSV will be processed.

## Extract

The **extract** mode will take a CSV dataset and produce a text file containing a column from that CSV dataset. It has the option use a maximum cutoff, as with the process mode, using `-m` or `--max_age`. The intended use is to gather all phonemic or orthographic utterances from the processed dataset (but can also be used to extract other columns, or to extract from a downloaded CSV that hasn't been processed). 

For example, to extract all phonemic utterances from the train file produced by the previous example, only including utterances targetting children under the age of 2, run the following:

```
python childes_processor.py extract processed/Eng-NA/train.csv phonemized_utterance -o extracted/Eng-NA -m 24
```

This will create a file `childes/extracted/Eng-NA/utterances.txt` containing the contents of the `phonemized_utterance` column where `target_child_age` is less than 24 months.