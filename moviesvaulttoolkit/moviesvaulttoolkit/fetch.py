from email import message
from typing import ClassVar, Iterable, List, Union
from pathlib import Path
import urllib.request as urll

import logging


class DatasetsFetcher:
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

    class DatasetsFetchingError(Exception):
        "Error raised when fetching datasets"
        def __init__(self, datasets, fetched, *args: object) -> None:
            msg = (
                f"Failed to fetch all {len(datasets)} datasets: {str(datasets)}"
                f"Fetched {len(fetched)} sources: {str(fetched)}!"
            )
            super().__init__(msg, *args)

    class SourceFetchingError(Exception):
        "Error raised when fetching single source"
        def __init__(self, source, output, *args: object) -> None:
            msg = f"Failed to fetch {source} into {output}!"
            super().__init__(msg, *args)


    @staticmethod
    def fetch(source: str, output: Union[Path, str]) -> Path:
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
            raise DatasetsFetcher.SourceFetchingError(source, output) from exc

        logging.debug('Fetched to %s', local_filename)
        logging.debug('Headers %s', str(headers))

        assert isinstance(local_filename, Path)
        return local_filename

    def fetch_datasets(self) -> Iterable[Path]:
        """Fetches datasets specified in DATASETS_NAMES

        Args:
            output_dir (Path): _description_

        Returns:
            Iterable[str]: _description_
        """
        self.output_path.mkdir(exist_ok=True)

        logging.debug(
            'Fetching %d files: %s',
            len(self.DATASETS_NAMES),
            ',\n'.join(self.DATASETS_NAMES)
        )

        fetched = [
            self.fetch(f"{self.URL_PREFIX}/{name}", self.output_path / name)
            for name in self.DATASETS_NAMES
        ]

        logging.debug(
            'Fetched %d files %s',
            len(fetched),
            ',\n'.join([_.as_posix() for _ in fetched])
        )

        if not len(fetched) == len(self.DATASETS_NAMES):
            raise self.DatasetsFetchingError(self.DATASETS_NAMES, fetched)

        return fetched


    def __init__(self, output_dir: Union[str, Path]) -> None:
        """Initialize DatasetFetcher

        Args:
            output_dir (Union[str, Path]): _description_
        """
        logging.debug('Initializing DatasetFetcher with %s', str(output_dir))
        self.output_path: Path = Path(output_dir).resolve()


if __name__ == '__main__':
    pass
