from collections import UserDict
import logging


logger = logging.getLogger(__name__)


class Download(UserDict):

    def __str__(self):
        return f"Download https://www.ebi.ac.uk/metagenomics/downloads/{self.data['id']}"

    def __repr__(self):
        return f"<Download https://www.ebi.ac.uk/metagenomics/downloads/{self.data['id']}>"