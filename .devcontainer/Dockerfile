FROM osgeo/gdal:ubuntu-small-3.2.1

RUN apt update && apt install -y python3-pip python3-distutils git

RUN adduser --disabled-password --gecos '' vscode

USER vscode

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

ENV PATH="~/.poetry/bin:$PATH"

ENV PATH="~/.local/bin:$PATH"