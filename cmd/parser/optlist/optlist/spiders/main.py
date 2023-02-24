import re
import scrapy
from ..items import OptlistItem


class MainSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["optlist.ru"]
    start_urls = ['https://optlist.ru/tenders/odezhda-obuv-optom',
                'https://optlist.ru/tenders/produkty-optom',
                'https://optlist.ru/tenders/stroitelniye-tovary-optom',
                'https://optlist.ru/tenders/stroitelniye-materialy-optom',
                'https://optlist.ru/tenders/detskie-tovary-igrushki-optom',
                'https://optlist.ru/tenders/tovary-dlya-doma-optom',
                'https://optlist.ru/tenders/podarki-optom',
                'https://optlist.ru/tenders/electronika-bytovaya-tehnika-optom',
                'https://optlist.ru/tenders/mebel-optom',
                'https://optlist.ru/tenders/kosmetika-optom',
                'https://optlist.ru/tenders/promishlennoe-oborudovanie-optom',
                'https://optlist.ru/tenders/avto-tovary-optom',
                'https://optlist.ru/tenders/lekarstva-optom',
                'https://optlist.ru/tenders/tovary-dlya-sporta-optom',
                'https://optlist.ru/tenders/tovary-ddlya-zhivotnih-optom',
                'https://optlist.ru/tenders/knigi-optom',
                'https://optlist.ru/tenders/tovary-dlya-tvorchestva-optom',
                'https://optlist.ru/tenders/uslugi',
                'https://optlist.ru/tenders/other']

    def parse(self, response):
        data = OptlistItem()
        table = response.css('div.mb-3')
        for item in table:
            data['category'] = response.css('div.row div.col-lg div.d-flex h1::text').get().replace('Закупка  ', '').replace('оптом', '').strip()
            if len(item.css('a')) != 0:
                data['url'] = response.urljoin(item.css('a::attr("href")').get())
                if len(item.css('div.clearfix')) != 0:
                    data['date'] = item.css('div.clearfix div.float-none::text').get()
                else:
                    data['date'] = None
                data['cardname'] = item.css('a::text').get().strip()
                if len(item.css('div.small a')) != 0:
                    data['region'] = item.css('div.small a::text').get().strip()
                else:
                    data['region'] = None
                data['description'] = ''.join(
                    re.findall(r'\S[а-я А-Я 0-9,.:-]*', ' '.join(
                        re.findall(r'\S\w.*', ''.join(
                            item.css('div.mb-2 ::text').getall())
                            )
                        )
                    )
                )
            else:
                continue
            yield data