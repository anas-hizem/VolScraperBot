import scrapy
from .TunisairExpressSelenium import Booking
from datetime import datetime, timedelta
class TunisairExpressSpider(scrapy.Spider):
    name = "volspider1"
    allowed_domains = ["tunisairexpress.net"]
    def extraire_heure(self,texte):
        # Séparer l'heure de la ville
        heure_ville = texte.split()[0]
        # Extraire l'heure et les minutes
        heure, minute = heure_ville.split(':')
        return heure + ':' + minute
    def change_format (self, place) :
            if place=='tunis' :
                return 'TUN'                                 
            elif place== 'paris' :
                return'ORY'
            elif place  == 'naples':                   
                return"NAP"
            elif place == "ROME" :
                return "ROM"
            elif  place== "maltes" :
                return "MAL"
            elif  place == "palerme" :
                return "PLO"
            elif  place == "consatantine" :
                return "CZL"
            elif  place == "TRIPOLI" :
                return "MJI"
            else:return "TUN"
    def next_date(self,input_date):
        # Convertir la chaîne d'entrée en objet datetime
        date_obj = datetime.strptime(input_date, '%d/%m/%Y')
        
        # Ajouter un jour à la date
        next_day = date_obj + timedelta(days=0)
        
        # Formater la date suivante comme une chaîne au format "jour/mois/année"
        next_date_str = next_day.strftime('%d/%m/%Y')
        
        return next_date_str

    def __init__(self, place_of_departure=None, place_of_arrival=None, type=None, check_in_date=None, check_out_date=None, *args, **kwargs):
        super(TunisairExpressSpider, self).__init__(*args, **kwargs)
        self.place_of_departure = self.change_format(place_of_departure)
        self.place_of_arrival = self.change_format(place_of_arrival)
        self.type = type
        self.check_in_date = self.next_date(check_in_date)
        if self.type!="aller-retour":
            self.check_out_date = None
        else:
            self.check_out_date = self.next_date(check_out_date)
    
    def start_requests(self):
        inst = Booking()
        inst.land_first_page()
        inst.select_place_of_departure(self.place_of_departure)
        inst.select_place_of_arrival(self.place_of_departure, self.place_of_arrival)
        inst.select_type(self.type)
        inst.select_dates(self.check_in_date, self.check_out_date, self.type)
        inst.click_search()
        search_url = inst.page_loaded()
        yield scrapy.Request(url=search_url, callback=self.parse, meta={'booking_instance': inst})
    

    def parse(self, response):
        inst = response.meta['booking_instance']
        outward_departure_place = inst.get_deparature_place(self.place_of_departure)
        outward_arrival_place = inst.get_arrival_place(self.place_of_arrival)
        return_arrival_place = outward_arrival_place
        return_departure_place = outward_departure_place
        outward_price = inst.get_outward_price()
        return_price = inst.get_return_price(self.type)
        outward_date = inst.get_outward_date()
        return_date = inst.get_return_date(self.type)
        url_of_vol =  inst.get_url()
        inst.click_next_page()
        outward_time = inst.get_time_of_deparature_travel(self.type)
        outward_travel_duration=inst.get_outward_travel_duration(self.type)
        return_travel_duration=inst.get_return_travel_duration(self.type)
        return_time=inst.get_time_of_return_travel(self.type)
        inst.close_browser()

        if self.type == "aller-retour":
            yield {
                'agence' : "TUNISAIR EXPRESS",
                'outward_date': outward_date,
                'outward_deparature_place': outward_departure_place,
                'outward_arrival_place': outward_arrival_place,
                'outward_price': outward_price,
                'outward_time': self.extraire_heure(outward_time) ,
                'duration_outward':outward_travel_duration,
                'return_date': return_date,
                'return_deparature_place': return_arrival_place,
                'return_arrival_place': return_departure_place,
                'return_price': return_price,
                'return_time': return_time ,
                'duration_return':return_travel_duration,
                'url_of_vol': url_of_vol
            }
        else :
            yield {
                'agence' : "TUNISAIR EXPRESS",
                'outward_date': outward_date,
                'outward_deparature_place': outward_departure_place,
                'outward_arrival_place': outward_arrival_place,
                'outward_price': outward_price,
                'outward_time': self.extraire_heure(outward_time) ,
                'duration_outward':outward_travel_duration,
                'url_of_vol': url_of_vol
            }

    