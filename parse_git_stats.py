import os
import subprocess
import sys
from datetime import datetime, timedelta

import pandas as pd
import numpy as np


def get_main_head_rev(repo_path):
    cdr = os.getcwd()
    os.chdir(repo_path)
    command = "git show-ref --heads -s"
    process = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, stderroutput = process.communicate()
    gitrev = stdoutput.decode("utf-8").strip()
    os.chdir(cdr)
    return gitrev

# function to get period, start_date, and end_date tuple for period


def get_period_range(start_year=2014, end_year=2017):
    period = 0
    for ayear in range(start_year, end_year):
        # remember, december must have end date as jan 1st of next year
        for amonth in range(1, 13):
            period += 1  # start from period 0 and count
            start_date = datetime(ayear, amonth, 1)
            if amonth == 12:
                end_date = datetime(ayear + 1, 1, 1)
            else:
                end_date = datetime(ayear, amonth + 1, 1)
            yield (period, start_date, end_date)


def count_contribs_in_git_log(
    start_date,
    end_date,
    no_merges=False,
    merges_only=False,
):
    # BUG: realted to how contribs are counted
    # we have a sliding window to asses if developer is first time contrib
    # but this puts the count for total contribs and committers off
    # need to have fix date for considering new contrib
    if no_merges:
        nmerges = " --no-merges"
    else:
        nmerges = ""

    if merges_only:
        mrgsonly = " --merges"
    else:
        mrgsonly = ""
    # we check a year back to see new contributors
    command = "git log --after='{start_date}' --before='{end_date}'{nmerges} "\
        "{merges_only} --reverse --pretty='%aE\t%at\t%cE'".format(
            start_date=start_date - timedelta(days=365),
            end_date=end_date,
            nmerges=nmerges,
            merges_only=mrgsonly,
        )
    # print("WORKING DIR IS:", os.getcwd())
    # print(command)  # debugging
    output = str(subprocess.check_output(
        command, shell=True), encoding="utf-8").strip()
    # print(cnt) # debugging
    data = [x.split("\t") for x in output.split("\n") if x]
    # print(data)
    # lets start counting contribs and committers
    new_contrib = []
    new_commiters = []
    contribs = {}
    commits = {}
    commits_others = {}
    all_contribs = {}
    all_commits = {}
    for auth, tm, comm in data:

        cdtime = datetime.fromtimestamp(int(tm))

        if not auth:
            continue
        # find whoever is a first time contrib within our period
        if (cdtime >= start_date and
                auth not in all_contribs.keys() and
                auth not in all_commits.keys()):
            # print("adding new contrib:", auth)
            # print("add_contribs:", all_contribs)
            # print("add_commits:", all_commits)
            new_contrib.append((auth, tm))

        # find whoever is a first time committer
        # and is committing work of others
        if (cdtime >= start_date and auth != comm and
                comm not in all_commits.keys()):
            new_commiters.append((comm, tm))

        # find whoever is a committer (other) within our period
        # meaning, this is a committer that committed then
        # work of others (author != committer)
        if cdtime >= start_date and auth != comm:
            commits_others[comm] = commits_others.setdefault(comm, 0) + 1

        # total count for the period
        if cdtime >= start_date:
            contribs[auth] = contribs.setdefault(auth, 0) + 1
            commits[comm] = commits.setdefault(comm, 0) + 1

        # in all commits to used to correctly find new contribs
        all_contribs[auth] = all_contribs.setdefault(auth, 0) + 1
        all_commits[comm] = all_commits.setdefault(comm, 0) + 1

        # we can calculate work distribution for committers and contribs
        # we need max, min, mean, median, and sd
        # do we need name of max contributor or committer?
        # maybe their percentage?

    total_sum_contribs = sum(contribs.values())
    total_sum_commits = sum(commits.values())
    total_sum_commits_for_others = sum(commits_others.values())

    if total_sum_contribs:
        contrib_ratios = sorted(
            [x / total_sum_contribs for x in contribs.values()])
    else:
        contrib_ratios = [0]

    if total_sum_commits:
        commit_ratios = sorted(
            [x / total_sum_commits for x in commits.values()])
    else:
        commit_ratios = [0]
    if total_sum_commits_for_others:
        commit_for_others_ratios = sorted([x / total_sum_commits_for_others
                                           for x in commits_others.values()])
    else:
        commit_for_others_ratios = [0]

    contribs_values = list(contribs.values())
    commits_values = list(commits.values())
    commits_others_values = list(commits_others.values())

    # print(contribs)

    return {
        "new_contribs": len(new_contrib),
        "new_commiters": len(new_commiters),
        "total_contribs": len(contribs.keys()),
        "committers_for_others": len(commits_others.keys()),
        "total_committers": len(commits.keys()),

        "mean_contribs": (contribs_values or None) and np.mean(contribs_values),
        "median_contribs": (contribs_values or None) and np.median(contribs_values),
        "std_contribs": (contribs_values or None) and np.std(contribs_values),
        "max_contribs": (contribs_values or None) and np.max(contribs_values),
        "min_contribs": (contribs_values or None) and np.min(contribs_values),
        "top_conrib_ratio": contrib_ratios[-1],
        "bottom_conrib_ratio": contrib_ratios[0],
        "mean_contrib_ratio": (contrib_ratios or None) and np.mean(contrib_ratios),
        "median_contrib_ratio": (contrib_ratios or None) and np.median(contrib_ratios),
        "conrib_ratio": contrib_ratios,

        "mean_commits": (commits_values or None) and np.mean(commits_values),
        "median_commits": (commits_values or None) and np.median(commits_values),
        "std_commits": (commits_values or None) and np.std(commits_values),
        "max_commits": (commits_values or None) and np.max(commits_values),
        "min_commits": (commits_values or None) and np.min(commits_values),
        "top_commits_ratio": commit_ratios[-1],
        "bottom_commits_ratio": commit_ratios[0],
        "mean_commits_ratio": (commit_ratios or None) and np.mean(commit_ratios),
        "median_commits_ratio": (commit_ratios or None) and np.median(commit_ratios),
        "commits_ratio": commit_ratios,

        "mean_commits_others": (commits_others_values or None) and np.mean(commits_others_values),
        "median_commits_others": (commits_others_values or None) and np.median(commits_others_values),
        "std_commits_others": (commits_others_values or None) and np.std(commits_others_values),
        "max_commits_others": (commits_others_values or None) and np.max(commits_others_values),
        "min_commits_others": (commits_others_values or None) and np.min(commits_others_values),
        "top_commits_others_ratio": commit_for_others_ratios[-1],
        "bottom_commits_others_ratio": commit_for_others_ratios[0],
        "mean_commit_for_others_ratios": (commit_for_others_ratios or None) and np.mean(commit_for_others_ratios),
        "median_commit_for_others_ratios": (commit_for_others_ratios or None) and np.median(commit_for_others_ratios),
        "commit_for_others_ratios": commit_for_others_ratios,
    }


