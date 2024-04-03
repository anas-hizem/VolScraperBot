import scrapy
from .TunisairExpressSelenium import Booking
from datetime import datetime, timedelta

class TunisairExpressSpider(scrapy.Spider):
    name = "volspider1"
    allowed_domains = ["tunisairexpress.net"]

    def extraire_heure(self, texte):
        try:
            heure_ville = texte.split()[0]
            heure, minute = heure_ville.split(':')
            return heure + ':' + minute
        except Exception as e:
            self.logger.error(f"Erreur lors de l'extraction de l'heure : {e}")
            return None

    def change_format(self, place):
        places_mapping = {
            'tunis': 'TUN',
            'paris': 'ORY',
            'naples': 'NAP',
            'rome': 'ROM',
            'maltes': 'MAL',
            'palerme': 'PLO',
            'consatantine': 'CZL',
            'tripoli': 'MJI'
        }
        return places_mapping.get(place.lower(), None)

    def next_date(self, input_date):
        try:
            date_obj = datetime.strptime(input_date, '%d/%m/%Y')
            next_day = date_obj + timedelta(days=0) 
            return next_day.strftime('%d/%m/%Y')
        except Exception as e:
            self.logger.error(f"Erreur lors du calcul de la prochaine date : {e}")
            return None


    def __init__(self, place_of_departure=None, place_of_arrival=None, type=None, check_in_date=None,check_out_date=None, *args, **kwargs):
        super(TunisairExpressSpider, self).__init__(*args, **kwargs)
        self.place_of_departure = self.change_format(place_of_departure)
        self.place_of_arrival = self.change_format(place_of_arrival)
        self.type = type
        self.check_in_date = self.next_date(check_in_date)
        self.check_out_date = self.next_date(check_out_date) if type == "aller-retour" else None
    
    def start_requests(self):
        inst = Booking()
        inst.land_first_page()
        inst.select_place_of_departure(self.place_of_departure)
        inst.select_place_of_arrival(self.place_of_departure, self.place_of_arrival)
        inst.select_type(self.type)
        inst.select_dates(self.check_in_date, self.check_out_date, self.type)
        inst.click_search()
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
        return_arrival_place = outward_arrival_place
        return_departure_place = outward_departure_place
        outward_price = inst.get_outward_price()
        return_price = inst.get_return_price(self.type)
        outward_date = convert_date_format(inst.get_outward_date())
        return_date = convert_date_format(inst.get_return_date(self.type))
        url_of_vol =  inst.get_url()
        inst.click_next_page()
        outward_time = inst.get_time_of_deparature_travel(self.type)
        outward_travel_duration=inst.get_outward_travel_duration(self.type)
        return_travel_duration=inst.get_return_travel_duration(self.type)
        return_time=inst.get_time_of_return_travel(self.type)

        

        if self.type == "aller-retour":
            item =  {
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
            item =  {
                'agence' : "TUNISAIR EXPRESS",
                'outward_date': outward_date,
                'outward_deparature_place': outward_departure_place,
                'outward_arrival_place': outward_arrival_place,
                'outward_price': outward_price,
                'outward_time': self.extraire_heure(outward_time) ,
                'duration_outward':outward_travel_duration,
                'url_of_vol': url_of_vol
            }
        yield item
        
        inst.close_browser()


    