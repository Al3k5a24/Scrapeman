import scrapy
from ..items import FragranceItem
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
import os

class MainSpiderScraper(scrapy.Spider):
    #name for cli call, syntax scrapy crawl *name*
    name = "FragranceSpider"

    #url from main page of website that will be scraped
    allowed_domains = ["kupujemprodajem.com", "www.kupujemprodajem.com"]

    #specific urls that you want to scrape from
    base_url = "https://www.kupujemprodajem.com/nega-i-licna-higijena/parfemi-muski/pretraga?keywords=xerjoff%20naxos&categoryId=20&groupId=1314&ignoreUserId=no&page="

    #define path where you want to save your xlsx file
    excel_path = r"C:\Users\lekid\OneDrive\Desktop\proba.xlsx"

    #number of pages to be scraped
    max_pages = 50

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #create excel workbook
        self.workbook = Workbook()
        self.worksheet = self.workbook.active
        self.worksheet.title = "Fragrances"

        headers = ['Header', 'Price']
        self.worksheet.append(headers)

        #fell free to customize by taste
        for cell in self.worksheet[1]:
            cell.font = Font(bold=True, size=12)
            cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            cell.font = Font(bold=True, color="FFFFFF")

        self.row_num = 2

    def start_requests(self):
        yield scrapy.Request(
            url=f"{self.base_url}1",
            callback=self.parse,
            meta={'page': 1}
        )

    def parse(self, response):
        current_page = response.meta['page']
        fragrances = response.css(".AdItem_adOuterHolder__hb5N_")

        #data which will be scraped
        for i, fragrance in enumerate(fragrances):
            item = FragranceItem()

            #specific url
            relative_url = fragrance.css("a::attr(href)").get()
            full_url = response.urljoin(relative_url)
            link=item["link"] = full_url

            # use this syntax to add more data if you need
            header=item["header"] = fragrance.css("div.AdItem_name__iOZvA::text").get()
            price=item["price"] = fragrance.css("div.AdItem_price__VZ_at div::text").get()

            if link:
                link = response.urljoin(link)

            if header:
                self.worksheet.append([header, price])

            #make header as hyper-link
            if link:
                link_cell = self.worksheet.cell(row=self.row_num, column=1)
                link_cell.hyperlink = link
                link_cell.font = Font(color="0563C1", underline="single")

                self.row_num += 1

            if item["header"]:
                yield item

        # next page
        if current_page < self.max_pages:
            yield scrapy.Request(
                url=f"{self.base_url}{current_page + 1}",
                callback=self.parse,
                meta={'page': current_page + 1}
            )

    def closed(self, reason):
        directory = os.path.dirname(self.excel_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        self.workbook.save(self.excel_path)
        self.logger.info(f"✓ Excel saved: {self.excel_path}")
        self.logger.info(f"✓ Total items: {self.row_num - 2}")