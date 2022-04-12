import requests
import logging


logger = logging.getLogger(__name__)


def get_entity(url):
    res = requests.get(url)
    logger.debug(res.url)
    if res.status_code != 200:
        message = f"Unexpected status code {res.status_code} for {url}"
        logger.error(message)
        raise RuntimeError(message)
    else:
        return res.json()["data"]


def paginate(url, max_results=None):
    results = []

    while True:
        res = requests.get(url)
        logger.debug(res.url)
        if res.status_code != 200:
            message = f"Unexpected status code {res.status_code} for {url}"
            logger.error(message)
            raise RuntimeError(message)
        else:
            data = res.json()
            results.extend(data["data"])
            next = data.get("links", {}).get("next")
            if next is not None:
                url = next
            else:
                break
        if max_results is not None and len(results) >= max_results:
            results = results[:max_results]
            break

    return results
