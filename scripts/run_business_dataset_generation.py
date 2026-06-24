from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.synthesis.generate_business_datasets import configure_logging, run_business_dataset_generation


def main() -> None:
    configure_logging()
    run_business_dataset_generation()


if __name__ == "__main__":
    main()
