from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
import pandas as pd
import DB_connection

driver = webdriver.Chrome('./chromedriver')

driver.get("http://oasis.krei.re.kr/basicInfo/etc/kma.do")

driver.implicitly_wait(3)

driver.find_element_by_id('sCalendar').click()
driver.find_element_by_id('sCalendar').clear()

yesterday = datetime.now() - timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')

driver.find_element_by_id('sCalendar').send_keys(yesterday)

driver.implicitly_wait(3)

driver.find_element_by_id('search2').click()

select = Select(driver.find_element_by_id('pageUnit'))
select.select_by_value('500')

results_table = []
rows = driver.find_elements_by_css_selector(".data_table tbody tr")

for row in rows:

    temp = []
    columns = row.find_elements_by_css_selector("td")

    for column in columns:

        temp.append(column.text)

    results_table.append(temp)

data = pd.DataFrame(results_table)

#1,4,5,8,9,10,11,12
del data[1], data[4], data[5], data[8], data[9], data[10], data[11], data[12]

#고창군, 안동시, 고흥군, 의성군, 신안군
data = data[data[2].isin(["고창군", "안동시", "고흥군", "의성군", "신안군"])]

data.loc[data[2] == "고창군", 2] = "Gochang"
data.loc[data[2] == "고흥군", 2] = "Goheung"
data.loc[data[2] == "신안군", 2] = "Sinan"
data.loc[data[2] == "안동시", 2] = "Andong"
data.loc[data[2] == "의성군", 2] = "Uiseong"

data.columns=["days", "region", "temperature", "rainfall", "daylight"]

yesterday = datetime.now() - timedelta(days=1)
weeks = yesterday.isocalendar()[1]
data['weeks'] = weeks

data.sort_values(by=['region'], axis=0,inplace=True)
data.reset_index(drop=True, inplace=True)

data['temperature'] = pd.to_numeric(data['temperature'])
data['rainfall'] = pd.to_numeric(data['rainfall'])
data['daylight'] = pd.to_numeric(data['daylight'])
del data['days'], data['weeks']




conn = DB_connection.engine.connect()
weatherData = pd.read_sql_table('weather', conn)
average = weatherData.groupby([weatherData["region"], weatherData["weeks"]], as_index=False).mean()

average = average[average['weeks'] == weeks]
average.sort_values(by=['region'], axis=0,inplace=True)
average.reset_index(drop=True, inplace=True)
del average['weeks']
average = average[['region','temperature','rainfall', 'daylight']]




temperature = abs(data['temperature'] - average['temperature'])
for i in temperature.index:
    if temperature[i] <= 1.5:
        temperature[i] = 0
    elif 1.5 < temperature[i] <= 3.0:
        temperature[i] = 1
    else:
        temperature[i] = 2

rainfall = abs(data['rainfall'] - average['rainfall'])
for i in rainfall.index:
    if rainfall[i] <= 3.0:
        rainfall[i] = 0
    elif 3.0 < rainfall[i] <= 6.0:
        rainfall[i] = 1
    else:
        rainfall[i] = 2

daylight = abs(data['daylight'] - average['daylight'])
for i in daylight.index:
    if daylight[i] <= 1.5:
        daylight[i] = 0
    elif 1.5 < daylight[i] <= 3.0:
        daylight[i] = 1
    else:
        daylight[i] = 2

array = {'temperature': temperature,
        'rainfall': rainfall,
        'daylight': daylight}

danger = pd.DataFrame(array)
danger.to_json()
print(danger)


