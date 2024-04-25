import requests
import xml.etree.ElementTree as ET


def get_cny():

    url = "https://www.cbr-xml-daily.ru/daily.xml"


    response = requests.get(url)


    if response.status_code == 200:

        xml_content = response.content
        
        root = ET.fromstring(xml_content)
        
        for currency in root.findall('.//Valute'):
            if currency.find('CharCode').text == 'CNY':
                rub_rate = round(float(currency.find('Value').text.replace(',', '.')), 2)
                rub_rate_plus = round(rub_rate * 0.07) + rub_rate
                return {'rub_rate':rub_rate, 'rub_rate_plus':rub_rate_plus}
    else:
        return "Ошибка при запросе XML:", response.status_code

print(get_cny())