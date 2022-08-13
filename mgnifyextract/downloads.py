from collections import UserDict
import logging
from pysam import FastaFile
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
import gzip
from mgnifyextract.util import download_file


logger = logging.getLogger(__name__)


class Download(UserDict):

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

    def file_format(self) -> str:
        return self.data["attributes"]["file-format"]["name"]

    def url(self) -> str:
        return self.data["links"]["self"]

    def __str__(self):
        return f"Download {self.data['links']['self']}"

    def __repr__(self):
        return f"<Download {self.data['links']['self']}>"
