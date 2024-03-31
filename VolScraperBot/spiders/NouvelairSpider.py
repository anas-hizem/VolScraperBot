import scrapy
import datetime
import locale
from .NouvelairSelenium import Booking
import re
class NouvelairSpider(scrapy.Spider):
    name = "NouvelairSpider"
    allowed_domains = ["nouvelair.com"]

    def __init__(self, place_of_departure=None, place_of_arrival=None, type=None, check_in_date=None, check_out_date=None, *args, **kwargs):
        super(NouvelairSpider, self).__init__(*args, **kwargs)
        self.place_of_departure = place_of_departure
        self.place_of_arrival = place_of_arrival
        self.type = type
        self.check_in_date = self.convert_date_format(check_in_date)
        self.check_out_date = self.convert_date_format(check_out_date)

    def convert_date_format(self, date_str):
        if date_str:
            # Séparer la date en composants
            day, month, year = date_str.split('/')
            # Convertir le mois en français
            months_mapping = {
                '01': 'jan',
                '02': 'fév',
                '03': 'mar',
                '04': 'avr',
                '05': 'mai',
                '06': 'jui',
                '07': 'jui',
                '08': 'aoû',
                '09': 'sep',
                '10': 'oct',
                '11': 'nov',
                '12': 'déc'
            }
            month_fr = months_mapping.get(month, month)
            new_date_format = f"{day} {month_fr} {year}"
            return new_date_format
        else:
            return None


    def start_requests(self):
        inst = Booking()
        inst.land_first_page()
        inst.accept_cookies()
        inst.select_place_of_departure(self.place_of_departure)  # Utilisez self.place_of_departure
        inst.select_place_of_arrival(self.place_of_arrival)  # Utilisez self.place_of_arrival
        inst.select_dates(self.check_in_date, self.check_out_date, self.type)  # Utilisez self.check_in_date, self.check_out_date et self.type
        inst.click_search()
        search_url = inst.page_loaded()
        yield scrapy.Request(url=search_url)

    def parse(self, response):
        if self.type == "aller-retour":
            outward_departure_place_text = response.css('div.journeySection_OUTBOUND_0 .info-block .port::text').get()
            outward_departure_place = re.search(r'(.+?)\s\(', outward_departure_place_text).group(1).upper()

            outward_arrival_place_text = response.css('div.journeySection_OUTBOUND_0 .info-block.right-info-block.text-right .port::text').get()
            outward_arrival_place = re.search(r'(.+?)\s\(', outward_arrival_place_text).group(1).upper()

            outward_price_text = response.css('div.journeySection_OUTBOUND_0 .middle.active-box.dayNavigation .price-text-single-line::text').get()
            outward_price = re.search(r'\d+', outward_price_text).group()

            # Conversion de la date
            outward_date_text = response.css('div.journeySection_OUTBOUND_0 .info-block .date-block .date ::text').get()
            outward_date = self.convert_date(outward_date_text)

            outward_time = response.css('div.journeySection_OUTBOUND_0 .time::text').get()

            duration_outward_text = response.css('div.journeySection_OUTBOUND_0 div.middle-block span.flight-duration::text').get()
            duration_outward = re.sub(r'\s', '', duration_outward_text)  # Supprimer les espaces

            return_departure_place_text = response.css('div.journeySection_INBOUND_1 .port::text').get()
            return_departure_place = re.search(r'(.+?)\s\(', return_departure_place_text).group(1).upper()

            return_arrival_place_text = response.css('div.journeySection_INBOUND_1 .info-block.right-info-block.text-right .port::text').get()
            return_arrival_place = re.search(r'(.+?)\s\(', return_arrival_place_text).group(1).upper()

            return_date_text = response.css('div.journeySection_INBOUND_1 .date::text').get()
            return_date = self.convert_date(return_date_text)

            return_price_text = response.css('div.journeySection_INBOUND_1 .middle.active-box.dayNavigation .price-text-single-line::text').get()
            return_price = re.search(r'\d+', return_price_text).group()

            duration_return_text = response.css('div.journeySection_INBOUND_1 .availability-flight-table .scheduled-flights .js-journey .js-scheduled-flight .selection-item .row .desktop-route-block .info-row .middle-block .flight-duration::text').get()
            duration_return = re.sub(r'\s', '', duration_return_text)  # Supprimer les espaces

            yield {
                'agence': "NOUVELAIR",
                'outward_departure_place': outward_departure_place,
                'outward_arrival_place': outward_arrival_place,
                'outward_date': outward_date,
                'outward_price': outward_price,
                'outward_time': outward_time,
                'duration_outward': duration_outward,
                'return_departure_place': return_departure_place,
                'return_arrival_place': return_arrival_place,
                'return_date': return_date,
                'return_price': return_price,
                'return_time': response.css('div.journeySection_INBOUND_1 .time::text').get(),
                'duration_return': duration_return,
                'url_of_vol': response.url
            }
        else:
            outward_departure_place_text = response.css('div.journeySection_OUTBOUND_0 .info-block .port::text').get()
            outward_departure_place = re.search(r'(.+?)\s\(', outward_departure_place_text).group(1).upper()

            outward_arrival_place_text = response.css('div.journeySection_OUTBOUND_0 .info-block.right-info-block.text-right .port::text').get()
            outward_arrival_place = re.search(r'(.+?)\s\(', outward_arrival_place_text).group(1).upper()

            outward_price_text = response.css('div.journeySection_OUTBOUND_0 .middle.active-box.dayNavigation .price-text-single-line::text').get()
            outward_price = re.search(r'\d+', outward_price_text).group()

            # Conversion de la date
            outward_date_text = response.css('div.journeySection_OUTBOUND_0 .info-block .date-block .date ::text').get()
            outward_date = self.convert_date(outward_date_text)

            outward_time = response.css('div.journeySection_OUTBOUND_0 .time::text').get()

            duration_outward_text = response.css('div.journeySection_OUTBOUND_0 div.middle-block span.flight-duration::text').get()
            duration_outward = re.sub(r'\s', '', duration_outward_text)  # Supprimer les espaces

            yield {
                'agence': "NOUVELAIR",
                'outward_departure_place': outward_departure_place,
                'outward_arrival_place': outward_arrival_place,
                'outward_date': outward_date,
                'outward_price': outward_price,
                'outward_time': outward_time,
                'duration_outward': duration_outward,
                'url_of_vol': response.url
            }

    def convert_date(self, date_str):
        # Convertir la date en format datetime
        datetime_obj = datetime.datetime.strptime(date_str, '%d %b. %Y')
        # Définir la localisation française pour le nom du jour et du mois
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        # Formatter la date avec le nom du jour
        formatted_date = datetime_obj.strftime('%a %d %b %Y')
        return formatted_date