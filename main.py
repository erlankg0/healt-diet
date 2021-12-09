from bs4 import BeautifulSoup
import json
import requests
from fake_useragent import UserAgent
from time import sleep
import csv

headers = {"accept": "*/*",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}

url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"


def requesting_url(url: str, header: dict):
    user_agent = UserAgent()
    # link
    link = url
    # header for scraping
    header = header
    # request html code
    req = requests.get(url, headers=header)
    # HTML file
    src = req.text


# def writing_html(name_html: str):
#     with open(f"templates/html/{name_html}.html", 'w', encoding="utf-8") as html_file:
#         html_file.write(src)

#
# writing_html("index")


def scraping_all_title_and_hrefs():
    with open("templates/html/index.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")

    all_categories = {}

    for item in all_products_hrefs:
        item_text = item.text
        item_href = " https://health-diet.ru" + item.get("href")
        print(f"{item_text} : url : {item_href}")

        all_categories[item_text] = item_href

    return all_categories


def write_json(name: str, json_object: dict):
    with open(f"templates/json/{name}.json", 'w', encoding='utf-8') as file:
        json.dump(json_object, file, indent=4, ensure_ascii=False)
        # парамент indent это отступ ensure_ascii не экраниует помогает работать с кирилицей


def replace_char_in_json():
    count = 0
    with open("templates/json/categpries.json", encoding="utf-8") as file:
        all_categories = json.load(file)
    iteration_categories = int(len(all_categories) - 1)
    print('Вам нужно ли создать html файлы ? 1 для записи 2 для чтения!')
    try:
        question = int(input())
        try:
            if question == 1:
                for category_name, category_href in all_categories.items():
                    replace_chars = [" ", ",", ".", "-", "'"]
                    for item in replace_chars:
                        if item in replace_chars:
                            count += 1
                            category_name = category_name.replace(item, "_")

                            giving_html_by_category(category_name, category_href)
                            print(f"finished {count}")

            else:
                for category_name, category_href in all_categories.items():
                    replace_chars = [" ", ",", ".", "-", "'"]
                    for item in replace_chars:
                        if item in replace_chars:
                            category_name = category_name.replace(item, "_")
                            if count == iteration_categories:
                                break
                            else:
                                scraping_by_category(category_name, category_href)

                                print(f"count {count}: name {category_name}")
        except Exception as error:
            print(f"Error {error}")

    except ValueError as error:
        print(f"Ошибка принимать только числа один или два")


def giving_html_by_category(category_name, category_href):
    req = requests.get(category_href, headers=headers)
    src = req.text

    with open(f"templates/html1/{category_name}.html", 'w', encoding='utf-8') as file:
        file.write(src)


def scraping_by_category(category_name, category_href):
    req = requests.get(category_href, headers=headers)
    src = req.text

    with open(f"templates/html/{category_name}.html", encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    try:
        # собирает заголовки таблицы

        table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
        product = table_head[0].text
        calories = table_head[1].text
        proteins = table_head[2].text
        fats = table_head[3].text
        carbohydrates = table_head[4].text

        with open(f"templates/csv/{category_name}.csv", 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    product,
                    calories,
                    proteins,
                    fats,
                    carbohydrates,
                ]
            )
        # Собирает данные продуктов
        products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

        for item in products_data:
            products_tds = item.find_all("td")

            title = products_tds[0].text
            calories = products_tds[1].text
            proteins = products_tds[2].text
            fats = products_tds[3].text
            carbohydrates = products_tds[4].text

            with open(f"templates/csv/{category_name}.csv", 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        title,
                        calories,
                        proteins,
                        fats,
                        carbohydrates,
                    ]
                )
    except Exception as error:
        print(error)


if __name__ == '__main__':
    # for_json = scraping_all_title_and_hrefs()
    replace_char_in_json()
    # write_doc_json = write_json('categpries', for_json)
