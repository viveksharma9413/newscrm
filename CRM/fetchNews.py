from urllib2 import urlopen
from bs4 import BeautifulSoup

'''
Funtion to fetch news by scrapping in.reueter.com website
'''
def fetch(url):
    try:
        data = urlopen(url)
        soup = BeautifulSoup(data)

        divs = soup.find('section',attrs={'class':'module-content'})        #find section tag within website html code
        divm = divs.find('div',attrs={'class':'news-headline-list'})        #find div tag with class=news-headline lit in website html code
        lis = divm.findAll('article',attrs={'class':'story'})               #find all article tag eith class=story within website html code

        news = ""
        for li in lis:
            link = 'in.reuters.com'+li.find('h3',attrs={'class':'story-title'}).find('a').get('href')           #extract link
            headlines = li.find('h3',attrs={'class':'story-title'}).find('a').contents[0]                       #extract headlines
            content = li.find('p').contents[0]                                                                  #extract content
            news += '<a href = \"'+link+'\"><h3>'+str(headlines)+'</h3></a>\n'+content+'\n\n'
        return news

    except AttributeError:
        print("please enter url from in.reuters.com of the format 'http://in.reuters.com/news/archive/......'")
        return "No News fetched"
