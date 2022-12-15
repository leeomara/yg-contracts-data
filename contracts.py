import scrapy

class ContractsSpider(scrapy.Spider):
    name = 'contracts'
    start_urls = [
        'https://service.yukon.ca/apps/contract-registry/f?p=108:500::::::',
    ]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'P500_FISCAL_YEAR_FROM': '2007-08', 
                'P500_FISCAL_YEAR_TO': '2007-08'
            },
            callback=self.after_submit
        )

    def after_submit(self, response):
        for contract in response.css('table#report_table_P510_RESULTS tbody tr'):
            fields = contract.css('td::text')
            yield {
                'Contract Description': fields[0].get(),
                'Vendor Name': fields[1].get(),
                'Amount': fields[2].get(),
                'Start Date': contract.css('td span::text').get(),
                'Contract No.': fields[3].get(),
                'C.O. No.': fields[4].get(),
                'Line No.': fields[5].get(),
                'SOA No.': fields[6].get(),
                'Department': fields[7].get(),
                'Contract Type': fields[8].get(),
                'Tender Class': fields[9].get(),
                'Community': fields[10].get(),
                'Type': fields[11].get(),
                'Fiscal Year': contract.css('td a::text').get(),
            }

        next_page = response.css('.t-Report-pagination--bottom a.t-Report-paginationLink--next::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.after_submit)