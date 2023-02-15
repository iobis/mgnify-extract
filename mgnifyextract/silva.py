import pandas as pd
from urllib.request import urlopen
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
import tarfile
import os
from mgnifyextract.util import clean_taxonomy_string


def download_silva_otus(marker: str, pipeline_version, date) -> None:
    silva_gz_file = f"silva_{marker.lower()}-{date}.tar.gz"
    silva_otu_file = f"silva_{marker.lower()}-{date}/{marker.lower()}2.otu"
    cache_dir = os.path.expanduser("~/.cache/mgnifyextract")
    url = f"ftp://ftp.ebi.ac.uk/pub/databases/metagenomics/pipeline-{pipeline_version}/ref-dbs/{silva_gz_file}"
    with urlopen(url) as fsrc, NamedTemporaryFile() as fdst:
        copyfileobj(fsrc, fdst)
        tar_file = tarfile.open(fdst.name)
        tar_file.extract(silva_otu_file, cache_dir)
        tar_file.close()


def read_otu_file(marker: str, pipeline_version: str, date: str) -> pd.DataFrame:
    silva_otu_file = f"silva_{marker.lower()}-{date}/{marker.lower()}2.otu"
    silva_otu_file_full = os.path.expanduser(f"~/.cache/mgnifyextract/{silva_otu_file}")
    if not os.path.isfile(silva_otu_file_full):
        download_silva_otus(marker, pipeline_version, date)
    df = pd.read_csv(silva_otu_file_full, sep="\t", header=None, usecols=["taxonomy", "taxonomy_id"], names=["row", "taxonomy", "taxonomy_id"], dtype={"taxonomy": str, "taxonomy_id": str})
    return df


def get_silva_otus(markers: list[str] = ["SSU", "LSU"], pipeline_version="5.0", date="20200130") -> pd.DataFrame:
    frames = [read_otu_file(marker, pipeline_version, date) for marker in markers]
    otus = pd.concat(frames)
    otus["taxonomy"] = otus["taxonomy"].apply(clean_taxonomy_string)
    otus = otus.groupby("taxonomy").nth(0).reset_index()
    return otus
