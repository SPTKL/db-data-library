FROM osgeo/gdal:ubuntu-small-3.6.1

COPY . /library/

WORKDIR /library/

RUN apt update && apt install -y python3-pip python3-distutils

RUNcurl -sSL https://install.python-poetry.org | python3 -

RUN . $HOME/.local/bin &&\
    poetry config virtualenvs.create false --local &&\
    poetry install --no-dev
