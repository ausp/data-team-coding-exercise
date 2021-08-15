# Load/transform/write files (Pandas)

### Prerequisites

#### Python 3.6.* or later.

See installation instructions at: https://www.python.org/downloads/

Check installation:

```bash
python3 --version
```

#### Installing Python requirements

```bash
pip3 install -r ./requirements.txt
```

#### Running tests

```bash
python -m pytest ./test
```

### Running solution

Run the below from the repository's root directory.

```bash
# Basic run:
python ./src/solution.py

# Default arguments:
python ./src/solution.py --components_location=./data/input/components.csv --orders_location=./data/input/orders.json.txt --output_location=./data/output/order_volume.txt
```

The output of this program will be placed in the filepath given in `--output_location`.

Any pushes to `main` will be checked (and possibly corrected) by `./.github/workflows/ci.yaml`.
