import scrapy
class Mobile(scrapy.Item):
    title = scrapy.Field()
    brand = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field() 

class AmazonScraper(scrapy.Spider):
    name = "amazon_scraper"

    # How many pages you want to scrape
    no_of_pages = 1

    # Headers to fix 503 service unavailable error
    # Spoof headers to force servers to think that request coming from browser ;)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2840.71 Safari/539.36'}

    def start_requests(self):
        # starting urls for scraping
        urls = ["https://www.amazon.com/b?node=18637575011&pf_rd_p=40ed81c0-6271-4813-bb5a-c65127ad0c47&pf_rd_r=1RYRAQR65AY5CD6GX5CJ"]

        for url in urls: yield scrapy.Request(url = url, callback = self.parse, headers = self.headers)

    def parse(self, response):

        self.no_of_pages -= 1

        # print(response.text)

        mobiles = response.xpath("//a[@class='.s-access-title']").xpath("@href").getall()
        
#        ddd print(len(mobiles))

        for mobile in mobiles:
            final_url = response.urljoin(mobile)
            yield scrapy.Request(url=final_url, callback = self.parse_mobile, headers = self.headers)
            # break
            # print(final_url)

        # print(response.body)
        # title = response.xpath("//span[@class='a-size-medium a-color-base a-text-normal']//text()").getall()
        # title = response.css('span').getall()
        # print(title)
        
        if(self.no_of_pages > 0):
            next_page_url = response.xpath("//ul[@id='pagnNextString']/a").xpath("@href").get()
            final_url = response.urljoin(next_page_url)
            yield scrapy.Request(url = final_url, callback = self.parse, headers = self.headers)

    def parse_mobile(self, response):
        title = response.xpath("//span[@id='result_1']//text()").get() or response.xpath("//h1[@id='title']//text()").get()
        brand = response.xpath("//a[@id='result_1']//text()").get() or "not specified"
        rating = response.xpath("//div[@id='averageCustomerReviews_feature_div']").xpath("//span[@class='a-icon-alt']//text()").get()

        price = response.xpath("//span[@id='priceblock_ourprice']//text()") or response.xpath("//span[@id='priceblock_dealprice']//text()")
        print(price)
        if len(price) > 1: price = price[1].get()
        elif len(price) == 1: price = price[0].get()
        else : price = price.get()
        
        reviews = response.xpath("//div[@class='a-expander-content reviewText review-text-content a-expander-partial-collapse-content']/span//text()").getall()
        description_raw = response.xpath("//div[@id='featurebullets_feature_div']//span[@class='a-list-item']//text()").getall()


        description = []
        for description_temp in description_raw:
            description.append(description_temp.strip())

        print(title, brand, rating, price)
        # print(final_review)
        # print(reviews)
        # print(description)

        yield Mobile(title = title.strip(), brand = brand.strip(), rating = rating.strip(), price = price.strip(), reviews = reviews, description = description)