from collections import UserDict
import logging
from typing import List
from mgnifyextract.downloads import Download
from mgnifyextract.util import fetch_objects


logger = logging.getLogger(__name__)


def get_analysis_downloads(accession: str, max_results: int = None) -> List[Download]:
    results = fetch_objects("analyses", accession, "downloads", max_results=max_results)
    return [Download.create(result) for result in results]


class Analysis(UserDict):

    def get_downloads(self, max_results: int = None) -> List[Download]:
        return get_analysis_downloads(self.data["id"], max_results=max_results)

    def get_fasta_files(self, max_results: int = None) -> List[Download]:
        results = [download for download in self.get_downloads() if download.file_format() == "FASTA"]
        if max_results is not None and len(results) >= max_results:
            results = results[:max_results]
        return results

    def __str__(self):
        return f"Analysis https://www.ebi.ac.uk/metagenomics/analyses/{self.data['id']}"

    def __repr__(self):
        return f"<Analysis https://www.ebi.ac.uk/metagenomics/analyses/{self.data['id']}>"
