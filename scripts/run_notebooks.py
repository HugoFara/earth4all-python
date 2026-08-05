"""Run the notebooks of `examples/` and save them with their figures in place.

    python scripts/run_notebooks.py

A notebook is worth reading before it is worth running, so the ones in this
repository are stored with their output. Run this after a change to the model,
so that what they show is what the code now does.

It needs a kernel: `pip install -e ".[notebook]"`.
"""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "notebooks", nargs="*", type=Path,
        help="the notebooks to run; all of examples/ by default",
    )
    parser.add_argument("--timeout", type=int, default=600, help="seconds per cell")
    args = parser.parse_args()

    import nbformat
    from nbclient import NotebookClient

    examples = Path(__file__).parent.parent / "examples"
    notebooks = args.notebooks or sorted(examples.glob("*.ipynb"))

    for path in notebooks:
        notebook = nbformat.read(path, as_version=4)
        client = NotebookClient(
            notebook, timeout=args.timeout, kernel_name="python3",
            resources={"metadata": {"path": str(path.parent)}},
        )
        client.execute()
        nbformat.write(notebook, path)
        cells = sum(1 for cell in notebook.cells if cell.cell_type == "code")
        print(f"ran {path} ({cells} code cells)")


if __name__ == "__main__":
    main()
