# mgnify-extract

This library extracts Darwin Core datasets from MGnify.

## Usage

Find studies:

```python
filters = {
    "lineage": "root:Environmental:Aquatic:Marine",
    "search": "Tara"
}
studies = find_studies(filters, max_results=1)
```

Fetching samples, runs, analyses, and downloads:

```python
study = get_study("MGYS00000462")
samples = study.get_samples()
runs = samples[0].get_runs()
analyses = runs[0].get_analyses()
downloads = analyses[0].get_downloads()
```

Generating Darwin Core tables:

```python
study = get_superstudy_studies("atlanteco")[0]
occ, dna = study_to_dwc(study)
```

## Run scripts

```
PYTHONPATH=. python scripts/develop.py
```

## Run module

```
python -m mgnifyextract
```
