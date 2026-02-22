from __future__ import annotations

import os
import zipfile
from pathlib import Path
import requests


CA_HEPTH_URL = "https://snap.stanford.edu/data/ca-HepTh.txt.gz"


def download_file(url: str, out_path: Path, chunk_size: int = 1 << 20) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        return

    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]  # src/.. -> project root
    raw_dir = project_root / "data" / "raw"
    gz_path = raw_dir / "ca-HepTh.txt.gz"

    print(f"Downloading to: {gz_path}")
    download_file(CA_HEPTH_URL, gz_path)
    print("Done.")


if __name__ == "__main__":
    main()
