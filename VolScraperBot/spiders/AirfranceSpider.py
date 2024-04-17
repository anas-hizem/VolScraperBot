import scrapy
from .AirfranceSelenium import Booking
from datetime import datetime, timedelta

class AirfranceSpider(scrapy.Spider):
    name = 'AirfranceSpider'
    allowed_domains = ["airfrance.tn"]

    def format_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            formatted_date = date_obj.strftime('%d %B %Y')
            formatted_date = formatted_date[0].upper() + formatted_date[1:]
            return formatted_date
        except ValueError:
            return None



    def __init__(self, demande_id=None, place_of_departure=None, place_of_arrival=None, type=None, check_in_date=None,check_out_date=None, *args, **kwargs):
        super(AirfranceSpider, self).__init__(*args, **kwargs)
        self.demande_id = demande_id
        self.place_of_departure = place_of_departure
        self.place_of_arrival = place_of_arrival
        self.type = type
        self.check_in_date = self.format_date(check_in_date)
        self.check_out_date = self.format_date(check_out_date) if type == "aller-retour" else None


    def start_requests(self):
        inst = Booking()
        inst.land_first_page()
        inst.accept_cookies()
        inst.select_type(self.type)
        inst.select_place_of_departure(self.place_of_departure)
        inst.select_place_of_arrival(self.place_of_arrival)
        inst.click_continue_buton()  
        inst.open_calandar(self.type) 
        i = inst.scrol_to_check_in_date(self.check_in_date)
        inst.select_check_in_date(self.check_in_date)
        inst.scrol_to_check_out_date(self.check_out_date , self.type , i)
        inst.select_check_out_date (self.check_out_date,self.type)
        inst.click_confirm()
        inst.click_submit()
        search_url = inst.page_loaded()
        yield  scrapy.Request(url=search_url, callback=self.parse, meta={'booking_instance': inst})


    def parse(self, response):
        inst = response.meta['booking_instance']
        inst.select_filter_outward()
        outward_departure_place = inst.get_deparature_place()
        outward_arrival_place = inst.get_arrival_place()
        return_departure_place = outward_arrival_place
        return_arrival_place = outward_departure_place
        outward_price = inst.get_outward_price()
        outward_time =inst.get_outward_time()
        outward_travel_duration = inst.get_outward__tarvel_duration()
        inst.click_details_button_outward()
        outward_date =inst.get_outward_tarvel_date()
        inst.click_exit_outward()
        url=inst.page_loaded()
        inst.go_to_return_travel(self.type)
        inst.select_filter_return(self.type)
        return_price = inst.get_return_travel_price(self.type)
        return_time=inst.get_return_travel_time(self.type)
        return_trip_duration = inst.get_return_trip_duration(self.type)
        inst.click_details_button_return(self.type)
        return_date = inst.get_return_tarvel_date(self.type)
        inst.click_exit_return(self.type)


        if self.type == "aller-retour":
            item =  {
                'demande_id': self.demande_id,
                'agence': "AIRFRANCE",
                'outward_departure_place':outward_departure_place ,
                'outward_arrival_place':outward_arrival_place,
                'outward_price':outward_price,
                'outward_time':outward_time,
                'duration_outward':outward_travel_duration + 'm',
                'outward_date':outward_date,
                'return_departure_place': return_departure_place,
                'return_arrival_place':return_arrival_place,
                'return_price':return_price,
                'return_time':return_time,
                'duration_return':return_trip_duration + 'm',
                'return_date':return_date,
                'url_of_vol':url
            }

        else:
            item =  {
                'demande_id': self.demande_id,
                'agence': "AIRFRANCE",
                'outward_departure_place':outward_departure_place ,
                'outward_arrival_place':outward_arrival_place,
                'outward_price':outward_price,
                'outward_time':outward_time,
                'duration_outward':outward_travel_duration + 'm',
                'outward_date':outward_date,
                'url_of_vol':url
            }
        yield item
        
        inst.close_browser()



    