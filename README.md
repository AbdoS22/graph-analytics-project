# Temporal Link Prediction in a Real Collaboration Network
**From Heuristics and Communities to Node Embeddings**

Course project for **Graph Analytics and Applications** (final-year engineering project)

## Team
- **NAHLI Ghita**
- **RAMDANI Nabil**
- **SALEHI Abderrahmane**

---

## Project Overview

This project studies **temporal (pseudo-temporal) link prediction** on a real-world scientific collaboration network, using the SNAP **ca-HepTh** co-authorship graph.

Given an observed graph (train split), the goal is to predict which new edges (future collaborations) appear in a held-out test split.

The project integrates concepts from the course:
- Graph properties and models (degree distribution, clustering, distances, GCC)
- Random / generative graph models (ER, BA, configuration model)
- Classical link prediction methods (CN, Jaccard, Adamic–Adar, Preferential Attachment)
- Path-based and random-walk methods (truncated Katz, rooted / personalized PageRank)
- Community detection and modularity (Louvain)
- Graph representation learning (node2vec embeddings)

The implementation is designed to run on a **standard CPU-only personal computer**.

---

## Dataset

We use the public SNAP dataset:

- **ca-HepTh (High Energy Physics Theory collaboration network)**

Interpretation:
- **Nodes** = authors
- **Undirected edges** = co-authorship relations

Raw dataset file in this repository:
- `data/raw/ca-HepTh.txt.gz`

---

## Repository Structure

```text
graph-analytics-final-project/
├── .venv/                         # Local virtual environment (not tracked)
├── data/
│   ├── raw/                       # Raw dataset (SNAP edge list)
│   │   └── ca-HepTh.txt.gz
│   └── processed/                 # Processed outputs (train/test/core)
│
├── notebooks/
│   ├── graph_stats.ipynb          # Structural analysis + null-model comparison
│   ├── link_prediction_baselines.ipynb
│   │                              # Heuristics + Katz + rooted PageRank
│   ├── communities.ipynb          # Louvain + community-aware LP features
│   └── embeddings.ipynb           # node2vec-based LP experiments
│
├── results/                       # Saved figures, result tables, CSVs
│
├── src/
│   ├── __init__.py
│   ├── config.py                  # (Optional) project paths/settings
│   └── data/
│       ├── __init__.py
│       ├── download_snap.py       # Download SNAP file
│       ├── preprocess.py          # Parse/clean graph edges
│       └── temporal_split.py      # Train/test split + core filtering
│
├── .gitignore
├── README.md
└── requirements.txt
```


## How to Run (Suggested Order)
1) Create and activate a virtual environment (Windows PowerShell)

python -m venv .venv
.venv\Scripts\Activate.ps1

2) Install dependencies

pip install -r requirements.txt

3) Prepare the data (scripts)

Run the data pipeline scripts from the project root:

python -m src.data.download_snap
python -m src.data.preprocess
python -m src.data.temporal_split

4) Open and run notebooks (in this exact order)

Open the project in VS Code and run the notebooks sequentially:

notebooks/graph_stats.ipynb

notebooks/link_prediction_baselines.ipynb

notebooks/communities.ipynb

notebooks/embeddings.ipynb

This order matters because later notebooks reuse ideas/outputs from earlier ones.

# What Each Notebook Does : 

1) graph_stats.ipynb

Goal: Characterize the graph structure before link prediction.

Main tasks:

Load train graph and compute connected components

Extract the giant connected component (GCC)

Compute graph statistics:

number of nodes/edges

average degree

clustering coefficient

shortest-path statistics (approximate average path length)

effective diameter / sampled diameter

Plot degree distribution (including log-log plots)

Build and compare null/generative models:

Erdős–Rényi (ER)

Barabási–Albert (BA)

Configuration model

Compare real graph vs null models (especially clustering and degree shape)

Why it matters: explains why some link prediction methods perform better than others.

2) link_prediction_baselines.ipynb

Goal: Evaluate classical link prediction baselines on a realistic candidate set.

Main tasks:

Build the core-restricted graph

Generate 2-hop candidate non-edges (friends-of-friends)

Compute candidate coverage (fraction of future edges inside candidate set)

Compute and evaluate classical scores:

Common Neighbors (CN)

Jaccard

Adamic–Adar (AA)

Preferential Attachment (PA)

Add stronger methods:

truncated Katz

rooted / personalized PageRank (PPR)

Evaluate all methods with:

Top-n accuracy (n = number of future edges)

Improvement over random baseline

Optional normalized performance by coverage

Produce comparison plots (bar charts)

Why it matters: establishes strong, interpretable baselines and runtime/performance trade-offs.

3) communities.ipynb

Goal: Test whether community structure improves link prediction.

Main tasks:

Run Louvain community detection on the core graph

Compute:

number of communities

modularity 
𝑄
Q

community size distribution (rank plot)

Add community-based features to candidate pairs:

same community indicator

community size statistics

Evaluate:

community-only score

community-aware combined score (e.g., AA + same-community bonus)

Compare community-enhanced scores to AA baseline

Why it matters: shows that mesoscale graph structure can provide complementary predictive signal.

4) embeddings.ipynb

Goal: Use graph representation learning (node2vec) for link prediction.

Main tasks:

Train node2vec embeddings on the core graph

Score candidate edges using embedding similarity:

dot product

cosine similarity

Compare embedding-based scores against strong baselines (e.g., AA)

Run a small node2vec parameter sensitivity study (q sweep)

Produce embedding comparison and parameter-sweep plots

Why it matters: adds a modern graph ML method and connects the project to representation learning.