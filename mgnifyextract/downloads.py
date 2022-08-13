from collections import UserDict
import logging
from pysam import FastaFile
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
import gzip
from mgnifyextract.util import download_file


logger = logging.getLogger(__name__)


class Download(UserDict):

    @staticmethod
    def create(data):
        if data["attributes"]["file-format"]["name"] == "FASTA":
            return FastaDownload(data)
        elif data["attributes"]["file-format"]["name"] == "TSV":
            return TsvDownload(data)
        elif data["attributes"]["file-format"]["name"] == "HDF5 Biom":
            return Hdf5BiomDownload(data)
        elif data["attributes"]["file-format"]["name"] == "JSON Biom":
            return JsonBiomDownload(data)
        else:
            return Download(data)

    def file_format(self) -> str:
        return self.data["attributes"]["file-format"]["name"]

    def group_type(self) -> str:
        return self.data["attributes"]["group-type"]

    def url(self) -> str:
        return self.data["links"]["self"]

    def __str__(self):
        return f"{self.__class__.__name__} {self.file_format()} {self.group_type()} {self.data['links']['self']}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.file_format()} {self.group_type()} {self.data['links']['self']}>"


class TsvDownload(Download):

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.group_type()} {self.data['links']['self']}>"


class Hdf5BiomDownload(Download):

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.group_type()} {self.data['links']['self']}>"


class JsonBiomDownload(Download):

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.group_type()} {self.data['links']['self']}>"


class FastaDownload(Download):

    def read(self) -> FastaFile:
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
        return f"<{self.__class__.__name__} {self.group_type()} {self.data['links']['self']}>"
