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
                'Start Date': fields[3].get(),
                'Contract No.': fields[4].get(),
                'C.O. No.': fields[5].get(),
                'Line No.': fields[6].get(),
                'SOA No.': fields[7].get(),
                'Department': fields[8].get(),
                'Contract Type': fields[9].get(),
                'Tender Class': fields[10].get(),
                'Community': fields[11].get(),
                'Type': fields[12].get(),
                'Fiscal Year': fields[13].get(),
            }

        next_page = response.css('.t-Report-pagination--bottom a.t-Report-paginationLink--next::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.after_submit)