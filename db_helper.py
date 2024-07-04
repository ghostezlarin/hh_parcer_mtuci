#импорт библиотек и дополнительных модулей
import psycopg2
import types
from SQL_code import const_salary_from, const_salary_to, const_resumes_all, const_resumes_zero, \
    const_with_salary
from connection_db_constant import user, password, host, port, database

#функция записи в таблицу связанную с парсингом сайта api.hh.ru
def write_to_hh_table(dict_of_fields: dict, request_id: int):
    hh_id: int = 0
    hh_name: str = ""
    hh_salary_null: int = 0
    hh_salary_from: int = 0
    hh_salary_to: int = 0
    hh_schedule: str = ''
    hh_employment: str = ''
    error_code: int = 0
    error_description: str = ''
    connection = 0
    try:
        hh_id = dict_of_fields["id"]
        # print(hh_id)

        hh_name = dict_of_fields["name"]
        # print(hh_name)

        if not (isinstance(dict_of_fields["salary"], types.NoneType)):
            if not (isinstance(dict_of_fields["salary"]["from"], types.NoneType)):
                hh_salary_from = dict_of_fields["salary"]["from"]

            if not (isinstance(dict_of_fields["salary"]["to"], types.NoneType)):
                hh_salary_to = dict_of_fields["salary"]["to"]
            # print(hh_salary_from)
            # print(hh_salary_to)
        else:
            hh_salary_null = 1

        if not (isinstance(dict_of_fields["schedule"], types.NoneType)):
            hh_schedule = dict_of_fields["schedule"]["name"]
        # print(hh_schedule)

        if not (isinstance(dict_of_fields["employment"], types.NoneType)):
            hh_employment = dict_of_fields["employment"]["name"]
        # print(hh_employment)

        # print('---------------------------------------------')
    except Exception as e:
        error_code = -6
        error_description = e.__str__()
        print("Error qqq")
        print(error_description)
        print(dict_of_fields)
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
    except Exception as e:
        error_code = -3
        error_description = e.__str__()
        print(error_description)

    if error_code == 0:
        try:
            cursor = connection.cursor()
            insert_query = """INSERT INTO hh_table (status, hh_id, hh_name, hh_salary_null,  hh_salary_from, hh_salary_to, hh_employment, hh_schedule, request_id) VALUES (1, %s, %s, %s, %s, %s, %s, %s, %s)"""
            record_to_insert = (
                hh_id, hh_name, hh_salary_null, hh_salary_from, hh_salary_to, hh_employment, hh_schedule, request_id)
            cursor.execute(insert_query, record_to_insert)
            connection.commit()
        except Exception as e:
            print(e.__str__())
            error_code = -6
            error_description = e.__str__()

        connection.close()

    return {"error_code": error_code, "error_description": error_description}

#Функиця записи данных о пользователе(Его telegram id, а также содержание запроса) в датабазу, для дальнейшей аналитики
def write_to_telegram_db(telegram_id: int, text: str, salary: int, employment: str):
    error_code: int = 0
    error_description: str = ""
    connection = 0
    request_id: int = 0
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
    except Exception as e:
        error_code = -8
        error_description = 'No connection with DB'
        return {"error_code": error_code, "error_description": error_description}

    if error_code == 0:
        try:
            cursor = connection.cursor()
            insert_query = """INSERT INTO telegram_bot_table (telegram_id, text, salary, employment) VALUES (%s, %s, %s, %s) RETURNING id"""
            record_to_insert = (telegram_id, text, salary, employment)
            cursor.execute(insert_query, record_to_insert)
            request_id = cursor.fetchone()[0]
            connection.commit()
        except Exception as e:
            error_code = -7
            error_description = e.__str__()
            print("rrrrrr")
            return {"error_code": error_code, "error_description": error_description}
        connection.close()
    return request_id


