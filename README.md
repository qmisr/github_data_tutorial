# GitHub Data Collection Tutorial
You can get some background information on GitHub data from the following [tutorial](datasource.md)

# Before use
1. Make sure you have a GitHub username and get [GitHub API tokens](https://github.com/settings/tokens) (You need to sign-in with your GitHub user)
2. rename local_settings.py.template to local_settings.py
3. Open local_settings.py and replace values with your GitHub credentials
4. Run the notebooks locally

# Requirements
Install the following packages using pip:
- requests-html
- python-dateutil
- pytz
- pandas
- gitpython

# Examples
- Using GitHub API in (github_api_examples)[./github_api_examples.ipynb]
- Scrapping github.com in (github_scrapping_examples)[./github_scrapping_examples.ipynb]
- Extracting data from Git (git_data_examples)[./git_data_examples.ipynb]

**Note:** you can view jupyter notebooks on GitHub!

# How to improve this work

You are welcome to report bugs and suggest improvements by creating [new issues](https://github.com/qmisr/github_data_tutorial/issues/new)


The main functions are in utils.py and parse_git_stats.py. You can clone this work and re-use and send a pull request for any improvements you make.

You can also review the py files and add comments by clicking on the line numbers to open issues.

