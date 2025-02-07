## Installation

```python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

From [py-bitcoinkernel](https://pypi.org/project/py-bitcoinkernel/) documentation:

* Bitcoin Core requires exclusive access to its data directory. If you want to use py-bitcoinkernel with an existing chainstate, you'll need to either first shut down Bitcoin Core, or clone the blocks/ and chainstate/ directories to a new location.

Simply launch `./scan-for-coinjoins.py`. As always with venv projects, make sure you have executed `source .venv/bin/activate` first.
