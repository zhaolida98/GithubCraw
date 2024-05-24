import pandas as pd
import os

token_pool = [
    #'0eab3f8517a53409e6bf1e3c1011c95a679688e1',
    '2eeff8a2b015b39732d5ccdd704d763f0eaeaf24',
    '5d6652ecf38702c003cf93e577da51dce3966b22',
    '8d636b909a0853775074a0086fe5844f31341775',
    '8bbab49f728dfe2f8d24133e72b5df6694182388',
    'fce7ccaa37ea90c215e2316fd52baf65c4b0cfa3',
    'd87ff2386248496d4c4b5018b1dc3170e4fdaa90',
    'ec86578e8826e23a515efba3dbe3045a8f0acfc4',
    '5b925bbd889bab4cb1978162aff87b25cee3628a',
    '8a63d8f43734b87ea6197bbec276298d0d99a170',
    '6d960ff5fa99779bf4694146f2cd534ed7306825',
    '5aca901da564bd2597af2175fe38738813ca0536',
    '16ed9533807f976d4d0d7505b5162762283fb65e',
    '80e30b0518f19d6d469fbfc50d3ebb3e764d5055',
    '00e07c81f0428b137f3508ea0bbce9341a65c1b0',
    'f9bc29389fe3de0ad10968a90166c9d50d1a5cad',
    '97b6d38f0ef247f5ad31bbee3408a94075d4b67a',
    '5c4d4e5d600e741154c9010ce628b9e7226a994c',
]
WORKER = 4
download_directory = "C:\\FileWorks\\CODE\\Scantist\\GithubCrawing\\download"

def get_urls():
    """
        Example Maven pom file download. Change the implementation of
        this method to supply a list of urls to request, along with
        the filenames to use to save the response.
    """

    df = pd.read_csv("/home/lee/Downloads/mostUsedLibs/mostly_used_libs/Maven_project_1-4_pages.csv")
    link = df.repo_link
    names = df.name

    urls=[]
    for a in range(len(names)):
        vendor, component = names[a].split(':')
        if link[a].startswith('https://github.com'):
            base, body = link[a].split('//')
            thelink = f'{body}.git'
        elif link[a].startswith('https://git-wip'):
            base3, body3 = link[a].split('//')
            thelink = body3.replace("?p=","/")
        elif link[a].startswith('scm:git'):
            base1, body1 = link[a].split('//')
            newbody1 = body1.split('/')
            thelink = "{}/{}/{}".format(newbody1[0], newbody1[1], newbody1[2])
        elif link[a].startswith('git://android'):
            newbody2 = link[a].split('/')
            thelink = "android.googlesource.com/{}/{}".format(newbody2[3],newbody2[4])
        elif link[a].startswith('https://git.openstack'):
            base4, body4 = link[a].split('//')
            thelink = body4.replace("git.openstack.org/cgit/openstack-dev/pbr/","opendev.org/openstack/pbr.git")
        else:
            print("{} is not supported".format(link[a]))
        thename = f'{component}'
        urls.append((thelink, thename))

    # Remove duplicate
    # Using set
    seen = set()

    # using list comprehension
    output = [(a, b) for a, b in urls
              if not (a in seen or seen.add(a))]

    return output


def download(info):
    url, filename = info
    token = random.choice(token_pool)

    if url.startswith("github.com") or url.startswith("android") or url.startswith("git-wip"):
        command = "git clone --progress https://{}@{}".format(token, url)
        temp = os.curdir
        os.chdir(download_directory)
        os.system(command)
        os.chdir(temp)


def run(get_url_fn=None, download_fn=None):
    if not get_url_fn:
        get_url_fn = get_urls
    if not download_fn:
        download_fn = download
    # Get the URLs to download
    request_urls = get_url_fn()

    # Download in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKER) as executor:
        future_names = [executor.submit(download_fn, url) for url in request_urls]
        for future in concurrent.futures.as_completed(future_names):
            # Wait for all threads to complete
            pass


def test():
    link = "https://git-wip-us.apache.org/repos/asf?p=commons-io.git"

    base3, body3 = link.split('//')
    body = body3.replace("?p=", "/")
    print(body)
    print(url)

run()