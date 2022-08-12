import unittest
from mgnifyextract.studies import Study, get_study


STUDY_ID = "MGYS00000462"


class TestStudies(unittest.TestCase):

    def test_get_study(self):
        study = get_study(STUDY_ID)
        self.assertIsInstance(study, Study)
        self.assertIsNotNone(study.data)
        self.assertEquals(study.data["id"], STUDY_ID)
