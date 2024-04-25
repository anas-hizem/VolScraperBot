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



    def __init__(self, demande=None, place_of_departure=None, place_of_arrival=None, type=None, check_in_date=None, check_out_date=None, *args, **kwargs):
        super(TunisairSpider, self).__init__(*args, **kwargs)
        self.demande = demande
        self.place_of_departure = place_of_departure
        self.place_of_arrival = place_of_arrival
        self.type = type
        self.check_in_date = self.format_date(check_in_date)
        self.check_out_date = self.format_date(check_out_date) if type == "aller-retour" else None



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
        yield  scrapy.Request(url=search_url, callback=self.parse, meta={'booking_instance': inst})

    def parse(self, response):
        def convert_date_format(date_str):
            if date_str is None:
                return None

            days_mapping = {
                'Lun': 'Lundi',
                'Mar': 'Mardi',
                'Mer': 'Mercredi',
                'Jeu': 'Jeudi',
                'Ven': 'Vendredi',
                'Sam': 'Samedi',
                'Dim': 'Dimanche'
            }
            months_mapping = {
                'Jan': 'Janvier',
                'Fév': 'Février',
                'Mar': 'Mars',
                'Avr': 'Avril',
                'Mai': 'Mai',
                'Jui': 'Juin',
                'Jui': 'Juillet',
                'Aoû': 'Août',
                'Sep': 'Septembre',
                'Oct': 'Octobre',
                'Nov': 'Novembre',
                'Déc': 'Décembre'
            }

            parts = date_str.split()  
            day_of_week = parts[0]     
            day = parts[1]             
            month = months_mapping.get(parts[2], parts[2])
            year = parts[3]           
            return f"{days_mapping[day_of_week]} {day} {month} {year}"

    
        inst = response.meta['booking_instance']
        outward_departure_place = inst.get_deparature_place()
        outward_arrival_place = inst.get_arrival_place()
        outward_departure_place_abr = inst.get_departure_place_abr()
        outward_arrival_place_abr = inst.get_arrival_place_abr()
        return_departure_place = inst.get_arrival_place()
        return_arrival_place = inst.get_deparature_place()
        return_departure_place_abr = inst.get_arrival_place_abr()
        return_arrival_place_abr = inst.get_departure_place_abr()
        outward_date =convert_date_format(inst.get_outward_tarvel_date())
        return_date = convert_date_format(inst.get_return_tarvel_date(self.type))
        outward_price = inst.get_outward_price()
        return_price = inst.get_return_travel_price(self.type)
        inst.go_to_next_page()
        outward_departure_time =inst.get_outward_departure_time()
        outward_arrival_time =inst.get_outward_arrival_time()
        outward_travel_duration = inst.get_outward__tarvel_duration()
        return_departure_time=inst.get_return_departure_time(self.type)
        return_arrival_time=inst.get_return_arrival_time(self.type)
        return_trip_duration = inst.get_return_trip_duration(self.type)
        url=inst.page_loaded()

        item =  {
            'demande': self.demande,
            'agence': "TUNISAIR",
            'outward_date':outward_date,
            'outward_departure_place':outward_departure_place ,
            'outward_arrival_place':outward_arrival_place,
            'outward_departure_place_abr':outward_departure_place_abr ,
            'outward_arrival_place_abr':outward_arrival_place_abr,
            'outward_price':outward_price,
            'outward_departure_time':outward_departure_time,
            'outward_arrival_time':outward_arrival_time,
            'duration_outward':outward_travel_duration,
            'return_date':return_date,      
            'return_departure_place': return_departure_place,
            'return_arrival_place':return_arrival_place,
            'return_departure_place_abr': return_departure_place_abr,
            'return_arrival_place_abr':return_arrival_place_abr,
            'return_price':return_price,
            'return_departure_time':return_departure_time,
            'return_arrival_time':return_arrival_time,
            'duration_return':return_trip_duration,
            'url_of_vol':url 
        }

        yield item
        inst.close_browser()

    