from mgnifyextract.studies import find_studies, get_study_samples, get_superstudy_studies, get_study
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

runs = samples[0].get_runs(max_results=1)
print(runs)

analyses = runs[0].get_analyses(max_results=1)
print(analyses)

fasta_files = analyses[0].get_fasta_files(max_results=1)
print(fasta_files)

fasta = fasta_files[0].read()
print(fasta.get_reference_length)
print(fasta.references[0])
print(fasta.fetch(fasta.references[0]))


#print(json.dumps(downloads, indent=2))
#analyses.read_fasta_files("MGYA00199483")
