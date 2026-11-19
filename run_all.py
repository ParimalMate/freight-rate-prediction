"""Run freight_rate_model.ipynb end to end, in place.

Produces validation_predictions.csv, december-chart-predictions.csv and
scorer_results/candidate_december.png (the notebook runs score.py itself).

Usage:  python run_all.py
"""
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

NOTEBOOK = Path(__file__).with_name("freight_rate_model.ipynb")


def main() -> None:
    nb = nbformat.read(NOTEBOOK, as_version=4)
    start = time.time()
    print(f"Running {NOTEBOOK.name} with {sys.executable} (about 15 minutes on a laptop CPU)...", flush=True)
    client = NotebookClient(nb, timeout=3600, kernel_name="python3",
                            resources={"metadata": {"path": str(NOTEBOOK.parent)}})
    try:
        client.execute()
    finally:
        nbformat.write(nb, NOTEBOOK)
    print(f"Done in {(time.time() - start) / 60:.1f} min. Outputs saved in the notebook.")
    for name in ("validation_predictions.csv", "december-chart-predictions.csv", "scorer_results/candidate_december.png"):
        print(f"  {'ok ' if (NOTEBOOK.parent / name).exists() else 'MISSING'} {name}")


if __name__ == "__main__":
    main()
