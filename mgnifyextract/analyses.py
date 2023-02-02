from collections import UserDict
import logging
from typing import List
from mgnifyextract.downloads import Download
from mgnifyextract.util import fetch_object, fetch_objects


logger = logging.getLogger(__name__)


def get_analysis(accession: str) -> "Analysis":
    """Get analysis by accession."""
    analysis = fetch_object("analyses", accession)
    return Analysis(analysis)


def get_analysis_downloads(accession: str, max_results: int = None) -> List[Download]:
    """Get downloads for analysis by accession."""
    results = fetch_objects("analyses", accession, "downloads", max_results=max_results)
    return [Download.create(result) for result in results]


class Analysis(UserDict):

    def get_downloads(self, max_results: int = None) -> List[Download]:
        """Get analysis downloads."""
        return get_analysis_downloads(self.data["id"], max_results=max_results)

    def __str__(self):
        return f"Analysis https://www.ebi.ac.uk/metagenomics/analyses/{self.data['id']}"

    def __repr__(self):
        return f"<Analysis https://www.ebi.ac.uk/metagenomics/analyses/{self.data['id']}>"
