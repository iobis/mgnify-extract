# mgnify-extract

This library extracts Darwin Core datasets from MGnify.

## Run scripts

```
PYTHONPATH=. python scripts/develop.py
```

## Run module

```
python -m mgnifyextract
```

## Examples

```python
filters = {
    "lineage": "root:Environmental:Aquatic:Marine",
    "search": "Tara"
}
studies = find_studies(filters, max_results=1)
```

```python
studies = get_superstudy_studies("atlanteco")
samples = get_study_samples(studies[0]["id"])
runs = get_sample_runs(samples[0]["id"])
analyses = get_run_analyses(runs[0]["id"])
downloads = get_analysis_downloads(analyses[0]["id"])
```
