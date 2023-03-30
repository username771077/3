# Импортируем необходимые библиотеки
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# Определяем URL и диапазон дат для парсинга
url = 'https://tv.yandex.ru/'
start_date = datetime.now().date()
end_date = start_date + timedelta(days=30)

# Создаем список для хранения программ
programs = []

# Осуществляем парсинг телепрограммы за диапазон дат
for single_date in pd.date_range(start_date, end_date):
    date_str = single_date.strftime('%Y-%m-%d')
    response = requests.get(url + 'channel/1/day/' + date_str)
    soup = BeautifulSoup(response.content, 'html.parser')
    for item in soup.select('.channel-schedule__event'):
        program = {}
        program['title'] = item.select_one('.channel-schedule__text').get_text(strip=True)
        program['time'] = item.select_one('.channel-schedule__time').get_text(strip=True)
        program['date'] = date_str
        programs.append(program)

# Создаем датафрейм из списка программ
df = pd.DataFrame(programs)

# Отображаем результаты
print(df.head())