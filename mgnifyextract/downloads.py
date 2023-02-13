from collections import UserDict
import logging
from pysam import FastaFile
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
import gzip
from mgnifyextract.util import download_file
import pandas as pd
from Bio.SeqIO.FastaIO import SimpleFastaParser


logger = logging.getLogger(__name__)


class Download(UserDict):

    @staticmethod
    def create(data):
        if data["attributes"]["file-format"]["name"] == "FASTA":
            return FastaDownload(data)
        elif ".mseq" in data["attributes"]["alias"]:
            return MseqDownload(data)
        elif data["attributes"]["file-format"]["name"] == "TSV":
            return TsvDownload(data)
        elif data["attributes"]["file-format"]["name"] == "HDF5 Biom":
            return Hdf5BiomDownload(data)
        elif data["attributes"]["file-format"]["name"] == "JSON Biom":
            return JsonBiomDownload(data)
        else:
            return Download(data)

    def __init__(self, data):
        UserDict.__init__(self, data)
        if "_SSU" in self.data["id"]:
            self.marker = "SSU"
        elif "_LSU" in self.data["id"]:
            self.marker = "LSU"
        else:
            self.marker = None

    def file_format(self) -> str:
        """Get download file format."""
        return self.data["attributes"]["file-format"]["name"]

    def group_type(self) -> str:
        """Get download group type."""
        return self.data["attributes"]["group-type"]

    def url(self) -> str:
        """Get download URL."""
        return self.data["links"]["self"]

    def __str__(self):
        return f"{self.__class__.__name__} {self.file_format()} {self.group_type()} {self.data['links']['self']}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.file_format()} {self.group_type()} {self.data['links']['self']} >"


class TsvDownload(Download):

    def read(self) -> pd.DataFrame:
        """Read file."""
        with NamedTemporaryFile(suffix=".tsv") as tsv:
            download_file(self.url(), tsv.name)
            df = pd.read_csv(tsv.name, sep="\t", skiprows=[0])
            return df

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.group_type()} {self.data['links']['self']} >"


class MseqDownload(Download):

    def read(self) -> pd.DataFrame:
        """Read file."""
        with NamedTemporaryFile(suffix=".gz") as gz:
            download_file(self.url(), gz.name)
            with gzip.open(gz.name, "rb") as f_in, NamedTemporaryFile(suffix=".mseq") as f_out:
                copyfileobj(f_in, f_out)
                df = pd.read_csv(f_out.name, sep="\t", skiprows=[0])
                return df

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.group_type()} {self.data['links']['self']} >"


class Hdf5BiomDownload(Download):

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.group_type()} {self.data['links']['self']} >"


class JsonBiomDownload(Download):

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.group_type()} {self.data['links']['self']} >"


class FastaDownload(Download):

    def read_pandas(self) -> pd.DataFrame:

        with NamedTemporaryFile(suffix=".gz") as gz:
            download_file(self.url(), gz.name)
            with gzip.open(gz.name, "rb") as f_in, NamedTemporaryFile(suffix=".fasta") as f_out:
                copyfileobj(f_in, f_out)
                with open(f_out.name) as fasta_file:
                    records = [{"reference": reference, "sequence": sequence} for reference, sequence in SimpleFastaParser(fasta_file)]
                    df = pd.DataFrame(records)
                    return df

    def read_pysam(self) -> FastaFile:
        format = self.file_format()
        if (format == "FASTA"):
            with NamedTemporaryFile(suffix=".gz") as gz:
                download_file(self.url(), gz.name)
                with gzip.open(gz.name, "rb") as f_in, NamedTemporaryFile(suffix=".fasta") as f_out:
                    copyfileobj(f_in, f_out)
                    fasta = FastaFile(f_out.name)
                    return fasta
        else:
            message = f"Format {format} not supported"
            logger.error(message)
            raise RuntimeError(message)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.group_type()} {self.data['links']['self']} >"
