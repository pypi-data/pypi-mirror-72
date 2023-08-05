# fsATC Kermout Strips API ![PyPI](https://img.shields.io/pypi/v/kermout-strips-api) ![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![License](https://img.shields.io/badge/license-MIT-red) ![Python version](https://img.shields.io/badge/Python-latest-blue)

Used to interact with Kermout's fsATC Strips System remotely. Here it is on [PyPI](https://pypi.org/project/kermout-strips-api/)!.

![Getting the plan](.media/plan.gif)

## How do I get it?

Install using pip or check out the release page!

```python
pip install kermout-strips-api
```

Check out the tests for an example of how it works!

## Typical usage

```python
from kermout_strips_api import Plan

plan = {
    'Callsign': 'UAL256',
    'Aircraft': 'B737',
    'Flight_Rules': 'IFR',
    'Departure': 'KSAN',
    'Arrival': 'KJFK',
    'Altitude': '5000',
    'Routes': 'DCT GPS',
    'remarks': 'bout to go vertical',
}

s = Plan(plan)

s.filePlan()
s.startLoop()

inp = input("Stop?\n")
print("")

s.stopLoop()

s.deletePlan()
```
