import pandas as pd
from bs4 import BeautifulSoup
from selenium  import webdriver
import json
import re

# firefox
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True  # opens firefox silently
browser = webdriver.Firefox(executable_path='.\Drivers\geckodriver.exe',options=fireFoxOptions) # uses Gecko driver

# chrome
# chromeOpts = webdriver.ChromeOptions()
# chromeOpts.headless = True
# browser = webdriver.Chrome(executable_path='.\Drivers\chromedriver.exe',options=chromeOpts)

# phantomJS
# browser = webdriver.PhantomJS(executable_path='/home/lee/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

# contra 15 m
#url = 'https://c.ikitesurf.com/classifieds?search=contra%2015m&type=all&location=all&price=all&c_states=all&brand=Cabrinha&year=all&size=all&views=all&sortby=date&page=1&orderby=dsc&expires=0&wanted=0&terms=all'
# all kites 15 m
url = 'https://c.ikitesurf.com/classifieds?search=&type=4&location=all&price=all&c_states=all&brand=all&year=all&size=15&views=all&sortby=date&page=1&orderby=dsc&expires=0&wanted=0&terms=all&favourite=0&deleted=0&reported=0'
      
# get content
browser.get(url)
content = browser.page_source
soup = BeautifulSoup(content, features='html.parser')
# get page count
pages = soup.find_all(class_="page-num")
pages = [int(x.string) for x in pages]
max_pages = max(pages)

classifieds = []
res = {}
cnt = 0

# for each pach
for i in range(1,max_pages+1):
    res[str(i)] = {}
    # go to webpage
    url = 'https://c.ikitesurf.com/classifieds?search=&type=4&location=all&price=all&c_states=all&brand=all&year=all&size=15&views=all&sortby=date&page=' + str(i) + '&orderby=dsc&expires=0&wanted=0&terms=all&favourite=0&deleted=0&reported=0'
    browser.get(url)
    content = browser.page_source
    soup = BeautifulSoup(content, features='html.parser')
    # grab elements
    prices = soup.find_all(class_ = 'cl-price-bigger')
    res[str(i)]['prices'] = [x.string for index, x in enumerate(prices) if index % 2 == 0]
    condition = soup.find_all(class_ = 'product_condition')
    res[str(i)]['conditions'] = [x.string for index, x in enumerate(condition) if index % 2 == 0]
    titles = soup.find_all(class_ = 'ld class_brief')
    res[str(i)]['titles'] = [x.string for index, x in enumerate(titles) if index % 2 == 0]
    # sold = soup.find_all(class_ = 'sold-details')
    # res[str(i)]['sold'] = [x.string for index, x in enumerate(sold) if index % 2 == 0]
    # for foo in soup.find_all(class_ ='classified-text'):
    #     locations = foo.find(class_ = 'ld')
    #     res[str(i)]['locs'] = [x.string for index, x in enumerate(locations) if index % 2 == 0]

    cnt += min(len(res[str(i)]['prices']),len(res[str(i)]['conditions']),len(res[str(i)]['titles']))
    
# re order data structure
final = {}
k = 0
for j in range(1,max_pages+1):
    pgcnt = min(len(res[str(j)]['prices']),len(res[str(j)]['conditions']),len(res[str(j)]['titles']))
    m = 1
    while k < cnt and m <= pgcnt:
        final[k] = {}
        final[k]['price'] = int(re.sub(r'[a-zA-Z]','',res[str(j)]['prices'][k%pgcnt]).replace('$','').strip())
        final[k]['condition'] = res[str(j)]['conditions'][k%pgcnt].strip()
        final[k]['title'] = res[str(j)]['titles'][k%pgcnt].strip()
        #final[k]['location'] = res[str(j)]['locs'][k%pgcnt].strip()
        k += 1
        m += 1

# sort by price for each item
final = sorted(final.items(), key= lambda x: x[1]['price'])    

# quit browser object, dump data, and close file
browser.quit()
json = json.dumps(final)
f = open('./ads.json', 'w')
f.write(json)
f.close()
print('completed')