def get_analytics(message_chat_id: int):
    connection = 0
    r = {
        "min_salary_from": 0,
        "max_salary_from": 0,
        "avg_salary_from": 0,
        "min_salary_to": 0,
        "max_salary_to": 0,
        "avg_salary_to": 0,
        "resumes_count": 0,
        "resumes_zero": 0,
        "resumes_with_salary": 0,
        "resumes_static_zero_analytic": 0,
        "resumes_with_salary_analytic": 0,
        "error_code": 0,
        "error_description": "",
    }
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
    except Exception as e:
        r["error_code"] = 9
        r["error_description"] = e.__str__()
        return r

    if r["error_code"] == 0:
        try:
            cursor = connection.cursor()
            telegram_check = """SELECT id FROM public.telegram_bot_table WHERE telegram_id = %s ORDER BY id DESC LIMIT 1;"""
            cursor.execute(telegram_check, (message_chat_id,))
            t = cursor.fetchone()
            print(t)
            if isinstance(t, tuple):
                print("isinstance(t, tuple)")
                request_id = t[0]
            else:
                print("!isinstance(t, tuple)")

                r["error_code"] = -11
                r["error_description"] = "!isinstance(t, tuple)"
                return r

            print(request_id)

            resumes_all_check = const_resumes_all
            cursor.execute(resumes_all_check, (request_id,))
            resumes_all = cursor.fetchone()[0]
            print(resumes_all)

            if resumes_all == 0:
                r["error_code"] = -12
                r["error_description"] = "Не найдено не одной записи"
                return r

            salary_from_check = const_salary_from
            cursor.execute(salary_from_check, (request_id, request_id))
            salary_from = cursor.fetchall()[0]
            print(salary_from)

            salary_to_check = const_salary_to
            cursor.execute(salary_to_check, (request_id, request_id))
            salary_to = cursor.fetchall()[0]
            print(salary_to)

            resumes_zero_check = const_resumes_zero
            cursor.execute(resumes_zero_check, (request_id,))
            resumes_zero = cursor.fetchone()[0]
            print(resumes_zero)

            resumes_with_salary_check = const_with_salary
            cursor.execute(resumes_with_salary_check, (request_id,))
            resumes_with_salary = cursor.fetchone()[0]
            print(resumes_with_salary)

            resumes_static_zero_analytic = round(resumes_zero / resumes_all * 100, 2)
            resumes_with_salary_analytic = round(resumes_with_salary / resumes_all * 100, 2)

            print(resumes_with_salary_analytic)
            print(resumes_static_zero_analytic)

            connection.close()

            return {
                "min_salary_from": salary_from[0],
                "max_salary_from": salary_from[1],
                "avg_salary_from": round(salary_from[2]),
                "min_salary_to": salary_to[0],
                "max_salary_to": salary_to[1],
                "avg_salary_to": round(salary_to[2]),
                "resumes_count": resumes_all,
                "resumes_zero": resumes_zero,
                "resumes_with_salary": resumes_with_salary,
                "resumes_static_zero_analytic": resumes_static_zero_analytic,
                "resumes_with_salary_analytic": resumes_with_salary_analytic,
                "error_code": r["error_code"],
                "error_description": r["error_description"],
            }

        except Exception as e:
            error_code = -10
            error_description = e.__str__
            print(e)
            return {
                "min_salary_from": 0,
                "max_salary_from": 0,
                "avg_salary_from": 0,
                "min_salary_to": 0,
                "max_salary_to": 0,
                "avg_salary_to": 0,
                "resumes_count": 0,
                "resumes_zero": 0,
                "resumes_with_salary": 0,
                "resumes_static_zero_analytic": 0,
                "resumes_with_salary_analytic": 0,
                "error_code": error_code,
                "error_description": error_description}


def write_data_to_db(list_of_dict: list, request_id: int):
    r = {"error_code": 0, "error_description": ""}
    try:
        print("start write_data_to_db.")
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database,
                                      )
        print("Connection ready.")
        for i in range(len(list_of_dict)):
            hh_id: int = 0
            hh_name: str = ""
            hh_salary_null: int = 0
            hh_salary_from: int = 0
            hh_salary_to: int = 0
            hh_schedule: str = ''
            hh_employment: str = ''
            try:
                hh_id = list_of_dict[i]["id"]
                hh_name = list_of_dict[i]["name"]

                if not (isinstance(list_of_dict[i]["salary"], types.NoneType)):
                    if not (isinstance(list_of_dict[i]["salary"]["from"], types.NoneType)):
                        hh_salary_from = list_of_dict[i]["salary"]["from"]

                    if not (isinstance(list_of_dict[i]["salary"]["to"], types.NoneType)):
                        hh_salary_to = list_of_dict[i]["salary"]["to"]

                else:
                    hh_salary_null = 1

                if not (isinstance(list_of_dict[i]["schedule"], types.NoneType)):
                    hh_schedule = list_of_dict[i]["schedule"]["name"]

                if not (isinstance(list_of_dict[i]["employment"], types.NoneType)):
                    hh_employment = list_of_dict[i]["employment"]["name"]

            except Exception as e:
                r["error_code"] = -2
                r["error_description"] = "{1FA3BCB5-62EA-44BA-9DDE-1D03CF33E27C} " + e.__str__()
                print(f"1FA3BCB5-62EA-44BA-9DDE-1D03CF33E27C {e}")
                print(list_of_dict[i])
                return r

            if r["error_code"] == 0:
                try:
                    cursor = connection.cursor()
                    insert_query = """INSERT INTO hh_table (status, hh_id, hh_name, hh_salary_null,  hh_salary_from, hh_salary_to, hh_employment, hh_schedule, request_id) VALUES (1, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    record_to_insert = (
                        hh_id, hh_name, hh_salary_null, hh_salary_from, hh_salary_to, hh_employment, hh_schedule,
                        request_id)
                    cursor.execute(insert_query, record_to_insert)
                    # connection.commit()
                except Exception as e:
                    r["error_code"] = -3
                    r["error_description"] = "{6C44F05A-69AA-4D9F-9AB6-7036CCA2B0D9} " + e.__str__()
                    print(f"6C44F05A-69AA-4D9F-9AB6-7036CCA2B0D9 {e}")
                    return r

        connection.commit()
        connection.close()
    except Exception as e:
        r["error_code"] = -1
        r["error_description"] = "{47F19C67-FCD7-4756-962B-1DC8F3B14EC9} " + e.__str__()
        print(f"47F19C67-FCD7-4756-962B-1DC8F3B14EC9 {e}")
    return r

# if __name__ == "__main__":
#     print(get_analytics(894498333))
