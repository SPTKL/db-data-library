# db-data-library

## Instructions:
1. Make sure you have GDAL installed (we are using version `2.4.0+dfsg-1+b1`)
```bash
sudo apt install -y gdal-bin libgdal-dev python3-gdal
```
2. then install poetry
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
```
3. Use poetry to install dependencies `poetry install`
4. Install pre-commit `poetry run pre-commit install`
5. Check out what's available via the cli `poetry run library --help`
6. To add/update documentation, run `poetry run pdoc -o docs --html library`

## Testing:

To test all functions within a script:
`poetry run pytest tests/{test script}.py -s`

To test a specific function:
`poetry run pytest tests/{test script}.py::{test name} -s`
> note the `-s` flag is optional, it allows print output (via stdout) to be included in the test output, otherwise it is ignored
