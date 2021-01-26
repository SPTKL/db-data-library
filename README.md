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
3. Run `source $HOME/.poetry/env`
4. Use poetry to install dependencies `poetry install`
5. Install pre-commit `poetry run pre-commit install`
6. Check out what's available via the cli `poetry run library --help`
7. To add/update documentation, run `poetry run pdoc -o docs --html library`
