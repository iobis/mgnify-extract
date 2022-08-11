from __future__ import annotations
from collections import UserDict
import logging
from typing import List
import mgnifyextract
from urllib.parse import urlencode
from mgnifyextract.runs import Run
from mgnifyextract.util import paginate


logger = logging.getLogger(__name__)


def get_sample_runs(accession: str, max_results: int=None) -> List[Run]:
    logger.debug(f"Getting runs for sample {accession}")
    params = {
        "format": "json"
    }
    results = []
    url = mgnifyextract.API_URL + f"/samples/{accession}/runs?" + urlencode(params)
    results = paginate(url, max_results)
    return [Run(result) for result in results]


class Sample(UserDict):

    def get_runs(self) -> List[Run]:
        return get_sample_runs(self.data["id"])

    def __str__(self):
        return f"Sample {self.data['id']}"

    def __repr__(self):
        return f"<Sample {self.data['id']}>"
