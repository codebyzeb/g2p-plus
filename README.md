# CHILDES_processor
Scripts for extracting files from [CHILDES](https://childes.talkbank.org/) and processing them. The `/childes` folder contains example corpora downloaded from CHILDES and the `processed` folder contains example age-ordered child and adult utterances extracted from these corpora.

## Usage

To run the scripts, first install the required packages in `requirements.txt` by creating a conda environment or otherwise:

```
conda create --name childes_processor python=3.8 pip
conda activate childes_processor
pip install -r requirements.txt
```

To download a corpus from CHILDES, run the `download_childes.py` script. This saves all the utterances from the Warren corpus into a csv file.

```
python scripts/download_childes.py Warren
```

To extract the child and adult utterances from the corpus, run the `extract_utterances.py` script. This takes advantage of the AOCHILDES library to extract the utterances and place them in a folder in the same directory.

```
python scripts/extract_utterances.py childes/Eng-NA/Warren.csv
```

If the script is run on a directory instead of a csv file, the utterances will be concatenated for all csv files found in that directory. THE AOCHILDES library orders the utterances by the age of the target child. 