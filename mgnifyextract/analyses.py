import logging
import mgnifyextract
from urllib.parse import urlencode
from mgnifyextract.util import paginate
from pysam import FastaFile
from urllib.request import urlopen
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
import gzip


logger = logging.getLogger(__name__)


def get_analysis_downloads(accession, max_results=None):
    logger.debug(f"Getting downloads for analysis {accession}")
    params = {
        "format": "json"
    }
    results = []
    url = mgnifyextract.API_URL + f"/analyses/{accession}/downloads?" + urlencode(params)
    results = paginate(url, max_results)
    return results


def read_fasta_files(accession):
    downloads = get_analysis_downloads(accession)
    for download in [d for d in downloads if d["id"].endswith("SSU.fasta.gz") or d["id"].endswith("LSU.fasta.gz")]:
        
        with urlopen(download["links"]["self"]) as src, NamedTemporaryFile() as gz:
            copyfileobj(src, gz)
            with NamedTemporaryFile() as fasta:
                copyfileobj(gzip.open(gz.name), fasta)
                sequences = FastaFile(fasta.name)
                print(sequences)

