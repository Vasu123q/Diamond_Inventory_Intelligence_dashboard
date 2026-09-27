import subprocess
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
from pathlib import Path

project_root = Path(__file__).resolve().parent

scripts = [
    project_root / "1_mapping_&_hidden_space_removal.py",
    project_root / "2_size_range_add.py",
    project_root / "3_grouping_sales.py",
    project_root / "4_merging_sales_avg_sales_day.py",
    project_root / "5_age_&_TotalSales_add.py",
    project_root / "6_.py",
    project_root / "7.py",
    
]

jupyter_books=[
    project_root / "model.ipynb",
    
]

for script in scripts:
    print(f"Running {script}...")
    subprocess.run(["python", script], check=True)

for notebook in jupyter_books:
    print(f"Running {notebook}...")
    subprocess.run([
        "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        notebook
    ], check=True)