from __future__ import annotations
from collections import UserDict
import logging
from typing import List
from mgnifyextract.runs import Run
from mgnifyextract.util import fetch_objects


logger = logging.getLogger(__name__)


def get_sample_runs(accession: str, max_results: int = None) -> List[Run]:
    results = fetch_objects("samples", accession, "runs", max_results=max_results)
    return [Run(result) for result in results]


class Sample(UserDict):

    def get_runs(self) -> List[Run]:
        return get_sample_runs(self.data["id"])

    def __str__(self):
        return f"Sample https://www.ebi.ac.uk/metagenomics/samples/{self.data['id']}"

    def __repr__(self):
        return f"<Sample https://www.ebi.ac.uk/metagenomics/samples/{self.data['id']}>"
