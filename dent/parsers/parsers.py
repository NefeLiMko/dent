from bs4 import BeautifulSoup
from w_storm_data import HEADERS
from celery import Celery
import datetime
import time
import requests
import json
import re
import selenium
import aiohttp
import asyncio
"""
Для вкладок топ 50 и аномалии:
● https://el-dent.ru/ done
● https://w-stom.ru/
● https://shop.rocadamed.ru/ done
● https://aveldent.ru/ done

"""
# TODO: eldent async

requests.session()

num = '3f1a75e'

COOKIES = {
    '__hash_': f'e4b6feb1e0{num}7762868d293b52f'
}


class WStorm():
    def __init__(self) -> None:
        self.counter = 0
        self.is_up = False
        self.url = 'https://w-stom.ru'
        self.lst = []
        self.links = {}
        self.cookies = {
            '__hash_': '400e03d3fcbd5ab8877cc531d72007c6'
        }
        self.headers = HEADERS

    def get_catalog(self):
        r = requests.get(f'{self.url}/catalog', cookies=self.cookies, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        catalog_categories = soup.find_all('div', class_='section')
        for subcategory in catalog_categories:
            self.links[subcategory.find('a').get('href')] = []
            self.lst.append(subcategory.find('a').get('href'))
    
    async def get_items_from_category(self, page_url):
        print(self.counter, page_url)
        #self.cookies['__hash_'] = hex(int(self.cookies['__hash_'], 16) + int('b77c284ded247ce2', 16))
        links_from_page =[]
        r = requests.get(f'{self.url}{page_url}', cookies=self.cookies, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            next_page = soup.find('li', class_='bx-pag-next').find('a').get('href')
            links_from_page.extend(await self.get_items_from_category(next_page))
            
            #next_page = soup.find('li', class_='bx-pag-next').find('a').get('href')
            #links_from_page.extend(await self.get_items_from_category(next_page))
            #links_from_page.extend()
            
            
        except Exception as e:
            print(e.__str__)
        finally:
            
            col_images = soup.find('div', class_='productList').find_all('div', class_='productColImage')
            for link in col_images:
                product_url = link.find('a').get('href')
                links_from_page.append({str(product_url): await self.get_items_from_page(product_url)})

            print(len(links_from_page))
            return links_from_page
            
    
    async def get_items_from_page(self, url):
        
        r = requests.get(f'{self.url}{url}', cookies=self.cookies, headers=self.headers)
        print(self.counter, r.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.find('h1', class_='changeName').text
        articul = soup.find('span', class_='changeArticle').text
        out = {'name': name,
                'articul': articul}
        self.counter += 1
        return out
        
    def check_cookies(self):
        try:
            while not self.is_up:
                asyncio.run(self.main())
                self.cookies['__hash_'] = hex(int(self.cookies['__hash_'], 16) - int('fff000000000000000', 16))[2:] 
                print(self.cookies)
        except KeyboardInterrupt:
            return
        except:     
            print('hihi')
            self.check_cookies()
    
    def get_json(self):
        with open('wstorm.json', 'w+') as out_json:
            json.dump(self.links, out_json, indent=4)
    
    async def main(self):

        self.get_catalog()
        tasks = [self.get_items_from_category(page_url+'?SORT_TO=90') for page_url in self.lst]
        results = await asyncio.gather(*tasks)
        if results != []:
            self.is_up = True
        

class Aveldent():
    def __init__(self):
        self.url = 'https://aveldent.ru'
        self.lst = []
        self.links = {}
        self.json_name = f'aveldent-{datetime.date.today()}.json'

    
    def get_catalog(self):
        r = requests.get(f'{self.url}')
        soup = BeautifulSoup(r.text, 'html.parser')

        catalog_categories = soup.find('div', class_='category_list_left')
        all_a = catalog_categories.find_all('a')
        for a in all_a:
            if (a.get('href') == '/promo') or (a.get('href') == '/exclusive') or (a.get('href') == '/discount') or (a.get('href') == 'https://aveldent.ru/brands') or (a.get('href') == '/seminar'):
                print(f"{a.get('href')} - loh")
            else:
                self.links[a.get('href')] = {}    
                page_number = '1'
                req = requests.get(f"{self.url}{a.get('href')}?page={page_number}")
                new_page = BeautifulSoup(req.text, 'html.parser')
                self.links[a.get('href')].update(self.get_items_from_page(a))
        
    
    def get_items_from_page(self, a):
        page_items = {}
        req = requests.get(f"{self.url}{a.get('href')}?limit=10211212")
        soup = BeautifulSoup(req.text, 'html.parser')
        
        print(req.url)
        for item in soup.find_all('div', class_ = 'caption'):
            a =  item.find('a')
            price = item.find('div', class_= 'price').text.split('р.')[0]
            product_code = item.find('small').text.split('Артикул')[0].split(': ')[1].encode().decode()
            try:
                articul = item.find('small').text.split('Артикул')[1].split(': ')[1]
            except:
                articul = 'not found'
            page_items[a.text] = {'link': a.get('href'), 'product_code':product_code, 'articul': articul, 'price':price}
            to_db = {'name':a.text, 'articul' :articul, 'price':price, 'site':'AD'}
            requests.post('http://127.0.0.1:8000/api/products/', data=to_db)
        return page_items


    def get_json(self):
        with open(self.json_name, 'w+', encoding="utf-8") as out_json:
            json.dump(self.links, out_json, indent=4, ensure_ascii=False)

    def start(self):
        self.get_catalog()
        self.get_json()

class Rocada():
    def __init__(self) -> None:
        self.url = 'https://shop.rocadamed.ru'
        self.lst = []
        self.links = {}
        self.json_name = f'rocada-{datetime.date.today()}.json'

    def get_catalog(self):
        r = requests.get(f'{self.url}/catalog/')
        soup = BeautifulSoup(r.text, 'html.parser')

        catalog_categories = soup.find('div', class_='cat-block_new')
        all_a = catalog_categories.find_all('a')
        for a in all_a:
            self.links[a.get('href')] = []

    def get_items_from_page(self, link):
        data = []
        r = requests.get(f'{self.url}{link}')
        print(r.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        page_items = soup.find('div', attrs={'id':'filtered-block-result'}).find_all('div', class_='catalog-item')
        for item in page_items:
            price_str = re.findall(r'\b\d+\b', item.find('li', class_='what_main').text.replace('&nbsp;', ''))
            price = ''.join(price_str)
            art = re.sub(" +", " ", item.find('p', class_='art').text) 
            tag = item.find('div', class_='product-middle').find('a').get('title')[11:]
            if len(art)>1:
                art = art[7:]
            else:
                art = 'no artikul'
            to_append = {'tag':tag, 'artikul':art, 'price':price}
            to_db = {'name':tag, 'articul' :art, 'price':price, 'site':'RM'}
            requests.post('http://127.0.0.1:8000/api/products/', data=to_db)
            data.append(to_append)
        try:
            next_page_link = soup.find('li', class_='bx-pag-next').find('a').get('href')
            data.extend(self.get_items_from_page(next_page_link))
            return data
        except:
            return data
        
    def get_json(self):
        with open(self.json_name, 'w+', encoding="utf-8") as out_json:
            json.dump(self.links, out_json, indent=4, ensure_ascii=False)


    def get_items(self):
        for link in self.links:
            self.links[link] = self.get_items_from_page(link)
            print(self.links[link])
    
    def start(self):
        self.get_catalog()
        self.get_items()
        self.get_json()


class El_dent():
    def __init__(self) -> None:
        self.url = 'https://el-dent.ru'
        self.lst = []
        self.links = {}
        self.json_name = f'eldent-{datetime.date.today()}.json'

    def get_catalog(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        ul = soup.find_all('div', class_='-menu_catalog_d')[1].find('ul')

        links_to_find = list(set(self.find_internal_links(ul=ul))) 
        #print(len(ul.find_all('li')), len(links_to_find)) #1461 1226
        for el in links_to_find:
            self.links[el] = []
        #self.links[li.find('a').get('href')] = []

    def find_internal_links(self, ul):
        links = []
        for li in ul.find_all('li'):
            try:
                if li.find('a').get('href')=='/vendors/':
                    break
                else:
                    new_ul = li.find('ul')
                    links.extend(self.find_internal_links(new_ul))
            except:
                links.append(li.find('a').get('href'))

        return links


    async def get_product_data(self, link):
        r = requests.get(f'{self.url}{link}')
        print(r.url)
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            data = soup.find('div', class_='product-info')
            tag = data.find('h1').text
            articul_found = False
            all_imgs = data.find_all('img')
            for img in all_imgs:
                if img.get('src') == '/phpshop/templates/white_brick/images/icons/manuf.png':
                    articul = img.parent.text[20:]

                    articul_found = True
                    break
            if not articul_found:
                articul = soup.find('div', class_='product-info').find('div', class_='cart').find('span').parent.text.split('Артикул')[1]
            price = data.find('span', class_='price').text
            out = {'tag':tag, 'articul':articul, 'price':price}
            to_db = {'name':tag, 'articul' :articul, 'price':price, 'site':'ED'}
            requests.post('http://127.0.0.1:8000/api/products/', data=to_db)
            print(out)
            return out
        except:
            return {}  


    async def get_pages(self, link):
        #print(self.links)
        
        try:
            all_link = f'{link[:-5]}-ALL.html'
            r = requests.get(f'{self.url}{all_link}')
            print(r.url)            
            soup = BeautifulSoup(r.text, 'html.parser')
        
            for el in soup.find('div', class_='items').find('ul').find_all('li'):
                data = el.find('div', class_='about')
                link_to_item = data.find('a').get('href')
                    
                    
                self.links[link].append(await self.get_product_data(link_to_item))
                self.lst.append(link_to_item)
        except:
            pass

    def get_json(self):
        with open(self.json_name, 'w+', encoding="utf-8") as out_json:
            json.dump(self.links, out_json, indent=4, ensure_ascii=False)

    async def start(self):
        self.get_catalog()
        tasks = [self.get_pages(page_url) for page_url in self.links]
        results = await asyncio.gather(*tasks)

        self.get_json()


def start_wstorm():
    item = WStorm()
    asyncio.run(item.check_cookies())


#start_wstorm()