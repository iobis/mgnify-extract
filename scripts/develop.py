from mgnifyextract.studies import find_studies, get_study_samples, get_superstudy_studies, get_study
from mgnifyextract.samples import get_sample_runs
from mgnifyextract.runs import get_run_analyses
from mgnifyextract.analyses import get_analysis_downloads
import logging
import json


logging_level = logging.DEBUG
logging_fmt = "%(asctime)s - %(levelname)5.5s - %(name)10.10s - %(message)s"
date_fmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging_level, format=logging_fmt, datefmt=date_fmt)
logging.getLogger("urllib3").setLevel(logging.INFO)


#filters = {
#    "lineage": "root:Environmental:Aquatic:Marine",
#    "search": "Tara"
#}
#studies = find_studies(filters, max_results=1)


#studies = get_superstudy_studies("atlanteco")


study = get_study("MGYS00000462")
print(json.dumps(study, indent=2))
#samples = get_study_samples("MGYS00000462", max_results=2)
#print(json.dumps(samples, indent=2))
#runs = get_sample_runs(samples[0]["id"])
#analyses = get_run_analyses(runs[0]["id"])
#downloads = get_analysis_downloads(analyses[0]["id"])
#print(json.dumps(downloads, indent=2))
