from typing import ClassVar, Iterable, List
from pathlib import Path
import urllib.request as urll

import logging

class DatasetFetcher:
    URL_PREFIX: ClassVar[str] = r'https://datasets.imdbws.com'
    DATASETS_NAMES: ClassVar[List[str]] = [
        'name.basics.tsv.gz',
        'title.akas.tsv.gz',
        'title.basics.tsv.gz',
        'title.crew.tsv.gz',
        'title.episode.tsv.gz',
        'title.principals.tsv.gz',
        'title.ratings.tsv.gz'
    ]

    def fetch(self, source: str, output: Path) -> str:
        """Fetches single dataset.

        Args:
            source (str): URL of dataset to fetch
            output (Path): Output path for given dataset

        Returns:
            str: Output path for given dataset
        """
        local_filename, headers = urll.urlretrieve(
            source, output
        )

        headers.

        return local_filename

    def fetch_datasets(self, output_dir: Path) -> Iterable[str]:
        for name in self.DATASETS_NAMES:
            self.fetch(
                f"{self.URL_PREFIX}/{name}",
                output_dir / name
            )
