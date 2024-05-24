# based on githubcrawler
# stars > 1000
# keyword contains IOT", "control", etc.
# amount == 500 projects

#############
# Libraries #
#############

import wget
import time
import simplejson
import pycurl
import os
import urllib

try:
    # Python 3
    from io import BytesIO
except ImportError:
    # Python 2
    from StringIO import StringIO as BytesIO


ACCESS_TOKEN = "xxxx"
URL = "https://api.github.com/search/repositories?&q="  # The basic URL to use the GitHub API
QUERY = "IOT"  # The personalized query (for instance, to get repositories from user 'rsain')
# SUBQUERIES_stars = "+stars:>500"
PARAMETERS = "&sort=stars&order=desc&per_page=10"  # Additional parameters for the query (by default 100 items per page)
DELAY_BETWEEN_QUERYS = (
    10  # The time to wait between different queries to GitHub (to avoid be banned)
)
OUTPUT_FOLDER = (
    "/Users/turly221/test-data/kongan_github/"  # Folder where ZIP files will be stored
)
OUTPUT_TXT_FILE = "/Users/turly221/test-data/kongan_github/"  # Path to the txt file generated as output
MINIMUM_PROJECT_NUM = 150  # The minimum num of projects

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

#############
# Functions #
#############


def getUrl(url):
    """ Given a URL it returns its body """
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.HTTPHEADER, [f"Authorization: token {ACCESS_TOKEN}"])
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    try:
        c.perform()
    except Exception as e:
        print(e)
        time.sleep(DELAY_BETWEEN_QUERYS)
        c.perform()
    c.close()
    body = buffer.getvalue().decode("utf-8")

    return body


########
# MAIN #
########


def downProj():
    # To save the number of repositories processed
    countOfRepositories = 0
    max_count = 2000000

    # url = URL + QUERY + SUBQUERIES_stars + PARAMETERS
    url = URL + QUERY + PARAMETERS
    print("query url: ", url)
    try:
        dataRead = simplejson.loads(getUrl(url))
        max_count = int(dataRead.get("total_count"))
    except Exception as e:
        print(f"query url: faied: {e}")
        time.sleep(DELAY_BETWEEN_QUERYS)
        return 1
    print(f"total count: {dataRead.get('total_count')}")
    if max_count == 0:
        print(f"return as no result found")
        return 0

    # Output CSV file which will contain information about repositories
    f = open(OUTPUT_TXT_FILE + f"{QUERY}-repositories.txt", "a+")

    while countOfRepositories < max_count:
        # Results are in different pages
        for currentPage in range(1, 11):
            url = URL + QUERY + PARAMETERS + "&page=" + str(currentPage)
            print("current page url: ", url)
            try:
                dataRead = simplejson.loads(getUrl(url))
            except Exception as e:
                print(e)
                if countOfRepositories > MINIMUM_PROJECT_NUM:
                    print("match MINIMUM_PROJECT_NUM")
                    return 0
                else:
                    time.sleep(DELAY_BETWEEN_QUERYS)
                    return 1

            # print(dataRead)
            # Iteration over all the repositories in the current json content page
            for item in dataRead["items"]:
                # Obtain user and repository names
                user = item["owner"]["login"]
                repository = item["name"]

                # Download the zip file of the current project
                print(
                    "Downloading repository '%s' from user '%s' ..."
                    % (repository, user)
                )
                clone_url = item["clone_url"]
                fileToDownload = (
                    clone_url[0 : len(clone_url) - 4] + "/archive/master.zip"
                )
                fileName = item["full_name"].replace("/", "#") + ".zip"

                if os.path.exists(OUTPUT_FOLDER + fileName):
                    countOfRepositories = countOfRepositories + 1
                    continue

                print("download url: " + fileToDownload)

                try:
                    wget.download(fileToDownload, out=OUTPUT_FOLDER + fileName)
                except Exception as e:
                    print(f"download url faield: {e}, continue")
                    continue
                f.write("user: " + user + "; repository: " + repository + "\n")
                countOfRepositories = countOfRepositories + 1
                if countOfRepositories > MINIMUM_PROJECT_NUM:
                    return 0

            print("Sleeping %d seconds" % DELAY_BETWEEN_QUERYS)
            time.sleep(DELAY_BETWEEN_QUERYS)

    print("DONE! %d repositories have been processed." % countOfRepositories)
    f.close()
    return 0


def download_for_keyword(target_keyword, target_count):
    global QUERY
    QUERY = urllib.parse.quote(target_keyword)
    global MINIMUM_PROJECT_NUM
    MINIMUM_PROJECT_NUM = target_count
    res = 1
    while res:
        res = downProj()


if __name__ == "__main__":
    industry4buzz_keywords = [
        "Internet of Things (IoT) platforms",
        "Location detection",
        "human machine interfaces",
        "fraud detection",
        "3D printing",
        "Smart sensors",
        "Big data",
        "machine learning",
        "artificial intelligence",
        "Multilevel customer interaction",
        "customer profiling",
        "Augmented reality",
        "virtual reality",
        "wearables",
        "Fog computing",
        "edge computing",
        "cloud computing",
    ]
    print("start to process industry4buzz_keywords")
    for target in industry4buzz_keywords:
        download_for_keyword(target, 30)

    extra_keywords = [
        "smart home",
        "smart building",
        "Smart factory",
        "AUTOSAR",
        "automotive",
        "robot",
        "autocad",
    ]
    print("start to process extra_keywords")
    for target in extra_keywords:
        download_for_keyword(target, 20)

    traditional_keywords = [
        "computer-aided design software‎",
        "scada",
        "Building information modeling‎",
        "Chemical engineering software‎",
        "Manufacturing software",
        "Film production software",
        "industrial automation",
        "enterprise resource planning",
        "Inductive Automation",
        "Power engineering software",
    ]
    print("start to process traditional_keywords")
    for target in traditional_keywords:
        download_for_keyword(target, 10)
