from selenium import webdriver
import os,re,urllib
import requests,json
from lxml import html
import urllib.parse as urlparse
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from configparser import ConfigParser
parser = ConfigParser()
parser.read('config.ini')

headers = {
                        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90"
            }
phantomjs_path="phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe"
driver = webdriver.PhantomJS(executable_path=phantomjs_path, service_log_path=os.path.devnull)

def email_id(company_name):
    """
    Function to extract email of a company from zauba corp
    :param company_name: name of the company for which we have to extract
    :return: returns email id of the company
    """
    #Using google.com for extracting relevant link
    link_="https://www.google.com/search?q="+str(company_name)+" zauba corp&start=0"
    driver.get(link_)
    results = driver.find_elements_by_css_selector('div.g')
    link = results[0].find_element_by_tag_name("a")
    href = link.get_attribute("href")
    url=urlparse.parse_qs(urlparse.urlparse(href).query)["q"]
    f = urllib.request.urlopen(url[0])
    s = f.read().decode('utf-8')
    #Regex for extractiong email id from zauba corp
    return (re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s)[0])


def employee(company_name):
    """
    Function to return employee strength for a company from linkedin.
    :param company_name: name of the company for which we have to extract
    :return: Employee strength
    """
    link_="https://www.google.com/search?q="+str(company_name)+" linkedin&start=0"
    driver.get(link_)
    results = driver.find_elements_by_css_selector('div.g')
    link = results[0].find_element_by_tag_name("a")
    href = link.get_attribute("href")
    url=urlparse.parse_qs(urlparse.urlparse(href).query)["q"]
    response = requests.get(url[0],headers=headers,verify=False)
    formatted_response = response.content.decode('utf-8').replace('<!--', '').replace('-->', '')
    doc = html.fromstring(formatted_response)
    datafrom_xpath = doc.xpath('//code[@id="stream-promo-top-bar-embed-id-content"]//text()')
    content_about = doc.xpath('//code[@id="stream-about-section-embed-id-content"]')
    if not content_about:
        content_about = doc.xpath('//code[@id="stream-footer-embed-id-content"]')
    try:
        json_formatted_data = json.loads(datafrom_xpath[0])
        size = json_formatted_data['size'] if 'size' in json_formatted_data.keys() else "Not Found"
        return size
    except:
        return "Not Found"
        
def industry_category(company_name):
    """
    Function to return industry category, revenue, profit from tofler.
    :param company_name: name of the company for which we have to extract
    :return: Dict containing industry category, revenue and profit
    """
    link_="https://www.google.com/search?q="+str(company_name)+" tofler&start=0"
    driver.get(link_)
    results = driver.find_elements_by_css_selector('div.g')
    link = results[0].find_element_by_tag_name("a")
    href = link.get_attribute("href")
    url=urlparse.parse_qs(urlparse.urlparse(href).query)["q"]
    print(url[0])
    f = urllib.request.urlopen(url[0])
    s = f.read().decode('utf-8')
    soup = BeautifulSoup(s, 'lxml')
    table = soup.findAll('div',attrs={"class":"l4 m6 s12 col"})
    data={}
    try :
        for x in table:
            if x.find('h5').text=="INDUSTRY*":
                data['industry']=(x.find('p').text)
    except:
        data['industry']="Not found"
    table = soup.findAll('div',attrs={"class":"s6 m3 col table-box"})
    try:
        data['revenue']=table[0].find('span').text
        table = soup.findAll('div',attrs={"class":"s6 m3 col table-box s-right"})
        data['profit']=table[0].find('span').text
    except:
        data['revenue']="Not found"
        data['profit']="Not found"
    return data
    
    
def naukri(company_name):
    """
    Function to return no. of position on naukri.com
    :param company_name: name of the company for which we have to extract
    :return: Number of open position on naukri.com
    """
    link_="https://www.google.com/search?q="+str(company_name)+" naukri.com&start=0"
    driver.get(link_)
    results = driver.find_elements_by_css_selector('div.g')
    link = results[0].find_element_by_tag_name("a")
    href = link.get_attribute("href")
    url=urlparse.parse_qs(urlparse.urlparse(href).query)["q"]
    f = requests.get(url[0],headers=headers,verify=False)
    s = f.content.decode('utf-8')
    soup = BeautifulSoup(s, 'lxml')
    table = soup.findAll('span',attrs={"class":"org"})
    count=0
    for x in table:
        if (fuzz.ratio(company_name.lower(),x.text.lower()))>80:
            count+=1
        else:
            break
    return count
