from mgnifyextract.downloads import Download, FastaDownload, MseqDownload
from mgnifyextract.studies import Study
import pandas as pd
from mgnifyextract.util import clean_taxonomy_string
from mgnifyextract.silva import get_silva_otus
import logging


logger = logging.getLogger(__name__)


def downloads_to_sequence_table(downloads: list[Download], marker: str) -> pd.DataFrame:
    fasta_files = [download for download in downloads if isinstance(download, FastaDownload) and download.marker == marker]
    mseq_files = [download for download in downloads if isinstance(download, MseqDownload) and download.marker == marker]
    assert len(fasta_files) == 1 and len(mseq_files) == 1

    fasta = fasta_files[0].read_pandas()
    mseq = mseq_files[0].read()

    df = fasta.merge(
        mseq
        .filter(items=["#query", "dbhit", "bitscore", "identity", "SILVA"])
        .rename({"#query": "reference"}, axis=1), how="left", on="reference"
    )
    return df


def translate_rank(input):
    ranks = {
        "sk": "superkingdom",
        "k": "kingdom",
        "p": "phylum",
        "c": "class",
        "o": "order",
        "f": "family",
        "g": "genus",
        "s": "species",
        "t": "strain"
    }
    return ranks[input]


def split_taxonomy_column(taxonomy):
    items = [part.split("__") for part in taxonomy.split(";")]
    ranks = [(translate_rank(item[0]), item[1]) for item in items]
    if len(ranks) > 0:
        scientificname = ("scientificName", ranks[-1][1])
        ranks.append(scientificname)
    return dict(ranks)


def study_to_dwc(study: Study, max_samples: int = None, markers: list[str] = ["LSU", "SSU"]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate Darwin Core tables for study."""
    occ_frames = []
    dna_frames = []

    samples = study.get_samples(max_results=max_samples)
    for i, sample in enumerate(samples):

        logger.info(f"Processing sample {i + 1} of {len(samples)}")

        # event fields

        event_fields = {
            "eventID": sample.data["attributes"]["biosample"],
            "decimalLongitude": sample.data["attributes"]["longitude"],
            "decimalLatitude": sample.data["attributes"]["latitude"],
            "eventDate": sample.data["attributes"]["collection-date"],
            "eventRemarks": sample.data["attributes"]["sample-desc"],
            "minimumDepthInMeters": None,
            "maximumDepthInMeters": None
        }

        # depth

        sample_metadata = sample.data["attributes"]["sample-metadata"]
        depth_items = [m for m in sample_metadata if m["key"] == "depth"]
        if len(depth_items) == 1:
            event_fields["minimumDepthInMeters"] = depth_items[0]["value"]
            event_fields["maximumDepthInMeters"] = depth_items[0]["value"]

        # dna and occurrences

        runs = sample.get_runs(max_results=None)
        for run in runs:
            analyses = run.get_analyses(max_results=None)
            for analysis in analyses:

                downloads = analysis.get_downloads()
                frames = [downloads_to_sequence_table(downloads, marker) for marker in markers]
                sequences = pd.concat(frames)

                dna = sequences.filter(["SILVA", "sequence", "dbhit"]) \
                    .rename({"SILVA": "taxonomy", "sequence": "DNA_sequence"}, axis=1)
                dna["taxonomy"] = dna["taxonomy"].apply(clean_taxonomy_string)
                dna.dropna(inplace=True)
                dna["temp"] = dna.groupby(["dbhit"])["taxonomy"].transform(lambda x: pd.factorize(x)[0]).astype(str)
                dna["occurrenceID"] = dna.apply(lambda x: "%s_%s_%s" % (event_fields["eventID"], x["dbhit"], x["temp"]), axis=1)

                occ = dna.groupby(["occurrenceID", "taxonomy"]).size().reset_index(name="organismQuantity")
                otus = get_silva_otus()
                occ = occ.merge(otus, how="left", on="taxonomy")
                occ = occ.join(pd.DataFrame(occ["taxonomy"].apply(split_taxonomy_column).values.tolist()))

                dna = dna.filter(["occurrenceID", "DNA_sequence"])
                dna = dna.groupby(["occurrenceID"]).nth(0).reset_index()
                dna["ref_db"] = "SILVA"

                for key, value in event_fields.items():
                    occ[key] = value

                occ_frames.append(occ)
                dna_frames.append(dna)

    occ = pd.concat(occ_frames)
    dna = pd.concat(dna_frames)

    return occ, dna
