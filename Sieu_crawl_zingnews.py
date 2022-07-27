# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import requests
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'X-Requested-With': 'XMLHttpRequest',
} 
#Get list link subject
r = requests.get('https://zingnews.vn/', headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

linkSJ =''
list_linkSJ = []
list_link = []
SP1 = soup.findAll('li')
for subject in range(0,len(SP1)):
  linkSJ = SP1[subject].findAll('a',recursive=False)
  linkSJ = str(linkSJ).strip('[]')
  if linkSJ != '':
    sj = linkSJ.split('>')
    sj1 = sj[1].split('<')
    sj1 = sj1[0].strip('\n')
    sj1 = sj1.lstrip().rstrip()
    list_linkSJ.append(sj1)
    sj2 = linkSJ.split('"')
    if sj2[1][1] != '/':
      l1 = f'https://zingnews.vn{sj2[1]}'
    else:
      l1 = f'https:{sj2[1]}'
    list_link.append(l1)

Subjects = pd.DataFrame({'Link_subject':list_link,
                      'Subjects':list_linkSJ})
Subjects.drop(Subjects.index[102:113], axis = 0, inplace = True)
Subjects

#function clean text
def cleanme(html):
       soup = BeautifulSoup(html) # create a new bs4 object from the html data loaded
       for script in soup(["script"]): 
           script.extract()
       text = soup.get_text()
       return text

#function get newspaper from a link
def get_newspaper(url):
  news = {}
  content = []
  r1 = requests.get(url, headers=headers)
  soup1 = BeautifulSoup(r1.content, 'html.parser')
  news['Id'] = (url.split('post')[1].split('.')[0])
  news['Date'] = cleanme(str(soup1.find(attrs={'class':'the-article-publish'})))
  news['Title'] = cleanme(str(soup1.find(attrs={'class':'the-article-title'})))
  news['Sumary'] = cleanme(str(soup1.find(attrs={'class':'the-article-summary'})))
  news['picture'] = re.findall(r'(https?://\S+)', str(soup1.findAll('td', class_ = 'pic')))
  body = soup1.find(attrs = {'class':'the-article-body'})
  if body:
    lf = body.findChildren("p", recursive=False)
    for a in range(0, len(lf)):
      content0 = body.findChildren("p", recursive=False)[a].text
      content.append(content0)
    content = ' '.join(content)
  news['Content'] = content  
  return(news)

#function to get newspaper from a sybject
def newspaper():
  print('enter url of subject')
  url_of_subject = input()
  r = requests.get(url_of_subject, headers=headers)
  soup = BeautifulSoup(r.content, 'html.parser')
  SP = soup.findAll('p', class_ = 'article-title') #tìm các sản phầm
  link = []
  links = []
  l = ''
  for i in range(0,len(SP)):
    children = SP[i].findChildren("a" , recursive=False)
    children = str(children).split('"')
    l = f'https://zingnews.vn{children[1]}'
    link.append(l)

  dic_news = {}
  for p in range(0, len(link)):
    key = get_newspaper(link[p]).get('Id')
    dic_news[key] = get_newspaper(link[p])
  return(dic_news)

if __name__ == "__main__":
  Subjects.to_excel('subject_crawl.xlsx', index = False)
  dics = newspaper()
  df_dic = pd.DataFrame(dics.items(), columns = ['Id','dics_newspaper'])
  df = []
  for n in range(0,len(dics)):
    df.append(list(df_dic.dics_newspaper[n].values()))
  df_dics = pd.DataFrame(df, columns = df_dic.dics_newspaper[0].keys())
  df_dics.to_excel('newspaper_file.xlsx', index = False)
