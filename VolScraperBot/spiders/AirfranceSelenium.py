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

class Booking(uc.Chrome): 
    def __init__(self, driver_path="C:/Users/HIZEM/Desktop/PCD/VolScraperBot/chromedriver.exe"):
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--headless") 
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        super().__init__(service=Service(executable_path=driver_path))  
        self.implicitly_wait(15)
        self.maximize_window()

    def land_first_page (self) :
        self.get("https://wwws.airfrance.tn/")
        self.implicitly_wait(110)

    def accept_cookies(self):
        accept_button = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="accept_cookies_btn"]'))
        )
        accept_button.click()
        self.implicitly_wait(30)

    def click_continue_buton(self):
        time.sleep(2)
        self.implicitly_wait(30)
        continue_button = WebDriverWait(self, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-homepage-app-root/div/div[1]/bw-homepage-hero-image/div/div/div[1]/div/bw-search-widget/mat-card/form/div/div/div[1]/button'))
        )
        continue_button.click()

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

    def select_place_of_arrival(self,place_of_arrival) : # Utilisez self.place_of_departure
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

        target_month =translate_month_to_french(check_in_date.split()[1])
        i=0
        while True:
            month_name_element = self.find_element(By.CSS_SELECTOR,f'#bwc-month-{i} .bwc-month__name')
            month_name_text = month_name_element.text
            if (target_month.lower() == month_name_text.strip().lower()):
                break
            else :
                alt_xpath_element = self.find_element(By.CSS_SELECTOR, '.bwc-calendar__next-month-button .mat-mdc-button-touch-target').click()
                time.sleep(0.5)
            i = i + 1

    def select_check_in_date(self, check_in_date):
        date_check_in = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'button[class="bwc-day__button mdc-button mat-mdc-button mat-primary mat-mdc-button-base"][aria-label="{check_in_date}"]'))
        )
        date_check_in.click()



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


    def select_filter(self):
        self.implicitly_wait(30)
        meilleur_tarif = WebDriverWait(self, 20).until(
            EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-filters-bar/div/bw-flight-list-result-sort/div/bwc-form-input-container/div/mat-form-field/div[1]/div[2]/div/select/option[1]'))
        )
        meilleur_tarif.click()


    def page_loaded(self):
        return self.current_url    
    

    def  get_deparature_place(self):
        outward_trip_departure_place = WebDriverWait(self, 20).until(
        EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-itinerary-locations/bws-flight-locations/ol/li[1]'))
        ).text    
        return outward_trip_departure_place

    def get_arrival_place(self):
        outward_trip_arrival_place = WebDriverWait(self, 20).until(
        EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-itinerary-locations/bws-flight-locations/ol/li[2]')))
        arrival_text = outward_trip_arrival_place.text
        if "correspondance" in arrival_text: 
            return(WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-itinerary-locations/bws-flight-locations/ol/li[3]'))).text)
        else:
            return(arrival_text)

    def get_outward_price(self):
        outward_price = WebDriverWait(self, 20).until(
            EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[2]/div/bw-itinerary-select/button/span[2]/span/span/span[2]/bw-price/span'))
        ).text    
        return(outward_price)

    def get_outward_tarvel_date(self):
        date_outward_trip_element  = WebDriverWait(self, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR ,'p[class="bwc-o-body bw-search-fare-time__date qa-search-fare-datetime"]'))
        )
        date_outward_trip_text = date_outward_trip_element.text
        date_outward_trip = date_outward_trip_text.split(',')[0]
        return(date_outward_trip)

    def get_outward_time (self):
        outward_time_element = WebDriverWait(self, 20).until(
            EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-times/span'))
        ).text
        outward_time = outward_time_element.split(" - ")
        return(outward_time[0])
    
    def get_outward__tarvel_duration(self):
        outward_trip_duration = WebDriverWait(self, 20).until(
        EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-duration/div'))
        ).text    
        return(outward_trip_duration)
    

    def click_details_button(self):
        self.implicitly_wait(30)
        WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[2]/bw-itinerary-details-trigger/button'))).click()
        self.implicitly_wait(30)

    
    def click_exit(self):
        self.implicitly_wait(30)
        WebDriverWait(self, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR , 'button[data-test="bwsfe-flight-details__button-close"][aria-label="Fermer la fenêtre contenant les détails de votre vol"]'))).click()
        self.implicitly_wait(30)

    
    def go_to_return_travel(self,trip_type):
        if (trip_type == "aller-retour"):
            self.implicitly_wait(50)
            try :
                next_page_button_1 = WebDriverWait(self, 20).until(
                    EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[2]/div/bw-itinerary-select/button'))
                ).click()

                next_page_button_confirm = WebDriverWait(self, 20).until(
                    EC.presence_of_element_located((By.XPATH ,'//*[@id="mat-tab-content-4-0"]/div/section/div/bws-flight-upsell-item/div/div[2]/bws-flight-upsell-confirm/button/span[2]'))
                )
                self.execute_script("arguments[0].click();", next_page_button_confirm)
            except Exception as e:
                print("Error retrieving information:", e)
            self.implicitly_wait(50)

    def get_return_travel_price(self,typeoftrip):
        if typeoftrip=="aller-retour":
            return_price = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[2]/div/bw-itinerary-select/button/span[2]/span/span/span[2]/bw-price/span'))
            ).text    
            return(return_price)
    def get_return_travel_time(self,typeoftrip):
        if typeoftrip=="aller-retour":
            return_time_element = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-times/span'))
            ).text
            return_time = return_time_element.split(" - ")
            return(return_time[0])
    def get_return_trip_duration(self,typeoftrip):
        if typeoftrip=="aller-retour":
            return_trip_duration = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.XPATH , '/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[1]/bw-itinerary-row/div/div/div[1]/bws-flight-duration/div'))
            ).text    
            return(return_trip_duration)
    def get_return_tarvel_date(self,typeoftrip):
        if typeoftrip=="aller-retour":
            date_return_trip_element  = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR ,'p[class="bwc-o-body bw-search-fare-time__date qa-search-fare-datetime"]'))
            )
            date_return_trip_text = date_return_trip_element.text
            date_return_trip = date_return_trip_text.split(',')[0]
            return date_return_trip

    def close_browser(self):
        self.quit()
    
    