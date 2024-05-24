import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import _thread
import time, os
import numpy as np
# from login import Login



MAX_NEEDED_NUM = 200
SENDING_GAP=5
HIDDING_GAP = 30



def get_user_agent():
    """
    功能：随机获取HTTP_User_Agent
    """
    user_agents = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36",
        "Host":"github.com",
        "Refer":"https://github.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language":"zh-CN,zh;q=0.9,zh-TW;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection":"keep-alive",
        "Cookie":"_octo=GH1.1.2041503079.1582250566; experiment:homepage_signup_flow=eyJyb2xsT3V0UGxhY2VtZW50IjoxNSwic3ViZ3JvdXAiOiJlbWFpbCIsImNyZWF0ZWRBdCI6IjIwMjAtMDItMjJUMDI6MzU6NDUuMjE5WiIsInVwZGF0ZWRBdCI6IjIwMjAtMDItMjJUMDI6MzU6NDUuMjE5WiJ9; _ga=GA1.2.1151890661.1582338968; _device_id=79a2721693b08d0c9aaeef8e8d3c5bbc; user_session=VibZhO65U6rXUpR3mS0zZUIzUyeR-fpP24xsQUU-2UxoAAUi; __Host-user_session_same_site=VibZhO65U6rXUpR3mS0zZUIzUyeR-fpP24xsQUU-2UxoAAUi; logged_in=yes; dotcom_user=zhaolida98; tz=Asia%2FShanghai; has_recent_activity=1; _gat=1; _gh_sess=FYDGloTXKtkkM0vELV9XuOFIfyWRPe0XwNMY%2B6k5BszgJofrjHNLF2LKeN3r3vkpmwmriU%2BxVg4LNOwVLcbjbSMwLFdnbOoYQUyewYRqj2EpPjfbuwtkCJKTWstXChzOcgZDHTvJOsQiAMCBqk82%2Fjwwqob7U1PP5z2rKQk4VX9voaRFaTAG88caK%2BmaO4MBHCQvZ0LisvV6QOrEh5rHgToZS7%2BqG9ptglRKdd3o%2Fqb%2FLBPMjeeGihmSyqT5JmGqg1yhunsVdw%2FUDdzfLtymZbJ6v%2BpuK6fZhfff0AmSoeCutB7km1iZTx68IFBYvwAILOSHjSnDfZE5lM83pexUXukd3aCojLUq8CA3QjUAvjuyGuela%2FpVqaUpoBgqXW%2BcjAeWddLztg5g5BV9zeYDVw%2B3P54cldxGCDggtn4q31CJo9JcM5R3x%2FPrFMO%2F0lIrzX%2BgKTvW1XVNaEUK3jXXhjg%2FV7zkXAmXGMULekzO4EctrZ8A2ynhy5KRxjM1Rl5BM0KIa7MjOG83S0u6czXewwDwfdiuJmvIAxpiU%2Bis1eu9kAh0zTfBCwx1WPFtZld0dnHXkX78muiojUoKc15oAvstMnucuShwpoLwEBIXMiRRLUWQjuFPx%2F8%2FEAJ%2BWLZHE9PpV0dwTf3Xr3gnG4ut8pTd6s54YTB1WBNZN9FYA18Szpr7lpNkKq5tZILi5tqWIYyKSLFFcwkVlE%2Ftb5gFVuvGaMPQKK0lAIKWfkxfLOK%2BkJswCHcUTpQ%2FEbImuqYVxqcst76gQCDqzoVWG9XYnEFnbIyt9HQT%2BnaXgHSmiV6u0XejaKku8%2F5KYWYL5WQGZdxCCM1uZ%2B%2BFQ0jO3ApiU84%2BESUdzJRwgDf7%2BwwKaE8LkTHeXFfQGh6HrVlazNX8Cc2e0PJWur6hKmuLRmToykZKQ%2BdKTOU%2BsapEiGw3c5x%2Bqtb2D%2FycmsTl%2BGIsA0hzjuF2G02rUA%2BaKpD32AYBTk74xCa5SZGUn8KyMbK1xb39ToRvRBgR0icVsx46WpwnEOJyrBit0bhZfJhOBhW5s5Vr0l68aym08MIcqwFL1juwCw8%2F7WjSxYdTklo2vur7dMHVZU%2BDEBpnyz0z2r6VKPTrUozOnehKLRnNW%2F4W8URy3i6oI4ErbdtiMR7BTRGd3MZ1jYdPfThde5n5NwyUqlRzo3zmUj4JdynREw%3D%3D--24XhjsCEk5dqb82A--J54SBbv8X15I5FrKhKA4cw%3D%3D"}
    return header

