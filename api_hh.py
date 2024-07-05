#импорт библиотек
import db_helper
import requests
import json

#функция получения всех страниц по HTTP запрос к api.hh.ru
def get_data_all(text: str, salary: str, employment: str, telegram_id: int):
    print("Start get_data_all")
    error_code = 0
    error_description = ''
    request_id = db_helper.write_to_telegram_db(telegram_id, text, salary, employment)
    if request_id == 0:
        return {"error_code": error_code, "error_description": error_description}
    try:
        for i in range(0, 20):
            print(f"Page:{i}")
            p = get_data_page(text, salary, employment, i, 1, request_id)
            if p["data"] < 100:
                break
    except Exception as e:
        error_code = -5
        error_description = e.__str__()
        print(f"get_data_all Exception: {error_description}")
    return {"error_code": error_code, "error_description": error_description}

#Функция получения нужной нам информации со страницы
def get_data_page(text: str, salary: str, employment: str, page: int, telegram_id: int, request_id: int):
    url = "https://api.hh.ru/vacancies/"
    r = {"error_code": 0, "error_description": "", "data": 0}
    params = {
        "salary": f"{salary}",
        "employment": f"{employment}",
        "text": f"{text}",
        "per_page": 100,
        "page": page
    }
    result = ""
    data = {}
    name_dict = {}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            result = response.text
            data = json.loads(result)["items"]
            print(f"Число записей на странице: {len(data)}")
            if len(data) > 0:
                db_helper.write_data_to_db(data, request_id)
                r["data"] = len(data)
            return r
        else:
            r["error_code"] = -1
            r["error_description"] = "response != 200"
            print(r["error_description"], f"response.status_code={response.status_code}")
            return r
    except Exception as e:
        r["error_code"] = -2
        r["error_description"] = e.__str__()
        print(f"get_data_page Exception: {r['error_description']}")
    return r

#функция обработки записи в датабазу
def write_data_to_db(list_of_dict: list, request_id: int):
    try:
        for i in range(len(list_of_dict)):
            db_helper.write_to_hh_table(list_of_dict[i], request_id)
    except Exception as e:
        error_code = -6
        error_description = e.__str__()
        print(f"write_data_to_db Exception: {error_description}")
    return


if __name__ == "__main__":
    get_data_all("Программист python", 1000000, "probation", 1)
