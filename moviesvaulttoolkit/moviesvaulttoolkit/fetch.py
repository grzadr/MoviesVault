from email import message
from typing import ClassVar, Iterable, List, Union
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

    class FetchingError(Exception):
        "Error raised when fetching sources"
        def __init__(self, source, output, *args: object) -> None:
            msg = f"Failed to fetch {source} into {output}!"
            super().__init__(msg, *args)

    def fetch(self, source: str, output: Union[Path, str]) -> str:
        """Fetches single dataset.

        Args:
            source (str): URL of dataset to fetch
            output (Path): Output path for given dataset

        Returns:
            str: Output path for given dataset
        """
        output_path = Path(output)
        logging.debug("Fetching %s to %s", source, output_path.as_posix())

        try:
            local_filename, headers = urll.urlretrieve(
                source, output
            )
        except Exception as exc:
            raise self.FetchingError(source, output) from exc

        logging.debug("Fetched to  %s", local_filename)
        logging.debug("Headers %s", str(headers))

        return local_filename

    def fetch_datasets(self, output_dir: Union[Path, str]) -> Iterable[str]:
        """Fetches datasets specified in DATASETS_NAMES

        Args:
            output_dir (Path): _description_

        Returns:
            Iterable[str]: _description_
        """
        output_path = Path(output_dir).resolve()
        output_path.mkdir(exist_ok=True)

        for name in self.DATASETS_NAMES:
            self.fetch(
                f"{self.URL_PREFIX}/{name}",
                output_path / name
            )
