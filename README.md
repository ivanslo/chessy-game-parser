## How To Setup

```
pythom -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## How To Convert a PGN File

```
python src/main.py --pgnFile tests/pgnSample.pgn

```

the files `tests/pgnSample_[1|2|3].json` should be present as a result.

## How To Test

```
py.test
```
