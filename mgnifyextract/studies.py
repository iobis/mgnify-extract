from __future__ import annotations
from collections import UserDict
import logging
from typing import Dict, List
from mgnifyextract.samples import Sample
from mgnifyextract.util import fetch_object, fetch_objects


logger = logging.getLogger(__name__)


def find_studies(filters: Dict, max_results: int = None) -> List[Study]:
    """Find studies by filters."""
    results = fetch_objects("studies", filters=filters, max_results=max_results)
    return [Study(result) for result in results]


def get_study(accession: str) -> Study:
    """Get study by accession."""
    study = fetch_object("studies", accession)
    return Study(study)


def get_study_samples(accession: str, max_results: int = None) -> List[Sample]:
    """Get samples for study by accession."""
    results = fetch_objects("studies", accession, "samples", max_results=max_results)
    return [Sample(result) for result in results]


def find_superstudies(filters: Dict, max_results: int = None) -> List[SuperStudy]:
    """Find superstudies by filters."""
    results = fetch_objects("super-studies", filters=filters, max_results=max_results)
    return [SuperStudy(result) for result in results]


def get_superstudy_studies(accession: str, max_results: int = None) -> List[Study]:
    """Get studies for superstudy by accession."""
    results = fetch_objects("super-studies", accession, "flagship-studies", max_results=max_results)
    return [Study(result) for result in results]


class Study(UserDict):

    def get_samples(self, max_results: int = None) -> List[Sample]:
        """Get samples for study."""
        return get_study_samples(self.data["id"], max_results=max_results)

    def __str__(self):
        return f"Study https://www.ebi.ac.uk/metagenomics/studies/{self.data['id']}"

    def __repr__(self):
        return f"<Study https://www.ebi.ac.uk/metagenomics/studies/{self.data['id']} >"


class SuperStudy(UserDict):

    def get_studies(self, max_results: int = None) -> List[Sample]:
        """Get studies for superstudy."""
        return get_superstudy_studies(self.data["id"], max_results=max_results)

    def __str__(self):
        return f"Superstudy https://www.ebi.ac.uk/metagenomics/super-studies/{self.data['id']}"

    def __repr__(self):
        return f"<Superstudy https://www.ebi.ac.uk/metagenomics/super-studies/{self.data['id']} >"