def count_occurance_in_git_log(
    grep,
    start_date,
    end_date,
    invert_grep=False,
    no_merges=False,
    merges_only=False,
    is_perl_regex=False,
):
    invertg = ""
    pregex = ""
    if invert_grep:
        invertg = " --invert-grep"

    if is_perl_regex:
        pregex = " --perl-regexp"

    if no_merges:
        nmerges = " --no-merges"
    else:
        nmerges = ""

    if merges_only:
        mrgsonly = " --merges"
    else:
        mrgsonly = ""
    command = "git log --after='{start_date}' --before='{end_date}'{nmerges} "\
        "{merges_only} --pretty='%h' -i --grep='{grep}'{invertg}{pregex} | wc -l".format(
            start_date=start_date,
            end_date=end_date,
            grep=grep,
            invertg=invertg,
            nmerges=nmerges,
            merges_only=mrgsonly,
            pregex=pregex,
        )
    # print("WORKING DIR IS:", os.getcwd())
    # print(command) # debugging
    cnt = subprocess.check_output(command, shell=True)
    # print(cnt) # debugging
    return int(cnt.strip())


def list_git_log_revs(
        grep, start_date, end_date,
        invert_grep=False, no_merges=False, merges_only=False, is_perl_regex=False):
    invertg = ""
    pregex = ""
    if invert_grep:
        invertg = " --invert-grep"

    if is_perl_regex:
        pregex = " --perl-regexp"

    if no_merges:
        nmerges = " --no-merges"
    else:
        nmerges = ""

    if merges_only:
        mrgsonly = " --merges"
    else:
        mrgsonly = ""

    command = "git log --after='{start_date}' --before='{end_date}'{nmerges} "\
        "{mrgsonly} --pretty='%H' -i --grep='{grep}'{invertg}{pregex}".format(
            start_date=start_date,
            end_date=end_date,
            grep=grep,
            invertg=invertg,
            nmerges=nmerges,
            mrgsonly=mrgsonly,
            pregex=pregex,
        )
