import scrapy
import re


class NoberoSpider(scrapy.Spider):
    name = 'nobero_spider'
    allowed_domains = ['nobero.com']
    start_urls = ['https://nobero.com/pages/men']

    def parse(self, response):
        categories = response.css(
            'a[href*="/collections/"]::attr(href)').getall()
        for category in categories:
            category_url = response.urljoin(category)
            yield scrapy.Request(category_url, callback=self.parse_category)

    def parse_category(self, response):
        product_urls = response.css(
            'a[href*="/products/"]::attr(href)').getall()
        for product_url in product_urls:
            full_product_url = response.urljoin(product_url)
            yield scrapy.Request(full_product_url, callback=self.parse_product)

        next_page = response.css('a.next.page-numbers::attr(href)').get()
        # if next_page:
        yield scrapy.Request(response.urljoin(next_page), callback=self.parse_category)

    def parse_product(self, response):
        product = {
            'category': response.css('a[href*="/collections/"] span::text').get(),
            'url': response.url,
            'title': response.css('h1.capitalize.text-lg.md\:text-\[1\.375rem\].font-\[familySemiBold\].leading-none::text').get().strip(),

            'price':   self.extract_price(response),

            'mrp': self.extract_mrp(response),

            'last_7_day_sale': self.extract_last_7_day_sale(response),
            'available_skus':self.extract_skus(response),
            **self.extract_attributes(response),
            'description':self.extract_description(response)
        }
        yield product

    def extract_price(self, response):
        price_text = response.css('#variant-price spanclass::text').get()
        if price_text:
            return int(price_text.strip().replace('₹', '').replace(',', ''))
        return None

    def extract_mrp(self, response):
        mrp_text = response.css(
            '#variant-compare-at-price').re_first(r'\d+[,.]?\d*')

        if mrp_text:
            return int(mrp_text.replace(',', ''))
        return None

    def extract_last_7_day_sale(self, response):
        sale_text = response.css('div.product_bought_count span::text').get()
        if sale_text:
            match = re.search(r'(\d+)', sale_text)
            if match:
                return int(match.group(1))
        return None
    

    def extract_attributes(self, response):
        attributes = {}
        for attribute in response.css('div#product-metafields-container div.product-metafields-values'):
            label = attribute.css('h4::text').get()
            value = attribute.css('p::text').get()
            if label and value:
                label_cleaned = label.strip().lower().replace(' ', '_')
                attributes[label_cleaned] = value.strip()
        return attributes
    
    def extract_description(self,response):
        description = response.css('#description_content *::text').getall()
        description_text = ' '.join(description).strip()
        if description_text:
            return description_text
        return None

    valid_sizes = {"S", "M", "L", "XL", "XXL", "XXXL"}

    def extract_skus(self, response):
        available_skus = []

        for option in response.css('select.option-select option'):
            title = option.css('::text').get()
            if not title:
                continue

            parts = [part.strip() for part in title.split(' / ')]
            if len(parts) != 2:
                continue

            color, size = parts

            if size not in self.valid_sizes:
                color, size = size, color

            value = option.css('::attr(value)').get()
            qty = option.css('::attr(data-variant-qty)').get()

            color_entry = next((entry for entry in available_skus if entry['color'] == color), None)
            if color_entry:
                if size not in color_entry['size']:
                    color_entry['size'].append(size)
            else:
                available_skus.append({
                    'color': color,
                    'size': [size]
                })
        return available_skus
