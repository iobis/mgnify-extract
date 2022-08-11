from turtle import down
from mgnifyextract import analyses
from mgnifyextract.studies import find_studies, get_study_samples, get_superstudy_studies, get_study
from mgnifyextract.samples import get_sample_runs
from mgnifyextract.runs import get_run_analyses
from mgnifyextract.analyses import get_analysis_downloads
import logging
import json


logging_level = logging.INFO
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


study_id = "MGYS00000462"

study = get_study(study_id)
print(study)

samples = study.get_samples(max_results=2)
print(samples)

runs = samples[0].get_runs()
print(runs)

analyses = runs[0].get_analyses()
print(analyses)

downloads = analyses[0].get_downloads()
print(downloads)

#print(json.dumps(downloads, indent=2))
#analyses.read_fasta_files("MGYA00199483")
