import bs4
import requests
import json


def get_vacancies(url, headers):
    main_response = requests.get(url, headers=headers)
    main_html_data = main_response.text
    main_soup = bs4.BeautifulSoup(main_html_data, "lxml")
    item = main_soup.find("div", id="a11y-main-content")
    items = item.find_all("div", class_="vacancy-search-item__card serp-item_link vacancy-card-container--OwxCdOj5QlSlCBZvSggS vacancy-card_clickme--Ti9glrpeP1wwAE3hAklj")

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
        description_tag = vacancy_soup.find("div", class_="g-user-content")
        description = description_tag.text if description_tag else "Нет описания"
        index_1 = description.find('Django')
        index_2 = description.find('Flask')
        if index_1 != -1 or index_2 != -1:
            parsed_vacancy.append({
                "title": title,
                "link": main_link,
                "salary": salary,
                "company": company,
                "city": city
                })
        return parsed_vacancy
    
def write_vacancy(vacancies):
    with open("parsed_vacancies.json", "w") as f:
        json.dump(vacancies, f, indent=4)


if __name__ == "__main__":
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

    get = get_vacancies(url, headers)
    write_vacancy(get)
    print("Вакансии занесены в файл")
    