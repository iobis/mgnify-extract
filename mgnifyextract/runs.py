from collections import UserDict
import logging
from typing import List
from mgnifyextract.analyses import Analysis
from mgnifyextract.util import fetch_objects


logger = logging.getLogger(__name__)


def get_run_analyses(accession: str, max_results: int=None) -> List[Analysis]:
    results = fetch_objects("runs", accession, "analyses", max_results=max_results)
    return [Analysis(result) for result in results]


class Run(UserDict):
    
    def get_analyses(self) -> List[Analysis]:
        return get_run_analyses(self.data["id"])

    def __str__(self):
        return f"Run https://www.ebi.ac.uk/metagenomics/runs/{self.data['id']}"

    def __repr__(self):
        return f"<Run https://www.ebi.ac.uk/metagenomics/runs/{self.data['id']}>"
