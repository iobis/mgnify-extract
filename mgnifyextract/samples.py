import logging
import mgnifyextract
from urllib.parse import urlencode
from mgnifyextract.util import paginate


logger = logging.getLogger(__name__)


def get_sample_runs(accession, max_results=None):
    logger.info(f"Getting runs for sample {accession}")
    params = {
        "format": "json"
    }
    results = []
    url = mgnifyextract.API_URL + f"/samples/{accession}/runs?" + urlencode(params)
    results = paginate(url, max_results)
    return results
