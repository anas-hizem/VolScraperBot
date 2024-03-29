import scrapy
from .AirfranceSelenium import Booking
from datetime import datetime, timedelta

class AirfranceSpider(scrapy.Spider):
    name = 'AirfranceSpider'
    allowed_domains = ["airfrance.tn"]

    def format_date(self,date_str):
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            formatted_date = date_obj.strftime('%d %B %Y')
            formatted_date = formatted_date[0].upper() + formatted_date[1:]
            return formatted_date
        except ValueError:
            return None
    def __init__(self, place_of_departure=None, place_of_arrival=None, type=None, check_in_date=None, check_out_date=None, *args, **kwargs):
        super(AirfranceSpider, self).__init__(*args, **kwargs)
        self.place_of_departure = place_of_departure
        self.place_of_arrival = place_of_arrival
        self.type = type
        self.check_in_date =self.format_date(check_in_date)
        if self.type!="aller-retour":
            self.check_out_date = None
        else:
            self.check_out_date = self.format_date(check_out_date)


    def start_requests(self):
        inst = Booking()
        inst.land_first_page()
        inst.accept_cookies()
        inst.click_continue_buton()  
        inst.select_type(self.type)
        inst.select_place_of_departure(self.place_of_departure)
        inst.select_place_of_arrival(self.place_of_arrival)
        inst.open_calandar(self.type) 
        inst.scrol_to_check_in_date(self.check_in_date)
        inst.select_check_in_date(self.check_in_date)
        inst.select_check_out_date (self.check_out_date,self.type)
        inst.click_confirm()
        inst.click_submit()
        search_url = inst.page_loaded()
        yield scrapy.Request(url=search_url, callback=self.parse, meta={'booking_instance': inst})
    def parse(self, response):
        inst = response.meta['booking_instance']
        inst.select_filter()
        outward_departure_place = inst.get_deparature_place()
        outward_arrival_place = inst.get_arrival_place()
        return_departure_place = outward_arrival_place
        return_arrival_place = outward_departure_place
        outward_price = inst.get_outward_price()
        outward_time =inst.get_outward_time()
        outward_travel_duration = inst.get_outward__tarvel_duration()
        inst.click_details_button()
        outward_date =inst.get_outward_tarvel_date()
        inst.click_exit()
        url=inst.page_loaded()
        inst.go_to_return_travel(self.type)
        inst.select_filter()
        return_price = inst.get_return_travel_price(self.type)
        return_time=inst.get_return_travel_time(self.type)
        return_trip_duration = inst.get_return_trip_duration(self.type)
        inst.click_details_button()
        return_date = inst.get_return_tarvel_date(self.type)
        inst.click_exit()
        url=inst.page_loaded()
        inst.close_browser()

        
        if self.type == "aller-retour":
            yield {
                'agence': "AIRFRANCE",
                'outward_date':outward_date,
                'outward_departure_place':outward_departure_place ,
                'outward_arrival_place':outward_arrival_place,
                'outward_price':outward_price,
                'outward_time':outward_time,
                'duration_outward':outward_travel_duration,
                'return_date':return_date,
                'return_departure_place': return_departure_place,
                'return_arrival_place':return_arrival_place,
                'return_price':return_price,
                'return_time':return_time,
                'duration_return':return_trip_duration,
                'url_of_vol':url
            }
        else:
            yield {
                'agence': "AIRFRANCE",
                'outward_date':outward_date,
                'outward_departure_place':outward_departure_place ,
                'outward_arrival_place':outward_arrival_place,
                'outward_price':outward_price,
                'outward_time':outward_time,
                'duration':outward_travel_duration,
                'url_of_vol':url
            }

    