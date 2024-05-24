"""
collect the github repos by language and sort by star, also only keep the one with pom.xml in the first layer path
- stars
  curl -H "Accept: application/vnd.github.v3+json" https://api.github.com/search/repositories?q=language%3Ajava+stars%3A1..*&sort=stars&type=Repositories&per_page=100&page=1
- fork
  curl -H "Accept: application/vnd.github.v3+json" https://api.github.com/search/repositories?q=language%3Ajava+stars%3A1..*&sort=forks&type=Repositories&per_page=100&page=1
- get trees
  https://api.github.com/repos/CyC2018/CS-Notes/git/trees/master
- *commits
  https://api.github.com/search/commits?q=repo:{repo/name}+fix+OR+bug+OR+issue
- *issues (total count)
  https://api.github.com/search/issues?q=repo:iluwatar/java-design-patterns+type:issue
- *pull request (total count)
  https://api.github.com/search/issues?q=repo:{repo/name}+type:pull-request
- recently updated
- create date(check program duration)
- size
- open issues(openissues/total issues)
"""
import csv
import json
import os
import time

import numpy as np
import requests

header = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": "token xxxxx"
}


class githubRepo:
    def __init__(self, name, size, open_issue_cnt, stars_cnt, fork_cnt, recently_update, create_date,
                 default_branch, language, commit_cnt=-1, issue_cnt=-1, pr_cnt=-1):
        self.name = name
        self.size = size
        self.recently_update = recently_update
        self.create_date = create_date
        self.open_issue_cnt = open_issue_cnt
        self.stars_cnt = stars_cnt
        self.fork_cnt = fork_cnt
        self.commit_cnt = commit_cnt
        self.issue_cnt = issue_cnt
        self.pr_cnt = pr_cnt
        self.language = language
        self.default_branch = default_branch

    def toDict(self):
        return {
            "name": self.name,
            "size": self.size,
            "recently_update": self.recently_update,
            "create_date": self.create_date,
            "open_issue_cnt": self.open_issue_cnt,
            "stars_cnt": self.stars_cnt,
            "fork_cnt": self.fork_cnt,
            "commit_cnt": self.commit_cnt,
            "issue_cnt": self.issue_cnt,
            "pr_cnt": self.pr_cnt,
            "branch": self.default_branch,
            "language": self.language
        }


def main(sort_range="stars%3A1..*", sort="stars", start_page=1, required_repo_num=1000, per_page=100):
    max_page = required_repo_num // per_page

    output_csv = open(os.path.join('..', 'SCAEvaluationData', 'collection.csv'), 'a+')
    field_name = ["name", "size", "stars_cnt", "fork_cnt", "open_issue_cnt", "recently_update", "create_date",
                  "language", "branch", "commit_cnt", "issue_cnt", "pr_cnt"]
    collection = csv.DictWriter(output_csv, field_name)

    if not os.path.exists(os.path.join('..', 'cache', 'collected_repo_name_set.npy')):
        repo_name_set = set()
    else:
        repo_name_set = np.load(os.path.join('..', 'cache', 'collected_repo_name_set.npy'), allow_pickle=True).item()
    if not os.path.exists(os.path.join('..', 'cache', 'total_repo_name_set.npy')):
        total_repo_name_set = set()
    else:
        total_repo_name_set = np.load(os.path.join('..', 'cache', 'total_repo_name_set.npy'), allow_pickle=True).item()
    last_star_cnt = 0
    try:
        for page_num in range(start_page, max_page + 1):
            query = f"https://api.github.com/search/repositories?q=language%3Ajava+{sort_range}&sort={sort}&type=Repositories&per_page={per_page}&page={page_num}"
            content = requests.get(query, headers=header).json()
            if 'items' not in content:
                with open(os.path.join('..', 'cache', 'breackpoint_result.json'), 'w') as f:
                    json.dump(content, f)
                raise RuntimeError(f"query failed at stars_range:{sort_range} on page {page_num}. check cache\\breackpoint_result.json")
            repo_list = content['items']
            for cnt, repo in enumerate(repo_list):
                print(f"processing {cnt}/{len(repo_list)} repos on page {page_num}/{max_page} of star {sort_range}", end='\r')
                name = repo['full_name']
                created_date = repo['created_at']
                updated_at = repo['updated_at']
                size = repo['size']
                star_cnt = int(repo['stargazers_count'])
                fork_cnt = int(repo['forks_count'])
                open_issue_cnt = int(repo['open_issues_count'])
                default_branch = repo['default_branch']
                language = repo['language']
                has_pom = False
                tree_query = f"https://api.github.com/repos/{name}/git/trees/{default_branch}"
                total_repo_name_set.add(name)
                if name in total_repo_name_set:
                    continue
                while True:
                    # REST API limit is 5000 per hour, which is 83 per minute. 60/83=0.73
                    tree_content = requests.get(tree_query, headers=header).json()
                    time.sleep(0.75)
                    if "tree" in tree_content:
                        file_list = tree_content['tree']
                        for file in file_list:
                            if 'pom.xml' in file['path']:
                                has_pom = True
                                break
                        if has_pom:
                            github_repo = githubRepo(name, size, open_issue_cnt, star_cnt, fork_cnt, updated_at, created_date,
                                                     default_branch, language)
                            repo_name_set.add(name)
                            collection.writerow(github_repo.toDict())
                            last_star_cnt = star_cnt
                        break
                    else:
                        with open(os.path.join('..', 'cache', 'breackpoint_result.json'), 'w') as f:
                            json.dump(tree_content, f)
                        print(f"\n{tree_query} get tree failed, sleep 10 seconds")
                        time.sleep(2)

    except KeyboardInterrupt:
        print("keyboard interrupt")
        exit(1)
    finally:
        output_csv.close()
        np.save(os.path.join('..', 'cache', 'collected_repo_name_set.npy'), repo_name_set)
        np.save(os.path.join('..', 'cache', 'total_repo_name_set.npy'), total_repo_name_set)
        print(f"\n{sort_range} done, last_star: {last_star_cnt}, project: {len(repo_name_set)}/{len(total_repo_name_set)}")
    main(f"1..{(last_star_cnt*4)//5}")

if __name__ == '__main__':
    main(sort_range="forks%3A1..*", sort="forks")

