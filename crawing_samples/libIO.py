import requests
from bs4 import BeautifulSoup
import pandas as pd



def scraper(platform, pages, rank_score, MODE):
    project_json = []
    for page_num in range(pages[0], pages[1]):
        # page_num = 4

        if MODE == 0:
            #download by platform
            base_url = 'https://libraries.io/search?languages=C&order=desc&' + 'page=' + str(
                page_num) + '&platforms=' + platform + '&sort=' + rank_score
            print(base_url)
        elif MODE == 1: #download by keywords
            base_url = 'https://libraries.io/search?keywords='+ platform \
                       +'&order=desc' + '&page='+str(page_num) +'&sort='+rank_score
            print(base_url)


        page = requests.get(base_url)

        soup = BeautifulSoup(page.text.__str__(), 'html.parser')

        project_list = soup.find_all(class_="project")
        # project_list = soup.find('div', attrs={'class':'project'})
        # print(project_list)
        # project_list_items = project_list.find_all('a')

        for project in project_list:
            project_meta = {}

            href_tag = project.find('a', href=True)
            detail_url = 'https://libraries.io/' + href_tag['href']
            project_meta['name'] = href_tag.contents[0]

            detail_page = BeautifulSoup(requests.get(detail_url).text, 'html.parser')
            project_detail = detail_page.find(class_='project-links')
            links = project_detail.find_all('a', href=True)
            if len(links) < 2:
                continue
            project_meta['homepage'] = links[0]['href']
            if str(project_meta['homepage']).startswith('https://github.com/'):
                project_meta['repo_link'] = links[0]['href']
                project_meta['pkg_link'] = links[1]['href']
            else:
                if len (links) > 2:
                    project_meta['repo_link'] = links[1]['href']
                    project_meta['pkg_link'] = links[2]['href']
                else:
                    project_meta['repo_link'] = ''
                    project_meta['pkg_link'] = links[0]['href']

            table = detail_page.find_all('dl', {'class': 'row'})[1]
            column_names = table.find_all('dt', {'class': 'col-xs-8'})

            names = []
            for cn in column_names:
                names.append(cn.text.strip())

            column_values = table.find_all('dd', {'class': 'col-xs-4'})
            values = []
            for name, value in zip(names, column_values):
                tmp = value.find('a', href=True)
                if tmp is not None:
                    values.append(tmp.text.strip())
                    project_meta[name] = tmp.text.strip()
                else:
                    values.append(value.text.strip())
                    project_meta[name] = value.text.strip()
            # print(column_nvalames)

            # print(names, values)
            print(project_meta)
            project_json.append(project_meta)


    if MODE == 0:
        save_path = './mostUsedLibs/'\
                    +platform + 'C_project_' + str(pages[0])  +'-' + str(pages[1]-1) + '_pages.csv'
    else:
        save_path = './keywords/' \
                    +platform + '_project_' + str(pages[0])  +'-' + str(pages[1]-1) + '_pages.csv'

    pd.DataFrame.from_dict(project_json).to_csv(save_path, index=False)

if __name__ == '__main__':



    # platforms = ['NPM', 'Maven', 'PyPI', 'Rubygems', 'Go', 'NuGet', 'Packagist', 'cocoapods']
    platforms=['Homebrew']
    score = 'dependents_count' #'dependent_repos_count'  # rank
    pages = [11,20]
    MODE = 0
    for platform in platforms:
        scraper(platform, pages, score, MODE )

    # keywords = [#'docker',
    #             #'blockchain',
    #             #'web',
    #             #'framwork',
    #             #'ios',
    #             #'api',
    #             #'plugin',
    #             #'database',
    #             'browser',
    #             'security',
    #             'deep-learning', 'machine-learning']
    # score = 'dependent_repos_count'
    # MODE = 1
    # pages = [1, 5]
    # for kw in keywords:
    #     print('Getting libraries on the topic '+kw)
    #     scraper(kw, pages, score, MODE)


