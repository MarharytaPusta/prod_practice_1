from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time



# Buy - гривні в долари. Я даю гривні, хочу отримати долари
# Sell - долари в гривні. Я даю долари
#
# mm
# # national_bank = Valute_to_price()
# # dict_elems1 = {"general" : "#exchangeRates tbody", "valute_selector" :  "tr td:nth-child(2)", "sell_selector" : "tr td:nth-child(5)", "buy_selector" : "tr td:nth-child(5)"}
# # national_bank.combine("https://bank.gov.ua/ua/markets/exchangerates", dict_elems1)
# #
# # print("------------------------")

# bisbank = Valute_to_price()
# # dict_elems1 = {"general" : ".module-exchange__list", "valute_selector" :  ".module-exchange__item .module-exchange__item-currency .module-exchange__item-text not(span)", "sell_selector" : ".module-exchange__item .module-exchange__item-currency .module-exchange__item-text not(span)", "buy_selector" : ".module-exchange__item .module-exchange__item-currency .module-exchange__item-text not(span)"}
# dict_elems1 = {"general" : ".tab_content .active table tbody", "valute_selector" :  "tr td:first-child", "sell_selector" : "tr td:nth-child(2)", "buy_selector" : "tr td:nth-child(3)"}
# bisbank.combine("https://www.bisbank.com.ua/kurs-valyut/", dict_elems1)
#
# # print("------------------------")
# #
# money24 = Valute_to_price()
# dict_elems = {"general" : ".map__courses-list", "valute_selector" :  ".currency-node-wrapper span", "sell_selector" : "li div:first-child", "buy_selector" : "li div:last-child"}
# money24.combine("https://money24.com.ua/", dict_elems)
#
# print("------------------------")
#
# privat_bank = Valute_to_price()
# dict_elems2 = {"general" : ".content_xl80mCnkD4 div:last-child", "valute_selector" :  ".currency_b_C9i_wbMZ div.content_w73Ioj4XNI div:first-child", "sell_selector" : ".rate_kx9iSqCXBH:nth-child(4)", "buy_selector" : ".rate_kx9iSqCXBH:nth-child(2)"}
# privat_bank.combine("https://next.privat24.ua/exchange-rates", dict_elems2)
#
# print("------------------------")
#
# globus_bank = Valute_to_price()
# dict_elems4 = {"general" : ".scrolledTable tbody", "valute_selector" :  "tr:not(:first-child) td:first-child", "sell_selector" : "tr:not(:first-child) td:nth-child(2)", "buy_selector" : "tr:not(:first-child) td:nth-child(3)"}
# globus_bank.combine("https://globusbank.com.ua/ua/kursy-valiut.html", dict_elems4)



class Dovnloaded_valutes():
    def __init__(self, driver_link, name_of_valute, list_prices_to_sell = None, list_prices_to_buy = None, list_dates = None):
        self.driver_link = driver_link
        self.name_of_valute = name_of_valute
        self.list_prices_to_sell = list_prices_to_sell
        self.list_prices_to_buy = list_prices_to_buy
        self.list_dates = list_dates

    def all_clicks(self, driver, list_to_click = None):
        if (list_to_click != None):
            for link in list_to_click:
                elem = driver.find_element(By.XPATH, link)
                driver.execute_script("arguments[0].click()", elem)

    def download_more(self, show_more_link, driver):
        if (show_more_link != None):
            wait = WebDriverWait(driver, 10)
            show_more = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, show_more_link)))
            time.sleep(2)
            while True:
                try:
                    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(show_more))
                    driver.execute_script("arguments[0].click()", button)
                    time.sleep(2)
                except TimeoutException:
                    print("Button no longer found or not clickable within the timeout")
                    break
                except NoSuchElementException:
                    print("Button not found on the page")
                    break
                except Exception:
                    print("An unexpected error occurred")
                    break

    def replace_comas(self, some_list):
        for i in range(len(some_list)):
            some_list[i] = some_list[i].replace(',', '.')

    def create_list(self, link_dictionary, name_in_dict, driver):
        elem = driver.find_element(By.CSS_SELECTOR, link_dictionary["general"])
        some_list = elem.find_elements(By.CSS_SELECTOR, link_dictionary[name_in_dict])
        some_list = [val.text for val in some_list]
        self.replace_comas(some_list)
        return some_list

    def write_in_file(self, file_name):
        with open(file_name, 'w') as bank:
            bank.write("date,buy,sell\n")
            for date, buy, sell in zip(self.list_dates, self.list_prices_to_sell, self.list_prices_to_buy):
                bank.write(f"{date},{buy},{sell}\n")

    def create(self, list_to_click, link_dictionary, file_name, show_more_link = None):
        driver = webdriver.Chrome()
        driver.get(self.driver_link)
        self.all_clicks(driver, list_to_click)
        self.download_more(show_more_link, driver)
        self.list_dates = self.create_list(link_dictionary, "link_date", driver)
        self.list_prices_to_sell = self.create_list(link_dictionary, "link_sell", driver)
        self.list_prices_to_buy = self.create_list(link_dictionary, "link_buy", driver)
        self.write_in_file(file_name)
        driver.close()







