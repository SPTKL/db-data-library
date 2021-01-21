# db-data-library

## Instructions:
1. Make sure you have GDAL installed (we are using version `2.4.0+dfsg-1+b1`)
```bash
sudo apt install -y gdal-bin libgdal-dev python3-gdal
```
2. then install poetry 
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
3. Use poetry to install dependencies `poetry install`
3. Check out what's available via the cli `poetry run library --help`