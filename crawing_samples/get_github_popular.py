# by chengwei, use github api v4
import requests
import pymongo
import json
c = pymongo.MongoClient('localhost', port=27018)
npm = c['application']
popular_repos = npm['popular_repos']

headers = {"Authorization": "XXX"}


def run_query(query):  # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    # else:
    #     raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.


def form_query(key):
    query = """
    query {
      search(query: "is:public stars:>1000 language:javascript", type: REPOSITORY, first:100""" + s + """ ) {
        repositoryCount
        pageInfo {
          startCursor
          endCursor
          hasNextPage
          hasPreviousPage
        }
        edges {
          node {
            ... on Repository {
              nameWithOwner
              stargazers {
                totalCount
              }
            }
          }
        }
      }
    }
    """
    return query
s = ''
repolist = []
has_next = True
while has_next:
    query = form_query(s)
    result = run_query(query)  # Execute the query
    key = result['data']['search']['pageInfo']['endCursor']
    print(key)
    s = ', after: "{}"'.format(key)
    if len(result['data']['search']['edges']) < 100:
        break
    else:
        repolist += result['data']['search']['edges']
namelist = list(x['node']['nameWithOwner'] for x in repolist)

with open('popular_js_repos.json', 'w') as f:
    json.dump(namelist, f)

popular_repos.insert(repolist)

# first 480 stars are over 10k
# first 153 stars are over 20k