# driver = webdriver.Chrome()
# driver.get("https://privatbank.ua/obmin-valiut")

privat = Dovnloaded_valutes("https://privatbank.ua/obmin-valiut", "USD")
list_to_click = ["//span[@plerdy-tracking-id='35644584901']", "/html/body/div[5]/article[2]/div[3]/article/div[1]/div/div/div/div[2]", "//button[@plerdy-tracking-id='16681147801']"]
link_dictionary = {"general" : ".insert_table", "link_date" : "tr td:nth-child(1)", "link_sell" : "tr td:nth-child(5)", "link_buy" : "tr td:nth-child(4)"}
privat.create(list_to_click, link_dictionary, "privat.csv", "div.download-more")

###############################################
"""
wait = WebDriverWait(driver, 10)

elem = driver.find_element(By.XPATH, "//span[@plerdy-tracking-id='35644584901']")
driver.execute_script("arguments[0].click()", elem)
elem = driver.find_element(By.XPATH, "/html/body/div[5]/article[2]/div[3]/article/div[1]/div/div/div/div[2]")
driver.execute_script("arguments[0].click()", elem)
elem = driver.find_element(By.XPATH, "//button[@plerdy-tracking-id='16681147801']")
driver.execute_script("arguments[0].click()", elem)

show_more = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.download-more")))
time.sleep(2)
while True:
    try:
        button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable(show_more)
        )
        driver.execute_script("arguments[0].click()", button)
        #     time.sleep(2)
    except TimeoutException:
        # The button was not found within the timeout, indicating it's gone
        print("Button no longer found or not clickable within the timeout.")
        break
    except NoSuchElementException:
        # The button is not present on the page
        print("Button not found on the page.")
        break
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        break
# while len(new_dates) > len(dates):
#     driver.execute_script("arguments[0].click()", show_more)
#     time.sleep(2)
#     dates = new_dates
#     i += 1
#     print(i)
#     new_dates = elem.find_elements(By.CSS_SELECTOR, "tr")
    #new_dates = elem.find_elements(By.CSS_SELECTOR, "tr")
name_of_valute = "USD"

elem = driver.find_element(By.CSS_SELECTOR, ".insert_table")
list_buy = elem.find_elements(By.CSS_SELECTOR, "tr td:nth-child(4)")
list_buy = [val.text for val in list_buy]
replace_comas(list_buy)

# elem = driver.find_element(By.CSS_SELECTOR, ".insert_table")
list_sell = elem.find_elements(By.CSS_SELECTOR, "tr td:nth-child(5)")
list_sell = [val.text for val in list_sell]
replace_comas(list_sell)

# elem = driver.find_element(By.CSS_SELECTOR, ".insert_table")
list_date = elem.find_elements(By.CSS_SELECTOR, "tr td:nth-child(1)")
list_date = [val.text for val in list_date]
replace_comas(list_date)

with open ("privat.csv", 'w') as bank:
    bank.write("date,buy,sell\n")
    for date,buy,sell in zip(list_date, list_buy, list_sell):
        bank.write(f"{date},{buy},{sell}\n")


print(list_buy)
print("--------------------------------------"*10)
print(list_sell)
print("--------------------------------------"*10)
print(list_date)
print("---------")
#
# list_buy = elem.find_elements(By.CSS_SELECTOR, ".module-exchange__item  div:nth-child(2) .module-exchange__item-text span")
# list_buy = [val.text for val in list_buy]
# print(list_buy)
# print("---------")
#
# list_sell = elem.find_elements(By.CSS_SELECTOR, ".module-exchange__item  div:nth-child(4) .module-exchange__item-text span")
# list_sell = [val.text for val in list_sell]
# print(list_sell)
# print("---------")
#
# driver.implicitly_wait(3)
# elem = driver.find_element(By.XPATH, "/html/body/main/section[2]/div/div[1]/div/input")
# print(elem)
# elem.click()
# elem2 = driver.find_element(By.XPATH, "/html/body/main/section[2]/div/div[1]/div/div/div/div[2]/div[10]")
# elem2.click()
#
# elem = driver.find_element(By.CSS_SELECTOR, ".module-exchange__list")
# list_valutes = elem.find_elements(By.CSS_SELECTOR, ".module-exchange__item .module-exchange__item-currency .module-exchange__item-text")

# elem = driver.find_element(By.NAME, "a")
# elem.send_keys("pip")
# elem.send_keys(Keys.RETURN)


driver.close()
"""