from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Valute_to_price():
    def __init__(self, list_valutes = None, list_prices_to_sell = None, list_prices_to_buy = None):
        self.list_valutes = list_valutes
        self.list_prices_to_sell = list_prices_to_sell
        self.list_prices_to_buy = list_prices_to_buy

    def creation_valutes(self, driver, link, dict_elems):
        if self.list_valutes is None:
            self.list_valutes = []
        driver.get(link)
        elem = driver.find_element(By.CSS_SELECTOR, dict_elems["general"])
        self.list_valutes = elem.find_elements(By.CSS_SELECTOR, dict_elems["valute_selector"])
        self.list_valutes = [val.text for val in self.list_valutes]

    def creation_sell(self, driver, link, dict_elems):
        if self.list_prices_to_sell is None:
            self.list_prices_to_sell = []
        driver.get(link)
        elem = driver.find_element(By.CSS_SELECTOR, dict_elems["general"])
        self.list_prices_to_sell = elem.find_elements(By.CSS_SELECTOR, dict_elems["sell_selector"])
        self.list_prices_to_sell = [val.text for val in self.list_prices_to_sell]


    def creation_buy(self, driver, link, dict_elems):
        if self.list_prices_to_buy is None:
            self.list_prices_to_buy = []
        driver.get(link)
        elem = driver.find_element(By.CSS_SELECTOR, dict_elems["general"])
        self.list_prices_to_buy = elem.find_elements(By.CSS_SELECTOR, dict_elems["buy_selector"])
        self.list_prices_to_buy = [val.text for val in self.list_prices_to_buy]


    def print_values(self):
        for i in range(len(self.list_valutes)):
            print(f"{self.list_valutes[i]} : {self.list_prices_to_sell[i]} / {self.list_prices_to_buy[i]}")

    def combine(self, driver, link, dict_elems):
        self.creation_valutes(driver, link, dict_elems)
        self.creation_sell(driver, link, dict_elems)
        self.creation_buy(driver, link, dict_elems)
        self.print_values()
        driver.close()


driver = webdriver.Chrome()
driver.implicitly_wait(3)
# money24 = Valute_to_price()
# dict_elems = {"general" : ".map__courses-list", "valute_selector" :  ".currency-node-wrapper span", "sell_selector" : "li div:first-child", "buy_selector" : "li div:last-child"}
# money24.combine(driver, "https://money24.com.ua/", dict_elems)

# national_bank = Valute_to_price()
# dict_elems = {"general" : "#exchangeRates tbody", "valute_selector" :  "tr td:nth-child(2)", "sell_selector" : "tr td:nth-child(5)", "buy_selector" : "tr td:nth-child(5)"}
# national_bank.combine(driver, "https://bank.gov.ua/ua/markets/exchangerates", dict_elems)

privat_bank = Valute_to_price()
dict_elems = {"general" : ".content_xl80mCnkD4 div:last-child", "valute_selector" :  ".currency_b_C9i_wbMZ div.content_w73Ioj4XNI div:first-child", "sell_selector" : ".rate_kx9iSqCXBH:nth-child(4)", "buy_selector" : ".rate_kx9iSqCXBH:nth-child(2)"}
privat_bank.combine(driver, "https://next.privat24.ua/exchange-rates", dict_elems)

# driver.get("https://next.privat24.ua/exchange-rates")
# elem = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/section/div/div[2]/div[1]/div/div[2]/div[3]/div[2]")
# elem = driver.find_element(By.CSS_SELECTOR, ".content_xl80mCnkD4 div:last-child") #general
# elems = elem.find_elements(By.CSS_SELECTOR, ".rate_kx9iSqCXBH:nth-child(2)") #BUY
# elems = elem.find_elements(By.CSS_SELECTOR, ".rate_kx9iSqCXBH:nth-child(4)") #SALE
# elems = elem.find_elements(By.CSS_SELECTOR, ".currency_b_C9i_wbMZ div.content_w73Ioj4XNI div:first-child" ) #Currency
#
# for el in elems:
#     print("\n\n")
#     print(el.get_attribute("outerHTML"))
# print(elems)
# lst = [l.text for l in elems]
# print(lst)
# for el in elems:
#     print(el.text)
# elem = elem.find_element(By.CSS_SELECTOR, "")
# print(elem.get_attribute("innerHTML"))
# list_valutes = elem.find_elements(By.CSS_SELECTOR, "#plerdy-tracking-id")
# list_valutes = [val.text for val in list_valutes]
# for i in range(len(list_valutes)):
#     print(f"{list_valutes[i]}")