def get_user_agent2():
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
        "Host":"github.com",
        "Refer":"https://github.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language":"zh-CN,zh;q=0.9,zh-TW;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection":"keep-alive",
        "Cookie":"_gh_sess=XQkhB2dedoy3s2HQkkT28O8rEchJSeJqPjY%2BIcqKiy95rkp%2BjaqDYDHUsUenDOZ%2FI0WgFeAu7mik4VaJmbF2zxx1kxLoszmgOolOHM3yxm2WUf9VLEKEKrN5RDLjtkhcAul5Qu65yNvbAZVnPcAnu9Njj%2FNI79QPDLDmf7Zz04AYsuG7aJ5Se%2Bhwri4zcf5pO0RUaCFf2nRBdiWlgJSejTtIhG%2BB53ZdFtOwrkw52DEkv1Me5sLM8Wm7KZQAbgZmzIdpaIa1bwd6d8tqyjUskw%3D%3D--mH92ganwHppdxoov--gOZ%2FnWwVx%2B5v9%2F2wq%2F4nKw%3D%3D; _octo=GH1.1.574286175.1591345280; logged_in=no; tz=Asia%2FShanghai; _ga=GA1.2.1886959418.1591345315; _gat=1"
    }
    return header


def get_random_ip():
    valid_ips=[
    'x.x.x.x:xxxx'
    ]
    ip = random.choice(valid_ips)
    proxies = {
        "http": 'http://'+ip,
        "https": 'http://'+ip
    }
    return proxies

def read_num(s):
    res = ''
    for i in s:
        if i.isdigit():
            res += i
    return int(res)

def is_in_file_list(reqfiles,first_level_file_list):
    if reqfiles !='.sln':
        if  reqfiles in first_level_file_list:
            return True
    elif reqfiles == '.sln' or reqfiles == '.csproj':
        for files in first_level_file_list:
            if reqfiles in files:
                return True
    else:
        return False

