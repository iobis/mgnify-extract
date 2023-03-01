# mgnify-extract

This library extracts Darwin Core datasets from MGnify. API documentation at https://iobis.github.io/mgnify-extract.

## Usage

Find studies:

```python
from mgnifyextract.studies import find_studies

filters = {
    "lineage": "root:Environmental:Aquatic:Marine",
    "search": "Tara"
}
studies = find_studies(filters, max_results=1)
```

Fetching samples, runs, analyses, and downloads:

```python
from mgnifyextract.studies import get_study

study = get_study("MGYS00000462")
# <Study https://www.ebi.ac.uk/metagenomics/studies/MGYS00000462>

samples = study.get_samples()
# [<Sample https://www.ebi.ac.uk/metagenomics/samples/ERS667567>, <Sample https://www.ebi.ac.uk/metagenomics/samples/ERS667569>, <Sample https://www.ebi.ac.uk/metagenomics/samples/ERS667570>, ...]

runs = samples[0].get_runs()
# [<Run https://www.ebi.ac.uk/metagenomics/runs/ERR867642>, <Run https://www.ebi.ac.uk/metagenomics/runs/ERR867641>, <Run https://www.ebi.ac.uk/metagenomics/runs/ERR770958>]

analyses = runs[0].get_analyses()
# [<Analysis https://www.ebi.ac.uk/metagenomics/analyses/MGYA00593805>, <Analysis https://www.ebi.ac.uk/metagenomics/analyses/MGYA00135741>]

downloads = analyses[0].get_downloads()
# [<FastaDownload Sequence data https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00593805/file/ERR867642_MERGED_FASTQ.fasta.gz?format=json>, <FastaDownload Taxonomic analysis SSU rRNA https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00593805/file/ERR867642_MERGED_FASTQ_SSU.fasta.gz?format=json>, <MseqDownload Taxonomic analysis SSU rRNA https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00593805/file/ERR867642_MERGED_FASTQ_SSU_MAPSeq.mseq.gz?format=json>, <TsvDownload Taxonomic analysis SSU rRNA https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00593805/file/ERR867642_MERGED_FASTQ_SSU_OTU.tsv?format=json>, <Hdf5BiomDownload Taxonomic analysis SSU rRNA https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00593805/file/ERR867642_MERGED_FASTQ_SSU_OTU_TABLE_HDF5.biom?format=json>, <JsonBiomDownload Taxonomic analysis SSU rRNA https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00593805/file/ERR867642_MERGED_FASTQ_SSU_OTU_TABLE_JSON.biom?format=json>]
```

Generating Darwin Core tables:

```python
from mgnifyextract.studies import get_superstudy_studies
from mgnifyextract.dwc import study_to_dwc

study = get_superstudy_studies("atlanteco")[0]
# <Study https://www.ebi.ac.uk/metagenomics/studies/MGYS00005780>

occ, dna = study_to_dwc(study, markers=["LSU", "SSU"], add_lsid=True)

dna
#                               occurrenceID                                       DNA_sequence ref_db
# 0      SAMN07136738_AACY020004229.3.2803_0  TCTAACCTAGGACCGTAATCCGGTTCGGAGACAGTGTATGGTGGGT...  SILVA
# 1      SAMN07136738_AACY020004229.3.2803_1  GCAAGCGAAGCTCTTGATCGAAGCCCCGGTGAACGGCGGCCGTAAC...  SILVA
# 2      SAMN07136738_AACY020010745.1.2286_0  GTGAGCTGGGTTCAGTACGTCGTGAGACAGTGCGGTCTCTATCCGC...  SILVA
# 3      SAMN07136738_AACY020016991.1.1233_0  AGACAGCCGGCTAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGG...  SILVA
# 4      SAMN07136738_AACY020017460.1.2216_0  TTAGTCGAGAGGGAAACAGCCCAGACCACCAATTAAGGTCCCTAAA...  SILVA
# ...                                    ...                                                ...    ...
# 12162      SAMN07136738_X99077.1111.2593_0  ACCATGGGAGCTGGTCATACCCGATACCGTTAGTCTAACCATTCGG...  SILVA
# 12163         SAMN07136738_Y15288.1.2614_0  GTGAAATCCTGTCTGAACATGGTGGGACCACCCTCCAAGCCTAAGT...  SILVA
# 12164         SAMN07136738_Z19136.1.3497_0  GCTCTGAACGTCAAAGTGATGAAATTCAACCAAGCGCGGGTAAACG...  SILVA
# 12165      SAMN07136738_Z67753.3976.6866_0  CCCAGATCACCAGTTAAGGCCCCAAAATAATTGCTAAGTGATAAAG...  SILVA
# 12166    SAMN07136738_Z67753.47493.50383_0  TTAGTCAAAAGGGAAACAGCCCAGATCACCAGTTAAGGCCCCAAAA...  SILVA
# 
# [12167 rows x 3 columns]
```
