# asyncspinner
Little graphic to show user that something is waited for when a progress bar is overkill, or the progress is unknown.

## Installation

```bash
pip install asyncspinner
```

## Usage
```
from asyncspinner import Spinner

async with Spinner('Connecting'):
    # some code that does something that requires waiting, e.g. connecting to a database
    await my_slow_thing()
```

## Demo
```bash
python -m asyncspinner
```
