# Connect4

## Installation
Create a dedicated Python 3.9 environment, for instance, using conda:
````
conda create -n connect4 python=3.9
conda activate connect4
````
**For users:** install the connect4 package
````
cd /path/to/package
pip install .
````
**For developers:** install the test framework and the pre-commit hooks
````
pip install -e ".[dev]"
pre-commit install
````

## Quick start

### Human VS Human
````
python scripts/connect4_human_vs_human.py
````

### Human VS (dummy) AI
````
python scripts/connect4_dummy_vs_human.py
````
