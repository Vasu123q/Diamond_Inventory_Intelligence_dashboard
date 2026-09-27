import subprocess
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
from pathlib import Path
project_root = Path(__file__).resolve().parent

scripts = [
    project_root/'L1'/'Main_runner_L1.py',
    project_root/'L2'/'Main_runner_L2.py',
    project_root/'L3'/'Main_runner_L3.py',
    project_root/'Inventory_summary_table.py',
    project_root/'Concater.py',    
]
for script in scripts:
    print(f"Running {script}...")
    subprocess.run(["python", script], check=True)

