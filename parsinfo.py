import requests
from bs4 import BeautifulSoup as bs4

def parser_services(url = 'https://it.omz.ru/'):
    request_cite = requests.get(url)
    soup = bs4(request_cite.text, 'html.parser')
    services = soup.find_all('div', class_='wb_element wb_text_element')
    clear_services = [i.text for i in services]
    return f'{clear_services[2]}\n{clear_services[3]}\n{clear_services[4]}'

def parser_manager(url = 'https://it.omz.ru/administration/'):
    request_adm = requests.get(url)
    soup = bs4(request_adm.text, 'html.parser')
    administration = soup.find_all('p', class_='wb-stl-custom13')
    clear_adm = [i.text for i in administration]
    return '\n'.join(clear_adm)

