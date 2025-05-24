
# 📚 Property Graphs – SDM Lab Project

Authors: *Alícia Chimeno Sarabia & Marc Fortó Cornellà*  
Date: April 10, 2024

## 🧠 Overview

This project explores the modeling, construction, querying, and analysis of a scholarly publication graph using **Neo4j** and **graph data science algorithms**. The data, primarily sourced from [DBLP](https://dblp.uni-trier.de), is preprocessed, structured, and evolved to support complex queries and recommendations in a research context.

---

## 🧱 Graph Design

The core of the graph is the **Paper** node, which links to various other entities:

- `Author` (via `writes`, includes `main_author`)
- `Reviewer` (via `reviews`)
- `Citations` (via `cites`)
- `Keyword` → `Topic`
- `Conference`, `Journal`, `Edition`, and `Volume`

Extended with:
- `Affiliation` nodes for authors
- `Review` edges with `content` and `decision` (boolean `approves`)

Graph evolution scripts are included to reflect these changes.

---

## ⚙️ Data Pipeline

1. **Source**: DBLP XML files.
2. **Conversion**: [dblp-to-csv tool](https://github.com/ThomHurks/dblp-to-csv).
3. **Preprocessing**: 
   - Done using `R` (see `markdownsmd.Rmd`)
   - Keyword extraction with NLP in `get_keywords.ipynb` (using `NLTK`, `sentence-transformers`).
4. **Loading**: CSV imports into Neo4j.

---

## 🔍 Queries Implemented

1. **Top 3 Most Cited Papers per Conference**
2. **Conference Communities** (authors with 4+ publications across editions)
3. **Journal Impact Factor**
4. **Author H-index**

All queries are written in Cypher and stored in the project scripts.

---

## 🤖 Reviewer Recommender System

Implemented a 4-stage recommendation pipeline:

1. **Community Definition** (based on keywords)
2. **Match Journals & Conferences to Communities**
3. **Rank Top-100 Cited Papers** per community
4. **Identify Gurus** (authors of 2+ top papers)

---

## 📈 Graph Algorithms

Utilized the **Neo4j Graph Data Science library**:

- **PageRank**: To identify influential papers based on citation graph.
- **Node Similarity**: To identify close co-author relationships.

---

## 📂 Structure

```bash
.
├── PartA.3_ChimenoFortó.py         # Graph evolution scripts
├── PartC_ChimenoFortó.py           # Recommender system queries
├── markdownsmd.Rmd                 # Data preprocessing in R
├── get_keywords.ipynb              # NLP keyword extraction
├── CSV datasets/                   # Nodes and edges data
└── README.md
```

---

## 🔗 References

- 📘 [DBLP](https://dblp.uni-trier.de)
- 🔄 [dblp-to-csv](https://github.com/ThomHurks/dblp-to-csv)
- 📊 [Neo4j Graph Algorithms](https://neo4j.com/docs/graph-data-science/current/)

---

## 💡 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/marcforto14/PropertyGraphs_SDM
   ```
2. Start a Neo4j instance with GDS plugin.
3. Import CSV data.
4. Run scripts `PartA.3_ChimenoFortó.py` and `PartC_ChimenoFortó.py` via Neo4j Browser or API.
