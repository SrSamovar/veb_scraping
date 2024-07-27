import bs4
import requests
import json


def pars_vacancies(url, headers, params):
    main_response = requests.get(url, params=params, headers=headers)
    main_html_data = main_response.text
    main_soup = bs4.BeautifulSoup(main_html_data, "lxml")
    item = main_soup.find("div", id="a11y-main-content")
    items = item.find_all("div", class_="vacancy-search-item__card serp-item_link vacancy-card-container--OwxCdOj5QlSlCBZvSggS")

    parsed_vacancy = []

    for vacancy_tag in items:
        h2_tag = vacancy_tag.find("h2", class_="bloko-header-section-2")
        title = h2_tag.text

        a_tag = h2_tag.find("a", class_ = "bloko-link")
        main_link = a_tag["href"]

        vacancy_response = requests.get(main_link, headers=headers)
        vacancy_html_data = vacancy_response.text
        vacancy_soup = bs4.BeautifulSoup(vacancy_html_data, "lxml")

        salary_tag = vacancy_soup.find("span", class_="magritte-text___pbpft_3-0-12 magritte-text_style-primary___AQ7MW_3-0-12 magritte-text_typography-label-1-regular___pi3R-_3-0-12")
        salary = salary_tag.text if salary_tag else "Не указана"
        company_tag = vacancy_soup.find("span", class_="bloko-header-section-2 bloko-header-section-2_lite")
        company = company_tag.text if company_tag else "Не указано"
        city_tag = vacancy_soup.find("span", {"data-qa": "vacancy-view-raw-address"})
        city = city_tag.text if city_tag else "Не указано"
        parsed_vacancy.append({
            "title": title,
            "link": main_link,
            "salary": salary,
            "company": company,
            "city": city
            })
    return parsed_vacancy
    
def write_vacancy(vacancies):
    if not vacancies:
        print("Нет найденных вакансий")
        return
    with open('vacancy.json', 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)
        print("Данные занесены в файл")



if __name__ == "__main__":
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    base_url = "https://spb.hh.ru/search/vacancy"
    params = {
        "text": "python, django, flask",
        "area": [1,2],
    }
    get = pars_vacancies(base_url,headers, params)
    write_vacancy(get)
    