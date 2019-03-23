# GitHub Data Collection Tutorial
This is a companion repository for the tutorial entitled:

### The Challenges and Opportunities Mining GitHub

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

You are welcome to report bugs and suggest improvements by creating [issues](https://github.com/qmisr/github_data_tutorial/issues/new)


The main functions are in utils.py and parse_git_stats.py. You can clone this work and re-use and send a pull request for any improvements you make.

You can also review the py files and add comments by clicking on the line numbers to open issues.

# How to cite this work

You are welcome to reuse and adapt this work for your own project, we ask that you reference this work in your project.

At the moment, this is part of the following working paper, cite it as:

```AlMarzouq, M., AlZaidan, A., & AlDallal, J. (2019). The Challenges and Opportunities Mining GitHub. Working paper.```

We would appreciate any comments on how to best cite this work. Should the repository be cited? or the research paper that introduced the instrument? One problem that needs to be addressed is how improvements can be recognized? We can certainly add an AUTHORS file, but just like survey instrument, we hope that there can be a way in which improvements can be recognized in research papers.
