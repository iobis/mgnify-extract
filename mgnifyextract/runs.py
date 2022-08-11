from collections import UserDict
import logging
from typing import List
import mgnifyextract
from urllib.parse import urlencode
from mgnifyextract.analyses import Analysis
from mgnifyextract.util import paginate


logger = logging.getLogger(__name__)


def get_run_analyses(accession: str, max_results: int=None) -> List[Analysis]:
    logger.debug(f"Getting analyses for run {accession}")
    params = {
        "format": "json"
    }
    results = []
    url = mgnifyextract.API_URL + f"/runs/{accession}/analyses?" + urlencode(params)
    results = paginate(url, max_results)
    return [Analysis(result) for result in results]


class Run(UserDict):
    
    def get_analyses(self) -> List[Analysis]:
        return get_run_analyses(self.data["id"])

    def __str__(self):
        return f"Run {self.data['id']}"

    def __repr__(self):
        return f"<Run {self.data['id']}>"
