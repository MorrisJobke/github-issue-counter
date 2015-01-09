# GitHub issue count stats

This is a script that fetches all issues and PRs from GitHub for a specific
repo. Then it calculates the count of open issues/PRs and their closed
counterpart.

You can combine the output of this script with `gnuplot` and get following.

![open issues](https://cloud.githubusercontent.com/assets/245432/5655326/0297ea18-96cd-11e4-9e77-df2b770dd1cd.png)

## How to start

Install the requirements

        pip install github3.py

or

        pip install -r requirements.txt

Get an API key for GitHub and set it as `GITHUB_TOKEN` in `import_issues.py`.

Update the `ORG` and `REPO` constant in `import_issues.py` and `process_issues.py`.

You can also specify a list of bug labels (BUG_LABEL) that rate a ticket with 10, and critical bug labels
(CRITICAL_BUG_LABEL) that rate a ticket with 100. All other tickets are rated with 1. These numbers just apply for open
tickets.

Then there is a new list for all sub components of your software that contains tickets in the same bug tracker and have
separate labels. Each of them will get a sub rating to compare sub components against each other. They are specified by
the APP_LABEL config option.

Run fetcher part:

        ./import_issues.py

This will fetch all issues and PRs and save the needed information to a JSON
file to work with in the next step, which saves GitHub API requests and speeds
the overall process up.

No process this file and calculate the issue/PR count for each day:

        ./process_issues.py

This then saves the result to a file called `result.tsv`, which has following
format(columns are separated by tabs):


        date	open_issues	closed_issues	open_prs	closed_prs
        2012-08-26	0	0	0	1
        2012-08-27	2	1	1	1
        2012-08-28	2	1	0	2

You can plot this file to a line graph via `gnuplot` and following commands:

        set xdata time
        set timefmt '%Y-%m-%d'
        plot 'result.tsv' using 1:2 title column with lines, 'result.tsv' using 1:3 title column with lines, 'result.tsv' using 1:4 title column with lines, 'result.tsv' using 1:5 title column with lines

For plotting the ranking graph:

        plot 'result.tsv' using 1:6 title column with lines

For plotting the ranking graph per app use this:

        plot 'result.tsv' using 1:7 title column with lines, 'result.tsv' using 1:8 title column with lines, 'result.tsv' using 1:9 title column with lines, 'result.tsv' using 1:10 title column with lines, 'result.tsv' using 1:11 title column with lines, 'result.tsv' using 1:12 title column with lines, 'result.tsv' using 1:13 title column with lines,  'result.tsv' using 1:14 title column with lines
