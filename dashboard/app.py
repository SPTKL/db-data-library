import random

import streamlit as st
from src.dataset import Dataset
from src.library import Library
from src.utils import emojis

# Set page configuration
st.set_page_config(
    page_title="Data Library", page_icon="📚", initial_sidebar_state="expanded"
)

# Logo
st.sidebar.markdown(
    """
    <div stule="margin-left: auto; margin-right: auto;">
    <img style='width:40%; margin: 0 auto 2rem auto;display:block;'
        src="https://raw.githubusercontent.com/NYCPlanning/logo/master/dcp_logo_772.png">
    </div>
    """,
    unsafe_allow_html=True,
)

# Initiate library class to get a list of available datasets
library = Library()
datasets = library.datasets

# Set dataset name as query param
query_params = st.experimental_get_query_params()
default = query_params["dataset"][0] if "dataset" in query_params else "doe_lcgms"
name = st.sidebar.selectbox("Select a Dataset", datasets, index=datasets.index(default))
st.experimental_set_query_params(dataset=name)

# Initiate dataset class
dataset = Dataset(name)
config = dataset.get_config_by_version("latest")
st.sidebar.write(config)

# List all versions and find latest version
versions = dataset.list_versions
latest_version = dataset.latest_version
other_versions = [v for v in versions if v not in ["latest", latest_version]]
other_versions.sort(reverse=True)
sorted_versions = ["latest", latest_version] + other_versions

# Layout for each dataset
st.markdown(f"# {random.choice(emojis)} {name}")
st.markdown(config["dataset"]["info"]["description"])
st.markdown(f"[more info]({config['dataset']['info']['url']})")


def create_download_link_markdown(version) -> str:
    """
    Create a list of hyperlink markdowns for the download urls
    """
    files = dataset.list_files_by_version(version)
    mk = []
    for f in files:
        filename = f.split("/")[-1]
        url = dataset.create_download_url(f)
        mk.append(f"[{filename}]({url})")
    return mk


# For each version, render a download content
for v in sorted_versions:
    mk = create_download_link_markdown(v)
    if v == "latest":
        st.markdown(
            f"""
        ## version: `latest` **(latest)**
        > Note: below links are permalinks and will always reflect the latest versions
        """
        )
        for m in mk:
            st.markdown(m)

    elif v == latest_version:
        st.markdown(
            f"""
        ## version: `{latest_version}` **(latest)**
        > Note: currently version `{latest_version}` is the latest
        """
        )
        for m in mk:
            st.markdown(m)
    else:
        st.markdown(
            f"""
        ## version: `{v}`
        """
        )
        for m in mk:
            st.markdown(m)
