from bs4 import BeautifulSoup 
import requests


BASE_URL = f"https://www.indeed.com"



def extract_last_page_num(url):
    """get the last page number
    :param url: str
    :return :int
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    div = soup.find("div",{"class":"pagination"})
    lis = div.find_all("li")
    label_list = [li.findChild()['aria-label'] for li in lis]
    return int(label_list[-2])

def extract_job(html):
    """get a dictionary of job's information
    :param html: Tag
    :return: dict[str,str]  
    """
    title = html.find('h2').text
    company = html.find('span',{"class":"companyName"}).text
    location = html.find('div',{'class':"companyLocation"}).text
    apply_link = (html.find('td',{'class':"resultContent"}).a)['data-jk']

    return {
        "title":title,
        "company":company,
        "location":location,
        "apply_link":apply_link
    
    }




def extract_jobs(url,last_page_num):
    """
    get a list of  job information dictionaries
    :param url: str
    :param last_page_num : int
    :return: list[dict[str,str]]
    """

    for i in range(last_page_num):
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        divs = soup.find_all("div", {"class":"slider_container"})
        jobs = [extract_job(div) for div in divs]
            

    return jobs



def get_jobs(search_term):
    """Extract jobs until the last page
    :param search_term: str
    :return: list[dict[str,str]]    
    """
    url = BASE_URL + f"/jobs?q={search_term}&l&vjk=467a04b2be1976cb"
    last_page_num = extract_last_page_num(url)
    print(extract_jobs(url,last_page_num))
    
    # 3. Extract jobs
    # 4. Return Jobs



get_jobs("java")