from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler  
import pytz
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
from tqdm import tqdm
import csv
from datetime import datetime, timedelta
import pytz

def extract_article_date(soup):
    date_element = soup.find("time", class_="article-content__time")
    
    if date_element:
        article_date = date_element.get_text(strip=True)
        return article_date
    else:
        return None

def Udn_news():
    user_agents = [
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"
    ]
    UA ={"User-Agent":random.choice(user_agents)}

    def get_random_proxy():
        proxy_list = [
            '1.2.3.4:6666',
            '2.2.3.4:7777',
            '103.61.39.99',
            '45.224.99.90',
            '61.79.139.30'
        ]
        proxy = random.choice(proxy_list)
        return proxy
    
    # All tags/keywords
    # keywords_list=["貪污","貪汙","洗錢","賄賂","逃漏稅","偽造","交保","詐欺","販毒","走私","違反證交法","詐貸","組織犯罪","地下匯税","賭博","起訴","移送","到案"]
    keywords_list=["貪污","貪汙","洗錢"]

    # Create empty lists
    news_list = []
    id_list = []
    tag_list=[]

    # Get today's datetime
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    def get_news_list(page_num):
        base_url = "https://udn.com/api/more"
        all_data = {}  
        processed_keywords = []

        for keywords in tqdm(keywords_list) : 
            processed_keywords.append(keywords)

            for page in range(page_num):
                channelId = 2
                id = 'search'
                type = 'searchword'
                query = f"page={page+1}&id={id}:{keywords}&channelId={channelId}&type={type}"
                news_list_url = base_url + '?' + query
                proxies = {'http': 'http://'+get_random_proxy()}
                r = requests.get(news_list_url, headers = UA,proxies=proxies)
                
                for t in r.json()["lists"]:
                    news_list.append(t["titleLink"])
                    sp = t["titleLink"].split("/")
                    id_list.append(sp[-2]+sp[-1])
                    tag_list.append(keywords)
                time.sleep(random.uniform(1,3))
            all_data[keywords] = {"news_list": news_list, "id_list": id_list}
        return all_data 

    # ANALYZE NEWS CONTENT
    all_data = get_news_list(page_num=1)

    print(f"共抓到 {len(news_list)} 筆新聞")

    title_list = []  
    content_list = [] 
    date_list = []
    selected_news_list = []
    selected_ids_list = []
    selected_tags_list = []

    for i in tqdm(range(len(news_list))):  
        
        resp =requests.get( news_list[i], headers = UA )
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text,"lxml") 

        # Extract publication date from the article
        article_date = extract_article_date(soup)
        article_date_obj = datetime.strptime(article_date, "%Y-%m-%d %H:%M") if article_date else None
        
        # article_date_obj2 = datetime.strptime(article_date, "%Y/%m/%d %H:%M") if article_date else None
        # Compare the article_date with yesterday's date and today's date 
        if (article_date_obj) and (yesterday.date() <= article_date_obj.date() < today.date()):
            
            print(f"!!Yes!!")
            #Extract title
            title = soup.select('h1',class_ ='article-content__title')
            if title != []:
                title = title[0].text
            else:
                title = ''

            #Extract content
            content = soup.select("section.article-content__editor>p")
            try:
                content = soup.select("section.article-content__editor>p")
            except:
                content = soup.select("div>main>p")

            #Combine content paragraphs into a single string
            cont =""
            for p in content:
                cont=cont+p.text 
            
            #Extract date
            Date = str(soup.find("time",class_="article-content__time"))
            try:
                Date = soup.find("time",class_="article-content__time").text
            except:
                Date = soup.find("span",class_="article-content__subinfo--time.datetime")  

            Date = Date.split( )[0] if Date != None else ""
            time.sleep(random.uniform(1, 3))

            #Extract ID
            div_element = soup.find('div', class_='line-it-button')             # Parse the HTML using BeautifulSoup
            data_url_value = div_element.get('data-url')

            #Extract news URL
            url = data_url_value.split('?')[0]
            urlID = url.split("/")[-1]

            emptyValue = "NONE"

            #Extract tag
            for keyword in keywords_list:
                selected_tags_list.append(keyword)

            if (urlID != None):
                selected_ids_list.append(urlID)
            else:
                selected_ids_list.append(emptyValue)

            if (url != None):
                selected_news_list.append(url)
            else:
                selected_news_list.append(emptyValue)
                
            if (title != None):
                title_list.append(title)
            else:
                title_list.append(emptyValue)

            if (cont!= None):
                content_list.append(cont)     
            else:
                content_list.append(emptyValue)   

            if (Date != None):
                date_list.append(Date)
            else:
                date_list.append(emptyValue)  

        else:
            print(f"!!Skip!!")  
    

    #儲存資料#
    tb={
        "ID":selected_ids_list,   
        "title":title_list,
        "href":selected_news_list,          
        "content":content_list,
        "Date":date_list,
        "tag": selected_tags_list            
    }  

    df = pd.DataFrame(tb,columns=["ID","title","href","content","Date","tag"])
    df.dropna(axis=0,how='any',inplace=True)
    df.drop_duplicates(subset='ID',inplace=True)
    return df

def save_to_csv(dataframe, filename):
    dataframe.to_csv(filename, index=False)
    
def run():
    output = Udn_news()
    print(output)
    save_to_csv(output, "udn_news.csv")

if __name__ == "__main__":
    # sched = BlockingScheduler(timezone=pytz.timezone("Asia/Taipei"))
    # sched.add_job(run,'cron',day_of_week ='0-6',hour = 13 ,minute = 36)     
    # sched.start()
    run()
