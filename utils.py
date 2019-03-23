import os

from git import Repo
from urllib.parse import urlparse, parse_qs

import requests
import pandas as pd
from pandas.io.json import json_normalize
from requests_html import HTMLSession

# hack to load configuration settings
from local_settings import *

GITHUB_ROOT_ENDPOINT = "https://api.github.com"


def fetch_github_api_data(api_path, accept_header=None,
                          params=None, debug=False, raw_response=False):
    # construct full url, but first
    # strip any leading or trailing /
    api_path = api_path.strip("/")
    url = "{}/{}".format(GITHUB_ROOT_ENDPOINT, api_path)
    print("Fetching data from {} params {}".format(url, params))
    if debug:
        print("Accept head: {}".format(accept_header))
    # Add optional headers or not
    # Some GitHub endpoints require Accept
    # header to be changed
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if accept_header:
        headers["Accept"] = accept_header

    # construct request
    r = requests.get(
        url,
        auth=(USERNAME, GITHUB_TOKEN),  # from local_settings
        headers=headers,
        params=params)

    if debug:
        print(r.json())
    # return a pandas dataframe from the json response
    # unless user requested raw_response
    if raw_response:
        return r
    return json_normalize(r.json())


def search_github(resource, search_query, page=None):
    params = {"q": search_query, "per_page": 100}
    if page:
        params["page"] = page

    # fetch search result
    search_res = fetch_github_api_data(
        "/search/{}".format(resource),
        accept_header="application/vnd.github.mercy-preview+json",
        params=params,
        raw_response=True)

    # parse json result
    res = search_res.json()

    # if page was set, then no need for pagination information
    if not page:
        # find pages for pagination
        # check if we have last page
        last_url = search_res.links.get("last")
        if last_url:
            p = urlparse(last_url.get("url"))
            try:
                pages = int(parse_qs(p.query).get("page")[0])
            except ValueError as ve:
                # single page if parsing error
                pages = 1

            # add pagination information
            pagination = {
                "page": 1,
                "total_pages": pages,
            }
            res["pagination"] = pagination
    return res


# This will clone the repo of a single project if it does not exist
def clone_git_repo(full_name, repo_url, repos_dir="./repos"):
    # replace slashes with underscore to use for dir names
    pdir_name = full_name.replace("/", "_")
    prepo_path = os.path.join(repos_dir, pdir_name)

    # create repos directory if not exists
    if not os.path.exists(repos_dir):
        os.makedirs(repos_dir)

    # check if project directory exists
    if os.path.exists(prepo_path):
        print("Repo exists in {}, not going to clone.".format(
            pdir_name))
    else:
        # if not exists it means we need to create directory
        # the we can clone into it
        os.makedirs(prepo_path)
        print(" cloning {} please wait ...".format(repo_url))
        Repo.clone_from(repo_url, prepo_path)
        print("finished cloning in {}.".format(prepo_path))