#     print(command)
    lst = str(subprocess.check_output(command, shell=True), "utf-8")
#     print(cnt)
    return [x.strip() for x in lst.split("\n") if x]


def get_stats_from_diff(r1, r2):
    values = [0, 0, 0]
    command = "git diff {} {} --shortstat".format(r1, r2)
    try:
        output = str(subprocess.check_output(command, shell=True), "utf-8")
    except:
        print("problem in diff {}, {} calling process".format(r1, r2))
        return values
    output = output.split(",")
    for item in output:
        try:
            val = int(item.strip().split()[0])
            if "file" in item:
                values[0] += val
            elif "insert" in item:
                values[1] += val
            elif "delet" in item:
                values[2] += val
            else:
                print("got an unknown item in:", output)
        except:
            print("problem in diff {}, {} item:".format(r1, r2), output)
    return values


def get_first_commit_timestamp():
    command = "git rev-list --max-parents=0 HEAD| xargs git log --pretty='%at'"
    output = str(subprocess.check_output(command, shell=True), "utf-8")
    revs = [x for x in output.split("\n") if x]
    return datetime.fromtimestamp(int(revs[-1]))


def get_tags_and_dates():
    command = "git tag"
    tags = str(subprocess.check_output(
        command, shell=True), "utf-8").split("\n")
    command = "git tag | xargs -L 1 git log --pretty='%at' -1"
    timestamps = str(subprocess.check_output(
        command, shell=True), "utf-8").split("\n")
    dates = [datetime.fromtimestamp(int(x)).date() for x in timestamps if x]
    return list(zip(tags, dates))


def get_tags_between_dates(start_date, end_date, tags_dates):
    return [
        t for t, d in tags_dates
        if start_date <= d < end_date
    ]


