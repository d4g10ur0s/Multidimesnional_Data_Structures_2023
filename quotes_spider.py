import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/List_of_computer_scientists',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        #q = response.css('div.mw-parser-output')
        #
        for i in range(0,22):
            xp = "//*[@id=\"mw-content-text\"]/div[1]/ul["+str(i)+"]"
            for quote in response.xpath(xp):
                print(quote.get())
                print('.' * 10)

        '''
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        '''
