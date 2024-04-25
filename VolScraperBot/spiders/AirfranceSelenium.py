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
import re
class Booking(uc.Chrome): 
    def __init__(self, driver_path="C:/Users/HIZEM/Desktop/VolScraper/VolScraperBot/chromedriver.exe"):
        opts = uc.ChromeOptions()
        opts.add_argument("--headless") 
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        serv= Service(executable_path=driver_path)
        super().__init__(service=serv) 
        self.maximize_window()

    def land_first_page (self) :
        self.get("https://wwws.airfrance.tn/")
        self.implicitly_wait(60)

    def accept_cookies(self):
        self.implicitly_wait(30)
        accept_button = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="accept_cookies_btn"]'))
        )
        accept_button.click()
        self.implicitly_wait(30)

    def click_continue_buton(self):
        time.sleep(1.5)
        continue_button = WebDriverWait(self, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="bwsfe-widget__open-search-button"][aria-controls="bw-search-widget-expandable"]'))
        )
        continue_button.click()
        self.implicitly_wait(60)


    def select_type(self,type_of_travel):
        if (type_of_travel == "aller-simple"):
            type_trip = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-homepage-app-root/div/div[1]/bw-homepage-hero-image/div/div/div[1]/div/bw-search-widget/mat-card/form/div/div[1]/div[1]/bwc-form-input-container/div/label/bwc-form-select/div[1]/mat-form-field/div[1]/div/div[2]/select/option[2]'))
            )
            type_trip.click()

    def select_place_of_departure(self,place_of_departure) :
        country_of_departure = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-test-value="origin"][placeholder="Départ de"]'))
        )
        country_of_departure.send_keys(place_of_departure)
        country_of_departure.send_keys(Keys.ENTER)            

    def select_place_of_arrival(self,place_of_arrival) : 
        country_of_arrival = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-test-value="destination"][ placeholder="Arrivée à"]'))
        )
        country_of_arrival.send_keys(place_of_arrival)
        country_of_arrival.send_keys(Keys.ENTER)
       
    def open_calandar(self,type_of_travel):
        if (type_of_travel == "aller-retour"):
            calendar = self.find_element(By.CSS_SELECTOR, 'span[class="bwc-body-1 bw-search-datepicker__travel-date"]')
            calendar.click()
        else :
            calendar = self.find_element(By.CSS_SELECTOR, 'span.bwc-body-1.bw-search-datepicker__travel-date')
            calendar.click()
                

            
    def scrol_to_check_in_date(self, check_in_date):
        def translate_month_to_french(month):
            month_mapping = {
                "January": "Janvier",
                "February": "Février",
                "March": "Mars",
                "April": "Avril",
                "May": "Mai",
                "June": "Juin",
                "July": "Juillet",
                "August": "Août",
                "September": "Septembre",
                "October": "Octobre",
                "November": "Novembre",
                "December": "Décembre"
            }
            return month_mapping.get(month, "")

        target_month_elem = check_in_date.split()[1]
        target_month =translate_month_to_french(target_month_elem)
        i=0
        while True:
            month_name_text_1 = self.find_element(By.CSS_SELECTOR,f'.bwc-calendar__month.ng-star-inserted.viewPortMonth #bwc-month-{i} .bwc-month__name.bwc-o-subheading').text
            month_name_text_2 = self.find_element(By.CSS_SELECTOR,f'.bwc-calendar__month.ng-star-inserted.viewPortMonth #bwc-month-{i+1} .bwc-month__name.bwc-o-subheading').text 
            if (target_month.lower() == (month_name_text_1.strip()).lower()):
                break
            elif (target_month.lower() == (month_name_text_2.strip()).lower()):
                break            
            else :
                self.find_element(By.CSS_SELECTOR, '.bwc-calendar__next-month-button .mat-mdc-button-touch-target').click()
                time.sleep(1)
            i += 1
        return i

    def select_check_in_date(self, check_in_date):
        date_check_in = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'button[aria-label="{check_in_date}"][class="bwc-day__button mdc-button mat-mdc-button mat-primary mat-mdc-button-base"]'))
        )
        date_check_in.click()

    def scrol_to_check_out_date(self, check_out_date, type_of_travel ,i):
        if (type_of_travel == "aller-retour"):

            def translate_month_to_french(month):
                month_mapping = {
                    "January": "Janvier",
                    "February": "Février",
                    "March": "Mars",
                    "April": "Avril",
                    "May": "Mai",
                    "June": "Juin",
                    "July": "Juillet",
                    "August": "Août",
                    "September": "Septembre",
                    "October": "Octobre",
                    "November": "Novembre",
                    "December": "Décembre"
                }
                return month_mapping.get(month, "")

            target_month_elem = check_out_date.split()[1]
            target_month =translate_month_to_french(target_month_elem)
            while True:
                month_name_text_1 = self.find_element(By.CSS_SELECTOR,f'.bwc-calendar__month.ng-star-inserted.viewPortMonth #bwc-month-{i} .bwc-month__name.bwc-o-subheading').text
                month_name_text_2 = self.find_element(By.CSS_SELECTOR,f'.bwc-calendar__month.ng-star-inserted.viewPortMonth #bwc-month-{i+1} .bwc-month__name.bwc-o-subheading').text 
                if (target_month.lower() == (month_name_text_1.strip()).lower()):
                    break
                elif (target_month.lower() == (month_name_text_2.strip()).lower()):
                    break            
                else :
                    self.find_element(By.CSS_SELECTOR, '.bwc-calendar__next-month-button .mat-mdc-button-touch-target').click()
                    time.sleep(1.5)
                i += 1

    def select_check_out_date (self,check_out_date,typeoftrip):
        if typeoftrip=="aller-retour":
            date_check_out = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'button[class="bwc-day__button mdc-button mat-mdc-button mat-primary mat-mdc-button-base"][aria-label="{check_out_date}"]'))
            )
            date_check_out.click()


    def click_confirm (self):
        confirm_button = WebDriverWait(self, 20).until(
               EC.visibility_of_element_located((By.XPATH, '//*[@id="cdk-overlay-2"]/bwc-calendar/div/div[3]/button[2]/span[2]'))
        )
        confirm_button.click()



    def click_submit(self):
        submit_button = WebDriverWait(self, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-homepage-app-root/div/div[1]/bw-homepage-hero-image/div/div/div[1]/div/bw-search-widget/mat-card/form/div/div[2]/div[2]/button/span[2]'))
        )
        submit_button.click()


    def select_filter_outward(self):
        self.implicitly_wait(60)
        WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-filters-bar/div/bw-flight-list-result-sort/div/bwc-form-input-container/div/mat-form-field/div[1]/div[2]/div/select/option[1]'))).click()
        time.sleep(1)

    def select_filter_return(self , typeoftrip):
        if typeoftrip=="aller-retour":
            self.implicitly_wait(60)
            WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-filters-bar/div/bw-flight-list-result-sort/div/bwc-form-input-container/div/mat-form-field/div[1]/div[2]/div/select/option[1]'))).click()
            time.sleep(1)

    def page_loaded(self):
        return self.current_url    
    

    def get_deparature_place(self):
        outward_trip_departure_place_elem = WebDriverWait(self, 20).until(
        EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-itinerary-locations/bws-flight-locations/ol/li[1]'))
        ).text 
        outward_trip_departure_place = outward_trip_departure_place_elem.split()[0].upper()
        return outward_trip_departure_place
    
    def get_deparature_place_abr(self):
        outward_trip_departure_place_elem = WebDriverWait(self, 20).until(
        EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-itinerary-locations/bws-flight-locations/ol/li[1]'))
        ).text 
        outward_trip_departure_place = outward_trip_departure_place_elem.split()[1].upper()
        res = re.search(r'\((.*?)\)', outward_trip_departure_place).group(1).upper()
        return res
    

    def get_arrival_place(self):
        outward_trip_arrival_place_elem = WebDriverWait(self, 20).until(
        EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-itinerary-locations/bws-flight-locations/ol/li[2]')))
        outward_trip_arrival_place = outward_trip_arrival_place_elem.text
        if "correspondance" in outward_trip_arrival_place:
            outward_trip_arrival_place_elem = WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-itinerary-locations/bws-flight-locations/ol/li[3]'))).text 
            outward_trip_arrival_place = outward_trip_arrival_place_elem.split()[0]
            return(outward_trip_arrival_place)
        else:
            return(outward_trip_arrival_place.split()[0].upper())
        
    def get_arrival_place_abr(self):
        outward_trip_arrival_place_elem = WebDriverWait(self, 20).until(
        EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-itinerary-locations/bws-flight-locations/ol/li[2]')))
        outward_trip_arrival_place = outward_trip_arrival_place_elem.text
        if "correspondance" in outward_trip_arrival_place:
            outward_trip_arrival_place_elem = WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-itinerary-locations/bws-flight-locations/ol/li[3]'))).text 
            outward_trip_arrival_place = outward_trip_arrival_place_elem.split()[1]
            res = re.search(r'\((.*?)\)', outward_trip_arrival_place).group(1).upper()
            return res
        else:
            outward_trip_arrival_place.split()[1].upper()
            res = re.search(r'\((.*?)\)', outward_trip_arrival_place).group(1).upper()
            return(res)
        
    def get_outward_price(self):
        outward_price_elem = WebDriverWait(self, 20).until(
            EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[2]/div/bw-itinerary-select/button/span[2]/span/span/span[2]/bw-price/span'))
        ).text  
        outward_price = outward_price_elem.split()[0]
        return(outward_price)

    def get_outward_tarvel_date(self):
        self.implicitly_wait(30)
        date_outward_trip_element  = WebDriverWait(self, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR ,'.bw-search-fare-time .bwc-o-body.bw-search-fare-time__date.qa-search-fare-datetime'))
        )
        date_outward_trip_text = date_outward_trip_element.text
        date_outward_trip = date_outward_trip_text.split(',')[0]
        self.implicitly_wait(30)
        return(date_outward_trip)

    def get_outward_departure_time (self):
        outward_time_element = WebDriverWait(self, 20).until(
            EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-times/span'))
        ).text
        outward_time_1 = outward_time_element.split(" - ")[0]
        outward_time = outward_time_1.split()[0]
        return(outward_time)
    
    def get_outward_arrival_time (self):
        outward_time_element = WebDriverWait(self, 20).until(
            EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-times/span'))
        ).text
        outward_time_1 = outward_time_element.split(" - ")[1]
        outward_time = outward_time_1.split()[1]
        return(outward_time)
    
    def get_outward__tarvel_duration(self):
        outward_trip_duration = WebDriverWait(self, 20).until(
        EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-duration/div'))
        ).text    
        return(outward_trip_duration)
    

    def click_details_button_outward(self):
        self.implicitly_wait(30)
        WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[2]/bw-itinerary-details-trigger/button'))).click()
        time.sleep(1.5)
        
    def click_details_button_return(self , trip_type):
        if (trip_type == "aller-retour"):
            self.implicitly_wait(30)
            WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[2]/bw-itinerary-details-trigger/button'))).click()
            time.sleep(1.5)
    
    def click_exit_outward(self):
        self.implicitly_wait(30)
        WebDriverWait(self, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR , 'button[data-test="bwsfe-flight-details__button-close"][aria-label="Fermer la fenêtre contenant les détails de votre vol"]'))).click()
        self.implicitly_wait(30)
        
    def click_exit_return(self , trip_type):
        if (trip_type == "aller-retour"):
            self.implicitly_wait(30)
            WebDriverWait(self, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR , 'button[data-test="bwsfe-flight-details__button-close"][aria-label="Fermer la fenêtre contenant les détails de votre vol"]'))).click()
            self.implicitly_wait(30)

    
    def go_to_return_travel(self,trip_type):
        if (trip_type == "aller-retour"):
            self.implicitly_wait(50)
            WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[2]/div/bw-itinerary-select/button'))).click()
            self.implicitly_wait(50)
            next_page_button_confirm = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR ,'button[class="bws-flight-upsell-confirm__button mdc-button mdc-button--raised mat-mdc-raised-button mat-accent mat-mdc-button-base"][data-test="bws-flight-upsell-confirm__button"]'))
            )
            self.execute_script("arguments[0].click();", next_page_button_confirm)
            self.implicitly_wait(50)
            time.sleep(1)


    def get_return_travel_price(self,typeoftrip):
        if typeoftrip == "aller-retour":
            return_price_elem = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[2]/div/bw-itinerary-select/button/span[2]/span/span/span[2]/bw-price/span'))
            ).text
            return_price = return_price_elem.split()[0]
            return(return_price)
    def get_return_departure_time(self,typeoftrip):
        if typeoftrip == "aller-retour":
            return_time_element = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-times/span'))
            ).text
            return_time_1 = return_time_element.split(" - ")[0]
            return_time = return_time_1.split()[0]
            return(return_time)
    def get_return_arrival_time(self,typeoftrip):
        if typeoftrip == "aller-retour":
            return_time_element = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-times/span'))
            ).text
            return_time_1 = return_time_element.split(" - ")[1]
            return_time = return_time_1.split()[1]
            return(return_time)
    def get_return_trip_duration(self,typeoftrip):
        if typeoftrip == "aller-retour":
            return_trip_duration = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-duration/div'))
            ).text    
            return(return_trip_duration)
    def get_return_tarvel_date(self,typeoftrip):
        if typeoftrip == "aller-retour":
            self.implicitly_wait(60)
            date_return_trip_element  = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR ,'p[class="bwc-o-body bw-search-fare-time__date qa-search-fare-datetime"]'))
            )
            date_return_trip_text = date_return_trip_element.text
            date_return_trip = date_return_trip_text.split(',')[0]
            return date_return_trip

    def close_browser(self):
        self.quit()
    
    