from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import os
import undetected_chromedriver as uc
import selenium

class Booking(uc.Chrome): 
    def __init__(self, driver_path="C:/Users/HIZEM/Desktop/PCD/VolScraperBot/chromedriver.exe"):
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--headless") 
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        super().__init__(service=Service(executable_path=driver_path)) 
        self.maximize_window()

    def land_first_page (self) :
        url = "https://www.tunisair.com/fr"
        self.get(url)
        self.implicitly_wait(110)

    def accept_cookies(self) :
        accept_button = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="agree-button eu-cookie-compliance-secondary-button"]'))
        )
        accept_button.click()

    def select_place_of_departure(self , place_of_departure):
        open_field = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div/main/section/section/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/form/div[1]/div[2]/div[1]/fieldset/div/div[1]/fieldset[1]/span/span[1]/span'))
        )
        open_field.click()
        country_of_departure = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,'input[class="select2-search__field"]'))
        )
        country_of_departure.clear()
        country_of_departure.send_keys(place_of_departure)
        country_of_departure.send_keys(Keys.ENTER) 

    
    def select_place_of_arrival(self , place_of_arrival):
        open_field = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div/main/section/section/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/form/div[1]/div[2]/div[1]/fieldset/div/div[1]/fieldset[2]/span/span[1]/span'))
        )
        open_field.click()
        country_of_arrival = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[class="select2-search__field"]'))
        )
        country_of_arrival.clear()
        country_of_arrival.send_keys(place_of_arrival)
        country_of_arrival.send_keys(Keys.ENTER) 

    def select_type(self , type_trip):
        if (type_trip == "aller-simple"):
            type_trip = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/main/section/section/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/form/div[1]/div[1]/fieldset[1]/div/div/div[2]/input'))
            )
            type_trip.click()
            time.sleep(1)
            type_trip.click()
            self.implicitly_wait(30)

        else :
            pass

    def open_calandar(self , type_trip):
        self.implicitly_wait(60)
        if(type_trip == "aller-retour"):
            calendar = self.find_element(By.CSS_SELECTOR,'input[class="calendar form-control"][id="edit-date"]')
            calendar.click()
        self.implicitly_wait(60)


    def select_check_in_date(self ,check_in_date , type_trip):
        self.implicitly_wait(30)
        if(type_trip == "aller-retour"):           
            date_check_in = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="input-mini form-control active"][name="daterangepicker_start"]'))
            )
            date_check_in.clear()
            date_check_in.send_keys(check_in_date)
            date_check_in.send_keys(Keys.DOWN)
            date_check_in.send_keys(Keys.ENTER)


    def select_check_out_date(self , check_out_date  ,type_trip):
        self.implicitly_wait(30)
        if(type_trip == "aller-retour"):
            date_check_out = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="input-mini form-control"][name="daterangepicker_end"]'))
            )
            date_check_out.clear()
            date_check_out.send_keys(check_out_date)
            date_check_out.send_keys(Keys.DOWN)
            date_check_out.send_keys(Keys.ENTER)


    def click_confirm(self  ,type_trip ):
        if(type_trip == "aller-retour"):
            confirm_button = WebDriverWait(self, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[class="applyBtn btn btn-sm btn-success"]'))
            )
            confirm_button.click()


    def set_check_in_date_one_way_trip(self , check_in_date , type_trip):
        if(type_trip == "aller-simple"):
            date_check_in = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="calendar form-control"][id="edit-date"]'))
            )
            date_check_in.clear()
            date_check_in.send_keys(check_in_date)
            date_check_in.send_keys(Keys.ENTER)



    def click_submit(self):
        submit_button = WebDriverWait(self, 20).until(
            EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div/main/section/section/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/form/div[1]/div[2]/div[2]/div/button'))
        )
        submit_button.click()
        
    def page_loaded(self):
        
        return self.current_url  

# Récupération du premier page 

    def  get_outward_tarvel_date(self):
        date_of_departure = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="s5"]/div/span[2]'))
        ).text
        return  date_of_departure

    def  get_return_tarvel_date(self , type_trip):
        if type_trip == "aller-retour":
            date_of_arrival = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="s6"]/div[2]/span[2]'))
            ).text
            return  date_of_arrival

    def get_outward_price(self):
        outward_price = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.calendarPerBound-inner-elements-outbound .calendarPerBound-fare .selected .calendarPerBound-price .price-amount'))
        ).text
        return outward_price

    def get_return_travel_price(self , type_trip):
        if type_trip == "aller-retour":
            return_price = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.calendarPerBound-inner-elements-inbound .calendarPerBound-fare .selected .calendarPerBound-price .price-amount'))
            ).text
            return  return_price

    def getTotalPrice(self , type_trip) :
        if type_trip == "aller-retour":
            total_price = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="s9"]/div/div/div[1]/div/span/span'))
            ).text
            return total_price
        
    #next_page_button
        

    def go_to_next_page(self):
        time.sleep(1)
        button = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.tripsummary-section-btn div.tripsummary-btn.tripsummary-button-validate button.plnext-widget-btn.btn.btn-primary.tripsummary-btn-primary.tripSummary-btn-continue.tripsummary-btn-validate.validate-btn'))
        )
        button.click()
        time.sleep(1)


    # Récupération de deuxieme page

    def get_deparature_place(self):
        place_of_departure_element = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH,'/html/body/section/section/div/section/section/div[2]/div/div/section/section/div[1]/section/div/section/div[4]/span/div/span/section[1]/header/div[1]/h2/div[1]/div[1]'))
        )
        place_of_departure = place_of_departure_element.text
        return  place_of_departure
    
    def get_arrival_place(self):
        place_of_return_element = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/section/section/div/section/section/div[2]/div/div/section/section/div[1]/section/div/section/div[4]/span/div/span/section[1]/header/div[1]/h2/div[3]/div[1]'))
        )
        place_of_return = place_of_return_element.text
        return place_of_return

    def get_outward_time(self):
        self.implicitly_wait(30)
        time_and_place_of_departure_element = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#tpl3_bound0-table-flightline0 .flight-details .flight-details-bound .flight-details-departure .flight-details-city'))
        )
        time_and_place_of_departure = time_and_place_of_departure_element.text
        time_of_departure_of_outward = time_and_place_of_departure.split()[0]
        return  time_of_departure_of_outward

    def get_outward__tarvel_duration(self):
        duration_outward_trip_elem = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#tpl3_bound0-table-flightline0 #tpl3_bound0-table-flightline-details0 .row .bound-table-flightline-header .flight-details .flight-details-custom-group .flight-details-duration .duration'))
        ).text
        duration_outward_trip = duration_outward_trip_elem.split()[2]
        return  duration_outward_trip




    def get_return_travel_time(self, type_trip):
        if type_trip == "aller-retour":
            time_and_place_of_return_element = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#tpl3_bound1-table-flightline0 #tpl3_bound1-table-flightline-details0 .row .bound-table-flightline-header .flight-details .flight-details-bound .flight-details-departure .flight-details-city'))
            )
            time_and_place_of_return = time_and_place_of_return_element.text
            time_of_departure_of_return = time_and_place_of_return.split()[0]
            return  time_of_departure_of_return

    def get_return_trip_duration(self, type_trip):
        if type_trip == "aller-retour":
            duration_return_trip_elem = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#tpl3_bound1-table-flightline0 #tpl3_bound1-table-flightline-details0 .row .bound-table-flightline-header .flight-details .flight-details-custom-group .flight-details-duration .duration'))
            ).text
            duration_return_trip = duration_return_trip_elem.split()[2]
            return duration_return_trip
    def close_browser(self):
        self.quit()
    