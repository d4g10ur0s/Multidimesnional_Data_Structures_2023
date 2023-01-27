import scrapy
import os
import json
import re
import time
import pandas as pd

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    info = []

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/List_of_computer_scientists',
        ]
        wurls = [
            'https://thesaurus.yourdictionary.com/education',
        ]

        '''for url in wurls:
            yield scrapy.Request(url=url, callback=self.parse_words)'''
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    async def parse_words(self,response):
        a = response.xpath("//*[contains(@class,'synonym-link')]/text()")
        words = []
        for b in a:
            if len(str(b.get()))>2:
                words.append(str(b.get()))
        try :
            path = os.getcwd()
            if os.path.exists(path + "\\words"):
                pass
            else:
                os.mkdir(path + "\\words")

            f = open(path + "\\words\\words.txt","w+")
            for word in words :
                f.write(word)
                f.write("\n")
            f.close()
        except ValueError:
            pass

    def write_file(self,scientist):
        scientist = pd.DataFrame(data=[scientist])
        path = os.getcwd()
        try :
            if os.path.exists(path  + "\\..\\data\\scientists"):
                pass
            else:
                os.mkdir(path + "\\..\\data\\scientists")

            f = open(path + "\\..\\data\\scientists\\"+scientist.loc[0]["name"]+".json","w+")
            scientist.to_json(f)
            #input('meta')
            f.close()
        except ValueError:
            pass

    '''def write_file(self,scientist):
        scientist = pd.DataFrame(data=[scientist])
        path = os.getcwd()
        try :
            if os.path.exists(path + "\\scientists"):
                pass
            else:
                os.mkdir(path + "\\scientists")
            f = open(path + "\\scientists\\"+scientist.loc[0]["name"]+".json","w+")
            scientist.to_json(f)
            #input('meta')
            f.close()
        except ValueError:
            pass'''

    async def parse_2(self,response):
        path = os.getcwd()
        f= open(path + "\\scrappy\\spiders\\words\\words.txt","r")
        words = f.readlines()
        f.close()
        t = []
        ps = PorterStemmer()

        for i in words :
            t.append(ps.stem(i[:len(i)-1]))
        words = t

        #metavlhth scientist
        scientist = {
            'name' : '',
            'education_text' : "",
            'awards' : 0,
        }
        #pairnw to viografiko ka8e scientist
        xp = '//*[@class=\"infobox biography vcard\"]'
        #prpei na parw ke text
        infobox = response.xpath(xp)
        #8elw onoma
        node = infobox.xpath('//*[@class=\"fn\"]')
        name = node.css('div::text').get()
        if name == None :
            if infobox.get() == None:
                name = response.xpath("/html/body/div[3]/h1/span/text()").get()

        scientist['name'] = name
        #input('ftasame sto name')
        #pame gia awards
        i=1
        tr = infobox.xpath("//tr["+str(i)+"]")
        while tr.get() != None :
            if tr[0].css('th::text').get()!= None and "Awards" in tr[0].css('th::text').get():
                ul = tr[0].css('td div ul')
                if len(ul) == 0:#kapoia den einai se ul
                    scientist['awards'] = len(tr[0].css('td').get().split("</a>"))-1
                else:
                    scientist['awards'] = len(ul.get().split("</li>"))-1

            i+=1
            tr = infobox.xpath("//tr["+str(i)+"]")
        #end while

        #gia education text
        ps = response.css("p")
        d = ps.getall()
        for p in d:
            #print(str(re.split("(</a>) |(<a)", p)))
            p=p.replace('</a>', '')
            p=p.replace('<a href=', ' ')
            p=p.replace('<a ', '')
            p=p.replace('</sup>', '')
            p=p.replace('title=', ' ')
            p=p.replace('<sup id=', ' ')
            p=p.replace('</p>', '')
            p=p.replace('<p>', '')
            p=p.replace('<b>', '')
            p=p.replace('</b>', '')
            p=p.replace('</span>', '')
            p=p.replace('<span>', '')
            p=p.replace('class=', ' ')
            p=p.replace('</i>', '')
            p=p.replace('<i>', '')
            p=p.replace('<', '')
            p=p.replace('>', '')
            for i in range(0,50):
                p=p.replace("["+str(i)+"]" , '')

            p = re.sub('\"[a-z,A-Z,/,\\,_,-,=,:]*\"',' ',p)
            p = re.sub('#*[a-z,A-Z,_,:,0-9]+\-[0-9]*','',p)
            p=p.strip()
            p=re.sub('(\")',' ',p)
            edu_text = []
            for w in words :
                mregex = "[ä,a-z,A-Z,0-9, ,(,),\']+("+w+")[A-Z,a-z,0-9,(,), ,\']+"
                b = re.match(mregex, p)
                if b==None :
                    mregex = "[ä,a-z,A-Z,0-9, ,(,),\']+("+w.capitalize()+")[A-Z,a-z,0-9,(,), ,\']+"
                    b = re.match(mregex, p)
                    if b==None:
                        pass
                    else:
                        edu_text.append(b.group())
                else:
                    edu_text.append(b.group())

            for sentence in edu_text :
                scientist["education_text"]+=sentence

        #prepei na apo8hkeusw plhroforia
        if scientist['awards']==None:
            scientist['awards']=0
        yield self.write_file(scientist)

    async def parse(self, response):
        #
        #/html/body/div[3]/div[3]/div[5]/div[1]/ul[1]
        #
        for i in range(1,25):
            xp = '//*[@id=\"mw-content-text\"]/div[1]/ul['+str(i)+']/li/a[contains(@href, "/wiki/")][1]'
            #exw parei to lis
            lis = response.xpath(xp)
            #pairnw to link apo ka8e li
            for l in lis :
                link = l.css('a::attr(href)').get()
                if link is not None:
                    link = response.urljoin(link)
                    #paw se epomenh selida
                    yield scrapy.Request(link, callback=self.parse_2)