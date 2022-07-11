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
    title = html.find('span',title=True).string
    company = html.find('span',{"class":"companyName"}).text
    location = html.find('div',{'class':"companyLocation"}).text
    job_id = (html.find('td',{'class':"resultContent"}).a)['data-jk']

    return {
        "title":title,
        "company":company,
        "location":location,
        "apply_link":f"https://www.indeed.com/jobs?l=england&vjk={job_id}"
    }



def extract_jobs(url,last_page_num):
    """
    get a list of  job information dictionaries
    :param url: str
    :param last_page_num : int
    :return: list[dict[str,str]]
    """
    jobs = []
    for i in range(last_page_num):
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        divs = soup.find_all("div", {"class":"slider_container"})
        for div in divs:
            jobs.append(extract_job(div))
            

    return jobs



def get_jobs(search_term):
    """Extract jobs until the last page
    :param search_term: str
    :return: list[dict[str,str]]    
    """
    url = BASE_URL + f"/jobs?q={search_term}&l&vjk=467a04b2be1976cb"
    last_page_num = extract_last_page_num(url)
    return extract_jobs(url,last_page_num)
    
    

if __name__ == '__main__':    
    print(get_jobs("java"))