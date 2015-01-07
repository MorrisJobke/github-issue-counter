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
        plot 'result.tsv' using 1:2 title 'open issues' with lines, 'result.tsv' using 1:3 title 'closed issues' with lines, 'result.tsv' using 1:4 title 'open PRs' with lines, 'result.tsv' using 1:5 title 'closed PRs' with lines