def scraper(packages_files, header=None, proxy=None):
    project_num = 0
    max_page_num = 0
    # for page_num in range(pages[0], pages[1]):
    for pkgname in packages_files:
        for reqfiles in packages_files[pkgname]:
            project_json = []
            if not os.path.exists(f'cache\\{pkgname}_{reqfiles}.npy'):
                valid_project_set = set()
                valid_count = 0 
                base_url = f'https://github.com/search?q=filename%3A{reqfiles}&type=code'
                soup = BeautifulSoup(requests.get(base_url,headers=header).text.__str__(), 'html.parser')
            

                # get total repo number and max page number
                page_tags = soup.find_all('span', class_='v-align-middle')
                for p_page in page_tags:
                    if 'code results' in p_page.text:
                        project_num = read_num(p_page.text)
                        max_page_num = project_num // 10 + 1
                        break

                # get a set of valid project url            
                print(f'{pkgname}->{reqfiles} have {project_num} results')
                for page in range(1, max_page_num+1):
                    time.sleep(SENDING_GAP)
                    print(f'    {pkgname}/{reqfiles} page {page}/{max_page_num} valid:{valid_count}')
                    if valid_count >= MAX_NEEDED_NUM:
                        break
                    paged_base_url = f'https://github.com/search?p={page}&q=filename%3A{reqfiles}&type=Code'
                    soup = BeautifulSoup(requests.get(paged_base_url, headers=header).text.__str__(), 'html.parser')
                    
                    # get list of projects links
                    project_href_list = soup.find_all('a', class_="link-gray")
                    
                    # get tags contains list of required file path
                    reqfile_path_list = soup.find_all(class_="f4 text-normal")
                    if len(project_href_list)==0 or len(reqfile_path_list)==0:
                        pd.DataFrame.from_dict(project_json).to_csv(f'data\\{pkgname}_{reqfiles}.csv', index=False)
                        with open('a.html', 'w',encoding='utf-8') as file_object:
                            file_object.write(str(soup))
                        print("    you are detected!")
                        time.sleep(HIDDING_GAP)
                        break
                    
                    # get pure list of required file path and list of repo href
                    reqfile_path_list = [reqfile_path.find('a')['title'] for reqfile_path in reqfile_path_list]
                    project_href_list = [project_href['href'] for project_href in project_href_list]

                    # filter the invalid projects
                    for ind, (reqfile_path,project_href) in enumerate(zip(reqfile_path_list,project_href_list)):
                        if "example" in reqfile_path.lower() or "test" in reqfile_path.lower() or "sample" in reqfile_path.lower():
                            print(f'        invalid analyzing https://github.com{project_href}')
                        else:
                            print(f'        valid analyzing https://github.com{project_href}')
                            valid_project_set.add(project_href)
                            valid_count = len(valid_project_set)
                np.save(f'cache\\{pkgname}_{reqfiles}.npy',valid_project_set)

            # load set and query project details
            valid_project_set = np.load(f'cache\\{pkgname}_{reqfiles}.npy', allow_pickle=True).item()
            print(f'successfully load {pkgname}_{reqfiles}.npy, set length is {len(valid_project_set)}', )
            
            # read details from valid project set
            for ind, project_ref in enumerate(valid_project_set):
                try:
                    project_meta = {}
                    detail_url = 'https://github.com/' + project_ref
                    detail_page = BeautifulSoup(requests.get(detail_url, headers=header).text.__str__(), 'html.parser')
                    
                    # obtain the project file list
                    project_detail = detail_page.find_all(class_='js-navigation-item')
                    project_detail = [detail.find(class_='content') for detail in project_detail]

                    # find star\watch\fork info
                    star_num = 0
                    watch_num = 0
                    fork_num = 0
                    star_watcher_fork_detail = detail_page.find_all('a',{'class':'social-count'})
                    for swf in star_watcher_fork_detail:
                        if 'starred' in swf['aria-label']:
                            star_num = read_num(swf.text)
                        if 'watching' in swf['aria-label']:
                            watch_num = read_num(swf.text)
                        if 'forded' in swf['aria-label']:
                            fork_num = read_num(swf.text)
                    project_meta['name'] = f'{pkgname}_{reqfiles}'
                    project_meta['stars'] = int(star_num)
                    project_meta['watchers'] = int(watch_num)
                    project_meta['forks'] = int(fork_num)
                    project_meta['repo_link'] = detail_url
                    project_json.append(project_meta)
                    print(f'{ind} {pkgname}_{reqfiles} {detail_url}')
                except Exception as e:
                    print(f'you are detected when visiting {detail_url}!\n{e}')
                    pd.DataFrame.from_dict(project_json).to_csv(f'data\\{pkgname}_{reqfiles}.csv', index=False)
                    time.sleep(HIDDING_GAP)
                finally:
                    time.sleep(SENDING_GAP)
            pd.DataFrame.from_dict(project_json).to_csv(f'data\\{pkgname}_{reqfiles}.csv', index=False)

if __name__ == "__main__":
    # packages_files = {
    # 'maven' : ['pom.xml'],
    # 'gradle' : ['build.gradle'],
    # 'ant' : ['ivy.xml', 'build.xml'],
    # 'npm' : ['package.json','package-lock.json','npm-shrinkwarp.json'],
    # 'yarn' : ['yarn.lock'],
    # 'go-modules' : ['go.mod'],
    # 'pip' : ['setup.py','requirements.txt','pipfile.lock'],
    # 'nuget' : ['.sln'],
    # 'nuget2' : ['packages.config'],
    # 'nuget3' : ['project.json','project.lock.json'],
    # 'nuget4' : ['project.assets.json','.csproj'],
    # 'rubygems' : ['gemfile.lock','gemfile'],
    # 'composer' : ['composer.lock','composer.json'],
    # 'cocoapods' : ['Podfile.lock'],
    # }
    packages_files = {
       'maven' : ['pom.xml']
    }

    
    # try:
    #     _thread.start_new_thread(scraper, (pack1,))
    #     _thread.start_new_thread(scraper, (pack2,))
    # except Exception as e:
    #     print(e)
    #     print("cannot run thread")
    # while 1:
    #   pass
    scraper(packages_files,header=get_user_agent(),proxy=get_random_ip())

