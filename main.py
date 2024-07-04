#импорт библиотек и модулей
import telebot
import re
from db_helper import get_analytics
from api_hh import get_data_all

#токен бота
token = "*"

#инициализация бота
bot = telebot.TeleBot(f"{token}")

#словарь для просмотра сесси пользователя
sessions: dict = {}

#словарь с переменными для параметров запроса на api.hh.ru
employment_dict = {"1": "full", "2": "part", "3": "project", "4": "volunteer", "5": "probation"}

#Функция для проверки является ли введеная строка числом
def Is_Int(s: str):
    try:
        int(s)
        return True
    except ValueError:
        return False

#обработка команды /start и /help
@bot.message_handler(commands=["start", "help"])
def send_help(message):
    bot.reply_to(message, "Для парсинга в БД по вашему запросу - введите:\n/search \n\n"
                          "Для получения аналитики - введите:\n/analytics ")

#Команда для мини игры /slots, является функцией для проверки работоспособности бота
@bot.message_handler(commands=["slots"])
def slots(message):
    try:
        print(f"id:{message.chat.id}; text: {message.text};")
        bot.send_dice(message.chat.id, '\U0001F3B0')
    except Exception as e:
        print(e.__str__())

#обработка команды /search
@bot.message_handler(commands=["search"])
def search(message):
    try:
        print("search")
        chat_id = message.chat.id

        if not (str(chat_id) in sessions):
            sessions[f"{chat_id}"] = {"state": "", "text": "", "salary": "", "employment": ""}

        sessions[f"{chat_id}"]["state"] = "search_step1"

        print(sessions[f"{chat_id}"])

        bot.reply_to(message, "Введите название вакансии.")

    except Exception as e:
        print("exexe")
        print(e.__str__())

#функция обработки /analytics
@bot.message_handler(commands=["analytics"])
def analytics(message):
    try:
        id_telegram = message.chat.id
        analytics_answer = get_analytics(id_telegram)
        print(analytics_answer)
        if analytics_answer["error_code"] == 0:
            bot.reply_to(message, f"Минимальная зарплата от: {analytics_answer["min_salary_from"]}\n"
                                  f"Максимальная зарплата от: {analytics_answer["max_salary_from"]}\n"
                                  f"Средняя зарплата от: {analytics_answer["avg_salary_from"]}\n"
                                  f"Минимальная зарплата от: {analytics_answer["min_salary_to"]}\n"
                                  f"Максимальная зарплата от: {analytics_answer["max_salary_to"]}\n"
                                  f"Средняя зарплата от: {analytics_answer["avg_salary_to"]}\n"
                                  f"Колличество найденых вакансий: {analytics_answer["resumes_count"]}\n"
                                  f"Колличество пустых вакансий и их процент: {analytics_answer["resumes_zero"]}; {analytics_answer["resumes_static_zero_analytic"]}%\n"
                                  f"Колличество вакансий с зарплатой и их процент: {analytics_answer["resumes_with_salary"]}; {analytics_answer["resumes_with_salary_analytic"]}%")
        else:
            if analytics_answer["error_code"] == -12:
                bot.reply_to(message, "По последнему запросу не найдено ни одной вакансии.")
            else:
                bot.reply_to(message,
                             "Ошибка. Перед вводом команды /analytics , выполните поиск нужной вакансии с помощью команды /search .")
    except Exception as e:
        print(e.__str__())


# Декоратор для обработки текстовых сообщений Telegram бота.
@bot.message_handler(content_types=['text'])
def all_messages(message):
    try:
        print("text message")

        if re.match('/', message.text):
            return

        chat_id = message.chat.id

        if not (str(chat_id) in sessions):
            sessions[f"{chat_id}"] = {"state": "", "text": "", "salary": "", "employment": ""}

        if sessions[f"{chat_id}"]["state"] == "search_step1":
            if not Is_Int(message.text):
                sessions[f"{chat_id}"]["state"] = "search_step2"
                sessions[f"{chat_id}"]["text"] = message.text
                bot.reply_to(message, "Введите ожидаемую зарплату (целое число).")
            else:
                bot.reply_to(message, "Некорректный ввод. Повторно напишите название вакансии.")

            print(sessions[f"{chat_id}"])
            return

        if sessions[f"{chat_id}"]["state"] == "search_step2":
            if Is_Int(message.text):
                if int(message.text) >= 0:
                    sessions[f"{chat_id}"]["state"] = "search_step3"
                    sessions[f"{chat_id}"]["salary"] = message.text
                    bot.reply_to(message, "Введите цифру,соотвествующую типу занятости.\n"
                                          "1: Полная занятость \n"
                                          "2: Частичная занятость \n"
                                          "3: Проектная работа \n"
                                          "4: Волонтерство \n"
                                          "5: Стажировка")
                else:
                    bot.reply_to(message, "Некорректный ввод. Введите целое положительное число.")
            else:
                bot.reply_to(message, "Некорректный ввод. Введите целое положительное число.")
            print(sessions[f"{chat_id}"])
            return

        if sessions[f"{chat_id}"]["state"] == "search_step3":
            if message.text in employment_dict:
                sessions[f"{chat_id}"]["state"] = "done"
                sessions[f"{chat_id}"]["employment"] = employment_dict[f"{message.text}"]
                bot.reply_to(message, "Запрос данных hh.ru принят.")
                get_data_all(sessions[f"{chat_id}"]["text"], sessions[f"{chat_id}"]["salary"],
                             sessions[f"{chat_id}"]["employment"], chat_id)
                bot.reply_to(message, "Запрос данных hh.ru  исполнен.")
            else:
                bot.reply_to(message, "Некорректный ввод. Введите нужную цифру.")

            print(sessions[f"{chat_id}"])
            return

        send_help(message)


    except Exception as e:
        print(e.__str__())
        bot.reply_to(message, "Ошибка. Повторите запрос.")


def main():
    print("Start")
    while 1 == 1:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e.__str__())


if __name__ == "__main__":
    main()
