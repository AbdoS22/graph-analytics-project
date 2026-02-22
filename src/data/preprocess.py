from __future__ import annotations

import gzip
from pathlib import Path
import pandas as pd


def read_ca_hepth_edges(gz_path: Path) -> pd.DataFrame:
    # SNAP format: each line "u v", comments start with '#'
    edges = []
    with gzip.open(gz_path, "rt", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            u, v = line.split()
            u, v = int(u), int(v)
            if u == v:
                continue
            # undirected: store (min,max) to avoid duplicates
            a, b = (u, v) if u < v else (v, u)
            edges.append((a, b))

    df = pd.DataFrame(edges, columns=["u", "v"]).drop_duplicates()
    return df


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    raw_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    gz_path = raw_dir / "ca-HepTh.txt.gz"
    out_csv = processed_dir / "edges.csv"

    df = read_ca_hepth_edges(gz_path)
    df.to_csv(out_csv, index=False)
    print(f"Saved {len(df):,} edges to {out_csv}")


if __name__ == "__main__":
    main()
