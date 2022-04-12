import logging
import mgnifyextract
from urllib.parse import urlencode
from mgnifyextract.util import paginate


logger = logging.getLogger(__name__)


def get_run_analyses(accession, max_results=None):
    logger.info(f"Getting analyses for run {accession}")
    params = {
        "format": "json"
    }
    results = []
    url = mgnifyextract.API_URL + f"/runs/{accession}/analyses?" + urlencode(params)
    results = paginate(url, max_results)
    return results
