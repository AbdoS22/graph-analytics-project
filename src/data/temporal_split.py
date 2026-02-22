from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx


def build_graph(edges: pd.DataFrame) -> nx.Graph:
    G = nx.Graph()
    G.add_edges_from(edges[["u", "v"]].itertuples(index=False, name=None))
    return G


def compute_core_nodes(train_edges: pd.DataFrame, test_edges: pd.DataFrame,
                       k_train: int = 2, k_test: int = 1) -> set[int]:
    Gtr = build_graph(train_edges)
    Gte = build_graph(test_edges)

    deg_tr = dict(Gtr.degree())
    deg_te = dict(Gte.degree())

    nodes = set(Gtr.nodes()) | set(Gte.nodes())
    core = {n for n in nodes if deg_tr.get(n, 0) >= k_train and deg_te.get(n, 0) >= k_test}
    return core


def main(seed: int = 42, test_frac: float = 0.2, k_train: int = 2, k_test: int = 1) -> None:
    project_root = Path(__file__).resolve().parents[2]
    processed_dir = project_root / "data" / "processed"

    edges_path = processed_dir / "edges.csv"
    df = pd.read_csv(edges_path)

    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(df))
    n_test = int(round(test_frac * len(df)))

    test_idx = perm[:n_test]
    train_idx = perm[n_test:]

    train_edges = df.iloc[train_idx].copy()
    test_edges = df.iloc[test_idx].copy()

    # Core restriction (Lecture 3)
    core = compute_core_nodes(train_edges, test_edges, k_train=k_train, k_test=k_test)

    # Keep only test edges inside Core×Core (E_new* in the lecture)
    test_core = test_edges[(test_edges["u"].isin(core)) & (test_edges["v"].isin(core))].copy()

    train_out = processed_dir / "train_edges.csv"
    test_out = processed_dir / "test_edges.csv"
    core_out = processed_dir / "core_nodes.txt"

    train_edges.to_csv(train_out, index=False)
    test_core.to_csv(test_out, index=False)
    core_out.write_text("\n".join(map(str, sorted(core))), encoding="utf-8")

    print(f"Train edges: {len(train_edges):,}")
    print(f"Test edges (core-filtered): {len(test_core):,}")
    print(f"Core nodes: {len(core):,}")
    print(f"Saved: {train_out}, {test_out}, {core_out}")


if __name__ == "__main__":
    main()
