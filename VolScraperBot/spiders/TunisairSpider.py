import scrapy
from .TunisairSelenium import Booking
from datetime import datetime, timedelta

class TunisairSpider(scrapy.Spider):
    name = 'TunisairSpider'
    allowed_domains = ["tunisair.tn"]

    def format_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            formatted_date = date_obj.strftime('%d-%m-%Y')
            return formatted_date
        except ValueError:
            return None

    def validate_input(self):
        if not all([self.place_of_departure, self.place_of_arrival, self.type, self.check_in_date]):
            raise ValueError("Entrée invalide : Veuillez fournir les informations nécessaires.")

    def __init__(self, place_of_departure=None, place_of_arrival=None, type=None, check_in_date=None, check_out_date=None, *args, **kwargs):
        super(TunisairSpider, self).__init__(*args, **kwargs)
        self.place_of_departure = place_of_departure
        self.place_of_arrival = place_of_arrival
        self.type = type
        self.check_in_date = self.format_date(check_in_date)
        self.check_out_date = self.format_date(check_out_date) if type == "aller-retour" else None
        self.validate_input()


    def start_requests(self):
        inst = Booking()
        inst.land_first_page()
        inst.accept_cookies()
        inst.select_place_of_departure(self.place_of_departure)
        inst.select_place_of_arrival(self.place_of_arrival)
        inst.select_type(self.type)
        inst.open_calandar(self.type)  
        inst.select_check_in_date(self.check_in_date,self.type)
        inst.select_check_out_date (self.check_out_date,self.type)
        inst.set_check_in_date_one_way_trip(self.check_in_date,self.type)
        inst.click_confirm(self.type)
        inst.click_submit()
        search_url = inst.page_loaded()
        yield scrapy.Request(url=search_url, callback=self.parse, meta={'booking_instance': inst})
    def parse(self, response):
        inst = response.meta['booking_instance']
        outward_departure_place = inst.get_deparature_place()
        outward_arrival_place = inst.get_arrival_place()
        return_departure_place = inst.get_arrival_place()
        return_arrival_place = inst.get_deparature_place()
        outward_date =inst.get_outward_tarvel_date()
        return_date = inst.get_return_tarvel_date(self.type)
        outward_price = inst.get_outward_price()
        return_price = inst.get_return_travel_price(self.type)
        inst.go_to_next_page()
        outward_time =inst.get_outward_time()
        outward_travel_duration = inst.get_outward__tarvel_duration()
        return_time=inst.get_return_travel_time(self.type)
        return_trip_duration = inst.get_return_trip_duration(self.type)
        url=inst.page_loaded()
        inst.close_browser()

        if self.type == "aller-retour":
            yield {
                'agence': "TUNISAIR",
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
        else :
            yield {
                'agence': "TUNISAIR",
                'outward_date':outward_date,
                'departure_place':outward_departure_place ,
                'arrival_place':outward_arrival_place,
                'outward_price':outward_price,
                'outward_time':outward_time,
                'duration_outward':outward_travel_duration,
                'url_of_vol':url 
            }

    