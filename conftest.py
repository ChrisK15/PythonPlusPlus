import sys
from pathlib import Path

# Adds src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))