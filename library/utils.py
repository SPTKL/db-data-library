from urllib.parse import urlparse

def parse_engine(url: str) -> str:
    """
    url: postgres connection string
    e.g. postgresql://username:password@host:port/database
    """
    result = urlparse(url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    portnum = result.port
    return f"PG:host={hostname} port={portnum} user={username} dbname={database} password={password}"


def format_url(url: str) -> str:
    """
    Adds "vsis3" if [url] is from s3
    - s3://edm-recipes/recipes.csv

    Adds "vsizip" to [url] if [url] is zipped.
    - abcd.zip/abcd.shp
    - abcd.zip/abcd.csv
    - etc

    Adds "vsicurl" if [url] contains http
    - https://rawgithubcontent.come/somerepo/somefile.csv
    """
    if "http" in url and ".zip" not in url:
        return "vsicul/" + url
    if ".zip" in url:
        if "http" in url:
            url = "/vsizip/vsicurl/" + url
        elif "s3://" in url:
            url = "/vsizip/vsis3/" + url.replace("s3://", "")
        else:
            url = "/vsizip/" + url
        return url
    if "s3://" in url and ".zip" not in url:
        return url.replace("s3://", "/vsis3/")