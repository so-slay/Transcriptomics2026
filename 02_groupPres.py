"""
Objectives: 
1. Fetch the protein sequences for our genes of interest
2. Run a BLAST on these sequences in the TARA Oceans Atlas

"""

import requests
import time
import sys
import platform

### Section 1

# Define the Base URL for the Candida Genome Database
BASE = "https://www.candidagenome.org/api/locus/{}/sequence_details"

# List of Gene IDs that interest us
GENE_IDS = [
"CPAR2_404850",
"CPAR2_304060",
"CPAR2_211810",
"CPAR2_201490",
"CPAR2_109780",
"CPAR2_103400",
"CPAR2_701390",
"CPAR2_301300",
"CPAR2_602950",
"CPAR2_106140",
"CPAR2_210700",
"CPAR2_209460",
"CPAR2_400570",
"CPAR2_405780",
"CPAR2_405900",
"CPAR2_301400",
"CPAR2_100710",
"CPAR2_100830",
"CPAR2_405010",
"CPAR2_401550",
"CPAR2_109010",
"CPAR2_402940",
"CPAR2_402640",
"CPAR2_108280",
"CPAR2_406210",
"CPAR2_303740",
"CPAR2_603610",
"CPAR2_106960",
"CPAR2_203450",
"CPAR2_500850",
"CPAR2_804060",
"CPAR2_108000",

    ]

# Fetch the sequences from the Candida Genome Database using an API
def fetch_cgd_protein(gene_id):
    r = requests.get(BASE.format(gene_id), timeout=15)
    if r.status_code != 200:
        print(f"  [!] {gene_id}: HTTP {r.status_code}")
        return None
    data = r.json()
    results = data.get("results", {})
    if not results:
        print(f"  [!] {gene_id}: no results")
        return None
    organism_data = next(iter(results.values()))  
    for seq in organism_data.get("sequences", []):
        if seq.get("seq_type") == "protein": # change to "genomic" of genome is needed
            return seq["residues"].rstrip("*")
    print(f"  [!] {gene_id}: no protein sequence found")
    return None

protein_seqs = {}
for gid in GENE_IDS:
    seq = fetch_cgd_protein(gid)
    if seq:
        protein_seqs[gid] = seq
        print(f"  {gid}: {len(seq)} aa")
    time.sleep(0.5)  # Wait timer to reduce load on the CGD server
print(f"\nFetched {len(protein_seqs)} / {len(GENE_IDS)} sequences")

with open("32-candida_proteins_10092026.fasta", "w") as f:
    for gene_id, seq in protein_seqs.items():
        f.write(f">{gene_id}\n{seq}\n")

print(f"Wrote {len(protein_seqs)} sequences to candida_proteins.fasta")


# Code generated with Claude ai, reviewed by Ananthakrishna S V

# Reproducibility section:
print("Python:", sys.version)
print("Platform:", platform.platform())
print("requests:", requests.__version__)


'''
references:
Candida Genome Database:
Lew-Smith J, Binkley J, Sherlock G (2025). The Candida Genome Database: annotation and visualization updates. Genetics, Volume 229, Issue 3, March 2025

TARA Oceans citations:
The Ocean Gene Atlas v2.0: online exploration of the biogeography and phylogeny of plankton genes. C. Vernette, J. Lecubin, P. Sanchez, Tara Oceans Coordinators, S. Sunagawa, T.O. Delmont, S.G. Acinas, E. Pelletier, P. Hingamp, M. Lescot. (2022) Nucleic Acides Research.
Link to paper: doi: 10.1093/nar/gkac420
The Ocean Gene Atlas: exploring the biogeography of plankton genes online. E. Villar, T. Vannier, C. Vernette, M. Lescot, M. Cuenca, A. Alexandre, P. Bachelerie, T. Rosnet, E. Pelletier, S. Sunagawa, P. Hingamp. (2018) Nucleic Acids Research.
Link to paper: doi: 10.1093/nar/gky376
'''
