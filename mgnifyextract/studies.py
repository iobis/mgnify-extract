from __future__ import annotations
from collections import UserDict
import logging
from typing import Dict, List
import mgnifyextract
from urllib.parse import urlencode
from mgnifyextract.samples import Sample
from mgnifyextract.util import paginate, get_entity


logger = logging.getLogger(__name__)


def find_studies(filters: Dict, max_results: int=None) -> List[Study]:
    params = {
        "format": "json"
    }
    if filters is not None:
        params = params | filters
    url = mgnifyextract.API_URL + "/studies?" + urlencode(params)
    results = paginate(url, max_results)
    return [Study(result) for result in results]


def get_study(accession: str) -> Study:
    logger.debug(f"Getting study {accession}")
    params = {
        "format": "json"
    }
    url = mgnifyextract.API_URL + f"/studies/{accession}?" + urlencode(params)
    return Study(get_entity(url))


def get_study_samples(accession: str, max_results: int=None) -> List[Sample]:
    logger.debug(f"Getting samples for study {accession}")
    params = {
        "format": "json"
    }
    results = []
    url = mgnifyextract.API_URL + f"/studies/{accession}/samples?" + urlencode(params)
    results = paginate(url, max_results)
    return [Sample(result) for result in results]


def find_superstudies(filters: Dict, max_results: int=None) -> List[SuperStudy]:
    params = {
        "format": "json"
    }
    if filters is not None:
        params = params | filters
    url = mgnifyextract.API_URL + "/super-studies?" + urlencode(params)
    results = paginate(url, max_results)
    return [SuperStudy(result) for result in results]


def get_superstudy_studies(accession: str, max_results: int=None) -> List[Study]:
    logger.debug(f"Getting studies for super-study {accession}")
    params = {
        "format": "json"
    }
    results = []
    url = mgnifyextract.API_URL + f"/super-studies/{accession}/flagship-studies?" + urlencode(params)
    results = paginate(url, max_results)
    return [Study(result) for result in results]


class Study(UserDict):

    def get_samples(self, **kwargs) -> List[Sample]:
        return get_study_samples(self.data["id"], **kwargs)

    def __str__(self):
        return f"Study {self.data['id']}"

    def __repr__(self):
        return f"<Study {self.data['id']}>"


class SuperStudy(UserDict):

    def get_studies(self, **kwargs) -> List[Sample]:
        return get_superstudy_studies(self.data["id"], **kwargs)

    def __str__(self):
        return f"Superstudy {self.data['id']}"

    def __repr__(self):
        return f"<Superstudy {self.data['id']}>"
