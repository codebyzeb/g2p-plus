# BNC Processor Usage

The `bnc_processor.py` script extracts and phonemizes [Audio BNC](http://www.phon.ox.ac.uk/AudioBNC). Running this script will convert the Audio BNC phonemic transcriptions to IPA and split the transcriptions into utterances by aligning with the associated orthographic transcriptions. The `/bnc` folder contains example downloaded corpora. The `/bnc/BNC-dataset` folder is a repository hosted on Huggingface containing the dataset in an easily loadable format.

The BNC processor script has two modes. The first downloads the phonetic transcripts from AudioBNC and saves both the phonemes (converted to IPA) and the words in two files, `bnc_phonemes.txt` and `bnc_words.txt` respectively. Using the `--split` option, the `bnc_phonemes.txt` file will be split into train, validation and test files using a 90-5-5 split, sequentially:

```
python bnc_processor.py download --split -o bnc
```

The second mode is used to create a phonemic transcription from the orthographic transcription produced in `bnc_words.txt` by the `download` command. It is intended to compare the phonetic transcription produced by humans and a phonetic transcription created by the `phonemizer` tool. It also has the same split option:

```
python bnc_processor.py phonemize bnc/bnc_words.txt -s -o bnc
```
