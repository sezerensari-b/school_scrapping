import json
import requests
from bs4 import BeautifulSoup
import warnings
import urllib3

warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

licence_url = "https://yokatlas.yok.gov.tr/onlisans-univ.php?u=" # url for licence
pre_licence_url = "https://yokatlas.yok.gov.tr/lisans-univ.php?u=" # url for pre licence 
licence_file_name = "licence_universities.json"
pre_licence_file_name="pre_licence_universities.json"
school_json = []

def start_scrap(url:str):
    for i in range(1, 5):
        for j in range(1000*i, 1000*i + 250):
            page_url = f"{url}{j}"
            make_scrap(page_url, j)


def make_scrap(url:str, j:int):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        uni_name = get_university_name(soup)
        
        if not uni_name:
            print(f"{j}. element is empty")
            return
        
        sections = get_sections(soup)
        school_json.append(make_university(uni_name, sections))


def make_university(uni_name:str, sections:list[dict]):
    university = {"name":uni_name, "faculties":{}}
    faculties:dict[str, list] = university.get("faculties")
    for section in sections:
        faculty_name = section.get("faculty")
        faculty_sections :list[str] = faculties.get(faculty_name,[])
        faculty_sections.append(section.get("section"))
        faculties[faculty_name] = faculty_sections
    
    return university


def get_university_name(soup:BeautifulSoup):
    h3_element = soup.select_one("body > div.row > div.container > div > h3")
    h3_element.find("small").extract()
    uni_name = h3_element.get_text(strip=True)
    if uni_name == "":
        return
    
    return uni_name


def get_sections(soup:BeautifulSoup):
    a_elements = soup.select("#bs-collapse > div > div > h4 > a")
    sections = []

    for element in a_elements:
        if not element:
            continue
        section_name = element.find('div').get_text(strip=True)
        faculty_name = element.find('font').get_text(strip=True).lstrip('(').rstrip(')')
        sections.append({
            "section": section_name,
            "faculty": faculty_name
        })

    return sections


##LICENCE
start_scrap(licence_url)
file = open(licence_file_name, 'w', encoding='utf-8')


## PRE LICENCE
# start_scrap(pre_licence_url)
# file = open(pre_licence_file_name, 'w', encoding='utf-8')



json.dump(school_json, file, ensure_ascii=False)