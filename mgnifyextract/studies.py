import logging
import mgnifyextract
from urllib.parse import urlencode
from mgnifyextract.util import paginate
import requests


logger = logging.getLogger(__name__)


def find_studies(filters, max_results=None):
    params = {
        "format": "json"
    }
    if filters is not None:
        params = params | filters
    url = mgnifyextract.API_URL + "/studies?" + urlencode(params)
    results = paginate(url, max_results)
    return results


def get_study(accession):
    logger.info(f"Getting study {accession}")
    params = {
        "format": "json"
    }
    url = mgnifyextract.API_URL + f"/studies/{accession}?" + urlencode(params)
    res = requests.get(url)
    logger.debug(res.url)
    if res.status_code != 200:
        message = f"Unexpected status code {res.status_code} for {url}"
        logger.error(message)
        raise RuntimeError(message)
    else:
        data = res.json()["data"]
        return data


def get_study_samples(accession, max_results=None):
    logger.info(f"Getting samples for study {accession}")
    params = {
        "format": "json"
    }
    results = []
    url = mgnifyextract.API_URL + f"/studies/{accession}/samples?" + urlencode(params)
    results = paginate(url, max_results)
    return results


def find_superstudies(filters, max_results=None):
    params = {
        "format": "json"
    }
    if filters is not None:
        params = params | filters
    url = mgnifyextract.API_URL + "/super-studies?" + urlencode(params)
    results = paginate(url, max_results)
    return results


def get_superstudy_studies(accession, max_results=None):
    logger.info(f"Getting studies for super-study {accession}")
    params = {
        "format": "json"
    }
    results = []
    url = mgnifyextract.API_URL + f"/super-studies/{accession}/flagship-studies?" + urlencode(params)
    results = paginate(url, max_results)
    return results