def get_git_stats_for_project(full_name,
                              start_year,  # inclusive
                              end_year,  # non-inclusive
                              repos_dir="./repos"
                              ):
    prid_name = full_name.replace("/", "_")
    repo_path = os.path.join(repos_dir, prid_name)
    # correct_dates = [date.strftime("%Y-%m-%d") for date in dates]
    # switch to head revision
    get_main_head_rev(repo_path)
    # switch to revision in desired date
    header = [
        "full_name", "date", "end_date", "period",
        "total_revs", "first_rev", "last_rev",
        "new_contribs", "new_committers", "total_contribs",
        "committers_for_others", "total_committers",

        "mean_contribs", "median_contribs", "std_contribs",
        "max_contribs", "min_contribs", "top_conrib_ratio",
        "bottom_conrib_ratio", "conrib_ratio",

        "mean_commits", "median_commits", "std_commits",
        "max_commits", "min_commits", "top_commits_ratio",
        "bottom_commits_ratio", "commits_ratio",

        "mean_commits_others", "median_commits_others", "std_commits_others",
        "max_commits_others", "min_commits_others", "top_commits_others_ratio",
        "bottom_commits_others_ratio", "commit_for_others_ratios",

        "initial_commit_date", "age_days", "releases", "no_releases",
        "refactors", "fixes_can_be_doc", "not_fixes_can_be_doc",
        "fixes_and_doc", "fixes_no_doc", "docs",
        "commits_no_merge", "merges", "total_commits",
        "files_changed_churn", "loc_added_churn", "loc_removed_churn",
        "files_changed_delta", "loc_added_delta", "loc_removed_delta",

    ]
    # This is a special function that uses git
    # so we have to change working dir
    cdr = os.getcwd()
    os.chdir(repo_path)

    tags_n_dates = get_tags_and_dates()
    data = []
    for period, start_date, end_date in get_period_range(start_year, end_year):

        rev_list = list_git_log_revs("", start_date, end_date)
        total_items = len(rev_list)
        if not total_items:
            print("no revisions between {} and {}".format(
                start_date, end_date))
            continue

        print("working on period {}, start: {}, end: {}".format(
                period, start_date, end_date))
                
        data_row = []
        data_row.append(full_name)
        data_row.append(start_date)
        data_row.append(end_date)
        data_row.append(period)
        # revision data
        data_row.append(total_items)
        data_row.append(rev_list[0])
        data_row.append(rev_list[-1])

        # committers and contribs
        com_data = count_contribs_in_git_log(start_date, end_date)
        data_row.append(com_data["new_contribs"])
        data_row.append(com_data["new_commiters"])
        data_row.append(com_data["total_contribs"])
        data_row.append(com_data["committers_for_others"])
        data_row.append(com_data["total_committers"])

        data_row.append(com_data["mean_contribs"])
        data_row.append(com_data["median_contribs"])
        data_row.append(com_data["std_contribs"])
        data_row.append(com_data["max_contribs"])
        data_row.append(com_data["min_contribs"])
        data_row.append(com_data["top_conrib_ratio"])
        data_row.append(com_data["bottom_conrib_ratio"])
        data_row.append(com_data["conrib_ratio"])

        data_row.append(com_data["mean_commits"])
        data_row.append(com_data["median_commits"])
        data_row.append(com_data["std_commits"])
        data_row.append(com_data["max_commits"])
        data_row.append(com_data["min_commits"])
        data_row.append(com_data["top_commits_ratio"])
        data_row.append(com_data["bottom_commits_ratio"])
        data_row.append(com_data["commits_ratio"])

        data_row.append(com_data["mean_commits_others"])
        data_row.append(com_data["median_commits_others"])
        data_row.append(com_data["std_commits_others"])
        data_row.append(com_data["max_commits_others"])
        data_row.append(com_data["min_commits_others"])
        data_row.append(com_data["top_commits_others_ratio"])
        data_row.append(com_data["bottom_commits_others_ratio"])
        data_row.append(com_data["commit_for_others_ratios"])

        # releases and age
        init_commit_date = get_first_commit_timestamp().date()
        data_row.append(init_commit_date)
        data_row.append((datetime.now().date() - init_commit_date).days)
        # releases and no_releases
        tags = get_tags_between_dates(
            start_date.date(),
            end_date.date(),
            tags_n_dates)
        data_row.append(",".join(tags))
        data_row.append(len(tags))

        # execute gitstat process
        refactors = count_occurance_in_git_log(
            "refactor",
            start_date, end_date, no_merges=True)
        fixes_can_be_doc = count_occurance_in_git_log(
            "(bug|fix|resolv)",
            start_date, end_date, is_perl_regex=True, no_merges=True)
        not_fixes_can_be_doc = count_occurance_in_git_log(
            "(bug|fix|resolv)",
            start_date, end_date, is_perl_regex=True, invert_grep=True,
            no_merges=True)
        fixes_and_doc = count_occurance_in_git_log(
            "(?=.*?doc)(?=.*?(bug|fix|resolv))",
            start_date, end_date, is_perl_regex=True, no_merges=True)
        fixes_no_doc = fixes_can_be_doc - fixes_and_doc
        docs = count_occurance_in_git_log("doc", start_date, end_date,
                                          no_merges=True)
        commits_no_merge = fixes_can_be_doc + not_fixes_can_be_doc
        merges = count_occurance_in_git_log(
            "", start_date, end_date, no_merges=False, merges_only=True)
        total_commits = commits_no_merge + merges
        data_row.extend([
            refactors, fixes_can_be_doc, not_fixes_can_be_doc,
            fixes_and_doc, fixes_no_doc, docs,
            commits_no_merge, merges, total_commits
        ])

        # calculate churn data
        # rev_list = list_git_log_revs("", start_date, end_date)
        # total_items = len(rev_list)
        churn = [0, 0, 0]
        deltas = [0, 0, 0]

        if total_items:
            left_revs = rev_list[:-1]
            # add the rev before the first rev
            left_revs.insert(0, "{}^1".format(rev_list[0]))
            right_revs = rev_list[:]
            revs = zip(left_revs, right_revs)
            # print("{} period: {} total items ".format(
            #     project, period, total_items))

            # calculate deltas here
            deltas = get_stats_from_diff(rev_list[0], rev_list[-1])
    #         print("deltas: ", deltas)
            # calculate churn here
            for i, rs in enumerate(revs):
                from operator import add
                churn = list(
                    map(add, churn, get_stats_from_diff(rs[0], rs[1])))
        data_row.extend(churn)
        data_row.extend(deltas)

        # print("appending: ", data_row)
        data.append(data_row)

    # must switch back to working dir
    os.chdir(cdr)
    return pd.DataFrame(data, columns=header)


if __name__ == '__main__':
    print("==== DF:\n",
          get_git_stats_for_project(
            "tensorflow/tensorflow", 2019, 2020
            ).head().T)
