import pytest

from moviesvaulttoolkit.fetch import DatasetsFetcher


@pytest.fixture
def base_fetcher(tmp_path) -> DatasetsFetcher:
    return DatasetsFetcher(str(tmp_path))


class TestDatasetFetcher:
    def test_basic_init_datasetfetcher(self, tmp_path):
        assert DatasetsFetcher(str(tmp_path)).output_path == tmp_path

    def test_fetch_datasets(self, base_fetcher: DatasetsFetcher):
        fetched = base_fetcher.fetch_datasets()
        content = list(base_fetcher.output_path.iterdir())
        assert fetched
        assert len(content) == len(fetched)
