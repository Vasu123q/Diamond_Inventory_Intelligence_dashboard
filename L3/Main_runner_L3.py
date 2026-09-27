import subprocess
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
from pathlib import Path

project_root = Path(__file__).resolve().parent

scripts = [
    
    project_root/'1_dATA_LEVELS_ADD_L3.py',
    project_root/'2_mapping_&_hidden_space_removal_L3.py',
    project_root/'3_size_range_add_L3.py',
    project_root/'4_grouping_sales.py',
    project_root/'5_merging_sales_avg_sales_day_L3.py',
    project_root/'6_age_&_TotalSales_add_L3.py',
    project_root/'7_L3.py',
    project_root/'8_L3.py',
    
]

jupyter_books=[
    project_root/'model_L3.ipynb',
    
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