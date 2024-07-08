import datasets

from typing import List

_DESCRIPTION = """\
Dataset for the transformer segmentation project.
The goal is to train a language model from scratch on phonemic data, without spaces, to see if transformers
will implicitly learn word boundaries. This dataset is a phonemized version of AUDIO BNC, a transcription of the British National Corpus.
"""

_HOMEPAGE = "https://huggingface.co/datasets/transformersegmentation/BNC"

filenames = [
    "train.txt", 
    "test.txt",
    "valid.txt"
]

class BNC(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.0.0")
    
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="BNC",
            description="Main section of Audio BNC with 2.5M utterances converted to IPA from the phonetic transcription",
        ),
        datasets.BuilderConfig(
            name="Ortho",
            description="Main section of Audio BNC with 2.5M utterances phonemized from the orthographic transcription",
        ),
    ]

    DEFAULT_CONFIG_NAME = "BNC"

    def _info(self):
            features = datasets.Features(
                {
                    "text": datasets.Value("string")
                }
            )
            return datasets.DatasetInfo(
                # This is the description that will appear on the datasets page.
                description=_DESCRIPTION,
                features=features,  # Here we define them above because they are different between the two configurations
                homepage=_HOMEPAGE,
            )


    def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
        """ 
        Returns data for different splits 
        """
    
        data_dir = self.config.name

        urls_to_download = {
            "train": f"{data_dir}/train.txt",
            "dev": f"{data_dir}/valid.txt",
            "test": f"{data_dir}/test.txt"
        } 

        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "split": "train",
                    "filepaths": downloaded_files["train"]}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "split": "dev",
                    "filepaths": downloaded_files["dev"]}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "split": "test",
                    "filepaths": downloaded_files["test"]
                }
            ),
        ]

     # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, split, filepaths):
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.

        # the filepaths should be a list of filepaths 
        if isinstance(filepaths, str):
            filepaths = [filepaths]
        
        global_idx = 0 

        for filepath in filepaths:
            with open(filepath, encoding="utf-8") as f:
                for row in f:
                    yield global_idx, {"text": row}
                    global_idx += 1 