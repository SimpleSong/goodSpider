import scrapy
from goods_spider.items import ImageItemsItem, MongodbItem
import goods_spider

class A1688Spider(scrapy.Spider):

    urls = goods_spider.settings.A1688_SRART_URLS

    name = '1688Spider'

    def start_requests(self):
        startUrl = 'https://shop1475254196895.1688.com/page/offerlist.htm?suggestiontype=winport&spm=a2615.2177701.20151125147.d147&keywords=s%BC%D22019%B4%BA%CF%C4%D0%C2%C6%B7%C5%AE%D7%B0+%BA%DA%C9%AB%C0%D9%CB%BF%D3%A1%BB%A8%C6%B4%BD%D3%CD%B8%CA%D3%B3%C4%C9%C0%B0%D9%B4%EE%CA%E7%C5%AE%D5%E6%CB%BF%C9%CF%D2%C2'
        yield scrapy.Request(url=startUrl, callback=self.pageView)

    def pageView(self, response):

        urls = []

        table = response.css('.offer-list-row')[0]

        items = table.css('li div.image a')

        for item in items:
             urls.append( item.css('::attr(href)').extract_first() )

        yield scrapy.Request(url=urls[0], callback=self.parse)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

        next_page = response.css('.next').extract_first()  # css选择器提取下一页链接

        if next_page is not None:  # 判断是否存在下一页
            next_url = response.css('.next').css('::attr(href)').extract_first()
            yield scrapy.Request(url=next_url, callback=self.pageView)

    def parse(self, response):

        imageItem = ImageItemsItem()

        imageUrls = []

        imgItems = response.css('#dt-tab .box-img img')
        path = response.css('h1.d-title::text').extract_first()

        for item in imgItems:
            imageUrls.append( item.css('::attr(src)').extract_first().replace('.60x60','') )

        imageItem['imageUrls'] = imageUrls
        imageItem['path'] = path
        imageItem['type'] = '主图'

        yield imageItem

        mongoItem = MongodbItem()
        mongoItem['url'] = response.url
        mongoItem['source'] = '1688'
        mongoItem['name'] = response.css('.d-title')[0].css('::text').extract_first()
        prices = []
        ps = response.css('tr.price span.value')
        for price in ps:
            prices.append(price.css('::text').extract_first())
        mongoItem['prices'] = prices
        mongoItem['mainPrice'] = prices[0]
        skus = []
        colors = []
        dColors = response.css('.d-content .list-leading img')
        for color in dColors:
            colors.append(
                {'name': color.css('::attr(alt)').extract_first(), 'url': color.css('::attr(src)').extract_first()})
        skus.append({'colors': colors})
        skusLine = response.css('.obj-content .table-sku tr')
        for skuLine in skusLine:
            name = skuLine.css('.name span::text').extract_first()
            price = skuLine.css('.price span .value::text').extract_first()
            stock = skuLine.css('.count span .value::text').extract_first()
            sku = {'name': name, 'price': price, 'stock': stock}
            skus.append(sku)
        mongoItem['skuList'] = skus
        details = {}
        des = response.css('#mod-detail-attributes table tbody td')
        length = int(len(des) / 2)
        for i in range(length):
            details[des[i * 2].css('::text').extract_first()] = des[i * 2 + 1].css('::text').extract_first()
        if None in details:
            details.pop(None)
        mongoItem['details'] = details
        yield mongoItem






