# GitHub as a Data Source
Now that we understand the distinction between Git and GitHub, we can understand the rich data set that each source can provide. A researcher can obtain data either from the Git repository or from the GitHub platform, with each platform having a different method for accessing the data and offering its own unique set of data as well as advantages.
## Research Data from Git
Git can provide data about changes to the source code. Specifically, it can provide data about what changes were made in a repository, when they were made and by whom. It does not provide any information related to the social coding interactions that occur on GitHub. Since Git is a tool that is not unique to GitHub, the information shared in this section applies to Git repositories hosted on platforms other than GitHub as well. Researchers can obtain research data by extracting useful information directly from the source code—such as metrics and dependency graphs—or can choose to extract meta-information that describes who changed what in the repository. The methods described here are not specific to repositories hosted on GitHub, but can be applied to any Git repository that a researcher can clone to his or her computer.
The general steps a researcher must follow to extract data from Git are:
1.	Clone the Git repository to the local machine using Git clone;
2.	Revert to a specific revision of the code base to extract data for a specific point in time using Git checkout <revision>;
3.	Extract data directly from source code, or from metadata using commands such as git log, git diff, or git blame. 
### Cloning Repos
There are two types of repository URLs on GitHub, depending on whether SSH or HTTPS URLs are used:
-	SSH URL: git@github.com:<ownername>/<reponame>.git
-	HTTPS URL: https://github.com/<ownername>/<reponame>.git
The repo URL in both formats consists of two main parts: the GitHub hostname and the project full name. The project full name is the path consisting of both the owner name and repo name. The project full name is a unique value on GitHub and can be used to identify any repository, even forked ones. For example:
1.	git@github.com:remoteinterview/zero.git
2.	git@github.com:0xflotus/zero.git
3.	git@github.com:anblandy/zero.git
4.	git@github.com:django/django.git
All four of these repositories are hosted on GitHub. The first three are three forks for the same project, “zero”, which belongs to three different owners: remoteinterview, 0xflotus, and anblandy. The fourth repo is an entirely different project, “django”, and is owned by the user django. When referring to a repo on GitHub, it is better to always use the owner/repo notation to identify a repository.
### 3.1.2	Identifying Revisions
Git keeps snapshots of files in the file system and records how these change over time. Central to these changes is the concept of revision, which is a 40-character unique ID (SHA1 hash) that corresponds to a successful commit operation and identifies a specific snapshot in time. Researchers who know the revision IDs can virtually travel in time to view different versions of a file, directory, or even complete a repository. 
To identify revisions—and extract useful meta-information—researchers can use the git log command:
```bash
commit f1f4aeb22e7bc9b504f69f7cb111ac9bdedb5f1e (HEAD -> master, origin/master, origin/HEAD)
Author: Dohyeon Kim <nero.union12@gmail.com>
Date:   Tue May 29 21:41:32 2018 +0900

    Fixed #28044 -- Unified the logic for createsuperuser's interactive and --noinput modes.

commit 0914a2003b1ad50f1d641709da86c14826bf063b
Author: Wang Dongxiao <me@wangdongxiao.com>
Date:   Mon May 28 21:14:46 2018 +0800

    Added 'caches' to django.core.cache.__all__.
```
The output shows the history for two revisions. The first line includes the revision ID following the word commit, followed by the author name, the date, and, finally, a commit message written by the author to describe what was done in this revision. It is important to note that all data in Git is textual and must be extracted by writing scripts to produce the output and parse the required information from it.

The git log command is quite flexible. The output can be customized using the --pretty or --format flags<sup>[1](#myfootnote1)</sup>. But the most useful options for the command are the ones that allow a researcher to filter commits based on date ranges, author names, or even commit messages. For example, the command git log --after="2017-01-01" --before="2017-02-01" would produce a list of commits in reverse chronological order for all commits between January 1, 2017, and February 1, 2017 (inclusive).
Typically, a researcher might sample some commits on specific dates. The researcher must clearly define the sampling protocol which must include:
-   The date range as well as the sampling duration;
-	Which commit is selected from the date range (e.g., first or last);
-	The order in which the commits are organized—Git defaults to commit date;
-	Whether commit date and author date are used to select the sample. Author date can be different depending on the workflow. The author date is when the patch was written, the commit date is when it was committed to the current code base.

One tip we can offer to simplify parsing and sampling of revision IDs is to format the log message to be shown on a single line and show only information relevant to the sampling process. Adding the option --pretty="%h %cD %s" to the command would achieve that and makes it easier to parse the output.
Once the revision to be included in the analysis is identified, the Git checkout <revision id> is used to switch to that revision, and then the data extraction process can begin. Other features in Git that might be useful in identifying revisions, and that might carry some useful information on the development process as well, are tags and branches. Such features might be too advanced for this tutorial, but they are important tools for identifying important revisions in a repository and we highly encourage researchers to familiarize themselves with them<sup>[2](#myfootnote2)</sup>.  

<a name="myfootnote1">1</a>: The complete git log reference can be found at https://git-scm.com/docs/git-log and the pretty format syntax to customize the log output is described at https://git-scm.com/docs/pretty-formats.
<a name="myfootnote2">2</a>: We would highly encourage the reader to get more familiar with how developers use Git to better make use of the data it makes available. Since this is an introductory tutorial, we will refer the reader to https://git-scm.com/book/en/v2/Git-Basics-Tagging for more information on tagging, and https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging for more information on branching.
