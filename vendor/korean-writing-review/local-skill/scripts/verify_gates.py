#!/usr/bin/env python3
"""Local vendor launcher; never installs into a global skill folder."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[2] / "upstream" / "scripts" / Path(__file__).name), run_name="__main__")
