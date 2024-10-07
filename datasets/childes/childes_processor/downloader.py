import logging

class ChildesDownloader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # We only import childespy if the class is instantiated, since for some reason it re-downloads childesr each time
        self.logger.info('Importing childespy')
        from childespy import get_utterances
        self.get_utterances = get_utterances

    def download(self, collection, corpus, out_path, separate_by_child):

        self.logger.info(f'\n\nAttempting to get utterances from the "{corpus}" corpus in the "{collection}" collection:\n')
        utts = self.get_utterances(collection=collection, corpus=corpus)
        speakers = list(utts["target_child_name"].unique())
        path = out_path / f'{collection}'

        if separate_by_child:
            path = path / f'{corpus}'
            if not path.exists():
                path.mkdir(parents=True)
            for speaker in speakers:
                a = utts[utts["target_child_name"] == speaker]
                out_path = path /f'{speaker}.csv'
                if out_path.exists():
                    out_path.unlink()
                self.logger.info(f'Saving {len(a)} utterances to {out_path}')
                a.to_csv(out_path)
        else:
            if not path.exists():
                path.mkdir(parents=True)
            out_path = path / f'{collection if corpus is None else corpus}.csv'
            utts.to_csv(out_path)
            self.logger.info(f'Saving {len(utts)} utterances to {out_path}')
            