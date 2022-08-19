import requests
from bs4 import BeautifulSoup
import fake_useragent

VAC_ON_PAGE = 100

user = fake_useragent.UserAgent().random
headres = {
    'user-agent': user
}

def extract_max_page(link):
    pages = []
    responce = requests.get(link, headers=headres).text
    soup = BeautifulSoup(responce, 'lxml')

    # find max_page
    paginator = soup.find_all('span', class_='pager-item-not-in-short-range')
    for p in paginator:
        pages.append(int(p.find('a').text))
    return pages[-1]


def extaxt_vacancy(max_page, keyword):
    jobs = []
    count = 0
    for page in range(max_page):
        print(f'Парсинг страница {page}')
        responce = requests.get(f'https://hh.ru/search/vacancy?text={keyword}&salary=&currency_code=RUR&experience'
                                f'=doesNotMatter&order_by=relevance&search_period=0&items_on_page={VAC_ON_PAGE}&no_magic=true'
                                f'&L_save_area=true&page={page}&hhtmFrom=vacancy_search_list',
                                headers=headres)

        soup = BeautifulSoup(responce.text, 'lxml')
        vacancy = soup.find_all('div', class_='serp-item')
        for vac in vacancy:
            count += 1
            title = vac.find('a').text
            link = vac.find('a')['href']
            company = vac.find('div', class_='vacancy-serp-item__meta-info-company').text
            city = vac.find_all('div', class_='bloko-text')[1].text.partition(',')[0]
            jobs.append({'title': title, 'company': company, 'city': city, 'link': link})
    return jobs

def get_jobs(keyword):
    link = f'https://hh.ru/search/vacancy?text={keyword}&salary=&currency_code=RUR&experience=doesNotMatter&order_by=' \
           f'relevance&search_period=0&items_on_page={VAC_ON_PAGE}&no_magic=true&L_save_area=true&page=0&hhtmFrom=vacancy_search_list'
    max_page = extract_max_page(link)
    jobs = extaxt_vacancy(max_page, keyword)
    return jobs