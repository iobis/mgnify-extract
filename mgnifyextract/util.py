from typing import Dict, List
import requests
import logging
from mgnifyextract import API_URL
from urllib.parse import urlencode
import shutil


logger = logging.getLogger(__name__)


def fetch_object(name: str, accession: str) -> Dict:
    logger.debug(f"Fetching {name}/{accession}")
    params = {
        "format": "json"
    }
    url = f"{API_URL}/{name}/{accession}?" + urlencode(params)
    res = requests.get(url)
    logger.debug(f"Fetching {res.url}")
    if res.status_code != 200:
        message = f"Unexpected status code {res.status_code} for {url}"
        logger.error(message)
        raise RuntimeError(message)
    else:
        return res.json()["data"]


def fetch_objects(name: str, accession: str = None, child_name: str = None, filters: Dict = None, max_results: int = None) -> List[Dict]:
    params = {
        "format": "json"
    }
    if filters is not None:
        params = params | filters
    endpoint_parts = [name, accession, child_name]
    endpoint = "/".join([part for part in endpoint_parts if part is not None])
    url = f"{API_URL}/{endpoint}?" + urlencode(params)
    return paginate(url, max_results)


def paginate(url: str, max_results: int = None) -> List[Dict]:
    results = []

    while True:
        res = requests.get(url)
        logger.debug(f"Fetching {res.url}")
        if res.status_code != 200:
            message = f"Unexpected status code {res.status_code} for {url}"
            logger.error(message)
            raise RuntimeError(message)
        else:
            data = res.json()
            results.extend(data["data"])
            next = data.get("links", {}).get("next")
            if next is None:
                break
            elif max_results is not None and len(results) >= max_results:
                break
            else:
                url = next

    if max_results is not None and len(results) >= max_results:
        results = results[:max_results]

    return results


def download_file(url: str, path: str) -> None:
    with requests.get(url, stream=True) as r:
        r.raw.decode_content = True
        with open(path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
