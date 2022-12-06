import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/List_of_computer_scientists',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_2(self,response):
        xp = '//*[@class=\"infobox biography vcard\"]'
        lis = response.xpath(xp)
        for l in lis :
            print(l.get())

    def parse(self, response):
        #
        #/html/body/div[3]/div[3]/div[5]/div[1]/ul[1]
        #
        for i in range(1,25):
            xp = '//*[@id=\"mw-content-text\"]/div[1]/ul['+str(i)+']/li/a[contains(@href, "/wiki/")][1]'
            #exw parei to lis
            lis = response.xpath(xp)
            #pairnw to link apo ka8e li
            input()
            for l in lis :
                link = l.css('a::attr(href)').get()
                if link is not None:
                    #print(link)
                    #print('*' * 30)
                    link = response.urljoin(link)
                    yield scrapy.Request(link, callback=self.parse_2)
                    #print('*' * 30)
