from typing import List
import unittest
from mgnifyextract.samples import Sample
from mgnifyextract.studies import Study, get_study


STUDY_ID = "MGYS00000462"


class TestStudies(unittest.TestCase):

    def test_get_study(self):
        study = get_study(STUDY_ID)
        self.assertIsInstance(study, Study)
        self.assertIsNotNone(study.data)
        self.assertEquals(study.data["id"], STUDY_ID)

    def test_get_samples(self):
        study = get_study(STUDY_ID)
        samples = study.get_samples(max_results=2)
        self.assertIsInstance(samples, List)
        self.assertEquals(len(samples), 2)
        self.assertIsInstance(samples[0], Sample)
        self.assertIsNotNone(samples[0].data)
