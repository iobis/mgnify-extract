from typing import List
import unittest
from mgnifyextract.runs import Run
from mgnifyextract.samples import Sample
from mgnifyextract.studies import get_study


STUDY_ID = "MGYS00000462"


class TestRuns(unittest.TestCase):

    def test_get_runs(self):
        study = get_study(STUDY_ID)
        samples = study.get_samples(max_results=2)
        runs = samples[0].get_runs(max_results=2)
        self.assertIsInstance(samples, List)
        self.assertEquals(len(samples), 2)
        self.assertIsInstance(samples[0], Sample)
        self.assertIsNotNone(samples[0].data)
        self.assertIsInstance(runs, List)
        self.assertEquals(len(runs), 2)
        self.assertIsInstance(runs[0], Run)
        self.assertIsNotNone(runs[0].data)
