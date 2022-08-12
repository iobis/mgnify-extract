from collections import UserDict
import logging
from typing import List
from mgnifyextract.downloads import Download
from mgnifyextract.util import fetch_objects
from pysam import FastaFile
from urllib.request import urlopen
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
import gzip


logger = logging.getLogger(__name__)


def get_analysis_downloads(accession: str, max_results: int=None) -> List[Download]:
    results = fetch_objects("analyses", accession, "downloads", max_results=max_results)
    return [Download(result) for result in results]


def read_fasta_files(accession: str):
    downloads = get_analysis_downloads(accession)
    for download in [d for d in downloads if d["id"].endswith("SSU.fasta.gz") or d["id"].endswith("LSU.fasta.gz")]:
        
        with urlopen(download["links"]["self"]) as src, NamedTemporaryFile() as gz:
            copyfileobj(src, gz)
            with NamedTemporaryFile() as fasta:
                copyfileobj(gzip.open(gz.name), fasta)
                sequences = FastaFile(fasta.name)
                print(sequences)


class Analysis(UserDict):
    
    def get_downloads(self) -> List[Download]:
        return get_analysis_downloads(self.data["id"])

    def __str__(self):
        return f"Analysis https://www.ebi.ac.uk/metagenomics/analyses/{self.data['id']}"

    def __repr__(self):
        return f"<Analysis https://www.ebi.ac.uk/metagenomics/analyses/{self.data['id']}>"
