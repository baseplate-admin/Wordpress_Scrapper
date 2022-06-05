from scrapy import Selector
from scrapy.spiders import SitemapSpider

PAGE_NUMBER = 1


class SiteSpider(SitemapSpider):

    name = "SiteSpider"

    sitemap_urls = ["https://shortstatusquotes.com/post-sitemap.xml"]

    def parse(self, response):
        global PAGE_NUMBER
        content = response.xpath(
            "/html/body/div/div[2]/div/main/article/div/p"
        ).getall()
        data_dict = {}

        content_list = []

        for data in content:
            data = Selector(text=data)

            if data.xpath("/html/body/p/strong"):  # Tttle
                data_dict[f"post_{PAGE_NUMBER}_title"] = data.xpath(
                    "/html/body/p/strong//text()"
                ).get()
                PAGE_NUMBER += 1
            elif data.xpath("/html/body/p/img"):  # Image
                data_dict[f"post_{PAGE_NUMBER}_image"] = data.xpath(
                    "/html/body/p/img//@src"
                ).extract()
            else:
                content_list.append(data.xpath("/html/body/p//text()").get())

            data_dict[f"post_{PAGE_NUMBER-1}_content"] = "".join(content_list)

        del content_list

        PAGE_NUMBER = 1

        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "content": data_dict,
        }


# --- it runs without project and saves in `output.csv` ---

from scrapy.crawler import CrawlerProcess

c = CrawlerProcess(
    {
        "USER_AGENT": "Mozilla/5.0",
        # save in file as CSV, JSON or XML
        "FEED_FORMAT": "csv",  # csv, json, xml
        "FEED_URI": "output.csv",  #
    }
)
c.crawl(SiteSpider)
c.start()
