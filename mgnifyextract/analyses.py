import logging
import mgnifyextract
from urllib.parse import urlencode
from mgnifyextract.util import paginate


logger = logging.getLogger(__name__)


def get_analysis_downloads(accession, max_results=None):
    logger.info(f"Getting downloads for analysis {accession}")
    params = {
        "format": "json"
    }
    results = []
    url = mgnifyextract.API_URL + f"/analyses/{accession}/downloads?" + urlencode(params)
    results = paginate(url, max_results)
    return results
