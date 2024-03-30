from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class Booking (webdriver.Chrome): 
    def __init__(self, driver_path="C:/Users/HIZEM/Desktop/PCD/VolScraperBot/chromedriver.exe") :
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless") 
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        super(Booking,self).__init__() 
        self.implicitly_wait(15)
        self.maximize_window()
    
    def land_first_page (self) :
        self.get("https://www.tunisairexpress.net/")
        self.implicitly_wait(60)

        
    def select_place_of_departure(self,place_of_departure) :
        self.implicitly_wait(60)
        country_of_departure_selected = WebDriverWait(self,10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,f'option[value="{place_of_departure}"]'))
        )                                                                   
        country_of_departure_selected.click()
        self.implicitly_wait(30)


    def select_place_of_arrival(self ,place_of_departure, place_of_arrival): 
        self.implicitly_wait(60)
        if place_of_departure == 'TUN':
            arrival_places = {'ORY': 15, 'ROM': 12, 'NAP': 10, 'MLA': 9, 'PMO': 11, 'CZL': 14, 'MJI': 13}
            i= arrival_places.get(place_of_arrival, 15) 
        else :
            i = 2
        country_of_arrival = WebDriverWait(self,10).until(
            EC.visibility_of_element_located((By.XPATH,f'//*[@id="arrivee"]/option[{i}]'))
        )                                                                   
        country_of_arrival.click()

    def select_type(self, type):
        if (type =='aller-simple'):
            aller_simple = WebDriverWait(self,10).until(
                EC.element_to_be_clickable((By.ID,'rdchq_cnt2'))
            )                                                                   
            aller_simple.click()

        
    def select_dates (self ,check_in_date , check_out_date, type):
        if  type == "aller-retour" :
            date = WebDriverWait(self,10).until(
                    EC.visibility_of_element_located((By.XPATH,'//*[@id="daterange"]')))  
            date.click()
            date.send_keys(check_in_date)
            date_selected = WebDriverWait(self,10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,'td[class="available active start-date end-date"]')))  
            date_selected.click()


            date = WebDriverWait(self,10).until(
                    EC.visibility_of_element_located((By.XPATH,'//*[@id="daterange2"]')))  
            date.click()
            date.send_keys(check_out_date)
            div = WebDriverWait(self, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.daterangepicker[style*="display: block;"]'))
            )
            element = div.find_element(By.CSS_SELECTOR, 'td.available.active.start-date.end-date')
            element.click()


        else :
            date = WebDriverWait(self,10).until(
                    EC.visibility_of_element_located((By.XPATH,'//*[@id="daterange"]')))  
            date.click()
            date.send_keys(check_in_date)
            date_selected = WebDriverWait(self,10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,'td[class="available active start-date end-date"]')))  
            date_selected.click()

    def click_search(self):
        button = WebDriverWait(self, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="submitbtn"][type="submit"]'))
        )
        button.click()

    def page_loaded(self):
        return self.current_url
    

    
    def get_outward_date(self) :
        date_of_departure = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="s4"]/div/span[2]'))
        ).text
        return date_of_departure

    def get_return_date(self,typeoftrip) :
        if typeoftrip=="aller-retour":
            date_of_arrival = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="s5"]/div[2]/span[2]'))
            ).text
            return date_of_arrival

    def get_outward_price(self) :
            outward_price = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.calendarPerBound-inner-elements-outbound .calendarPerBound-fare .selected .calendarPerBound-price .price-amount'))
            ).text
            return outward_price
    def get_return_price(self,typeoftrip) :
        if typeoftrip=="aller-retour":
                return_price = WebDriverWait(self, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.calendarPerBound-inner-elements-inbound .calendarPerBound-fare .selected .calendarPerBound-price .price-amount'))
                ).text
                return return_price



    def get_deparature_place(self) :
        outward_place = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#calendarPerBound-cell-display-outbound .calendarPerBound-outbound-city.fromcity'))
        ).text
        return outward_place

    def get_arrival_place(self) :
        return_place = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#calendarPerBound-cell-display-outbound .calendarPerBound-outbound-city.tocity'))
        ).text
        return return_place   



    def get_url(self):
        return self.current_url
    

    def click_next_page (self):    
        button = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="plnext-widget-btn btn btn-primary tripsummary-btn-primary tripSummary-btn-continue tripsummary-btn-validate validate-btn"]'))
        )
        button.click()
        time.sleep(0.5)

    
    def get_time_of_deparature_travel(self,typeoftrip):
        if typeoftrip=="aller-simple":
            time_of_departure = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#s23 div.tripsummary-itinerary-details div.tripsummary-details .tripsummary-time'))).text
            return time_of_departure

        else:
            time_of_departure = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#s27 div.tripsummary-itinerary-details div.tripsummary-details .tripsummary-time'))).text
            return time_of_departure

    def get_time_of_return_travel(self,typeoftrip):
        if typeoftrip=="aller-retour":
            time_of_return = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#s28 div.tripsummary-itinerary-details div.tripsummary-details .tripsummary-time'))
            ).text
            return (time_of_return)
        
    def get_outward_travel_duration(self,typeoftrip):
        if typeoftrip=="aller-simple":
            duration_outward_trip_elem = WebDriverWait(self, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#s23 div.tripsummary-itinerary-details div.tripsummary-details .tripsummary-total-duration-value'))
            )
            duration_outward_trip =  duration_outward_trip_elem.text.split(',')[0]
            return duration_outward_trip

        else:
            duration_outward_trip_elem = WebDriverWait(self, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#s27 div.tripsummary-itinerary-details div.tripsummary-details .tripsummary-total-duration-value'))
            )
            duration_outward_trip =  duration_outward_trip_elem.text.split(',')[0]
            return duration_outward_trip

    def get_return_travel_duration (self,typeoftrip):
        if typeoftrip=="aller-retour":
            duration_return_trip_elem = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#s28 div.tripsummary-itinerary-details div.tripsummary-details .tripsummary-total-duration-value'))
            ).text
            duration_return_trip = duration_return_trip_elem.split(',')[0]
            return(duration_return_trip)
    def close_browser(self):
        self.quit()
    

    
        

