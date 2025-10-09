from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Valute_to_price():
    def __init__(self, list_valutes = None, list_prices_to_sell = None, list_prices_to_buy = None):
        self.list_valutes = list_valutes
        self.list_prices_to_sell = list_prices_to_sell
        self.list_prices_to_buy = list_prices_to_buy

    def creation_list(self, driver, dict_elems, for_selector):

        elem = driver.find_element(By.CSS_SELECTOR, dict_elems["general"])
        list_for_class = elem.find_elements(By.CSS_SELECTOR, dict_elems[for_selector])
        list_for_class = [val.text for val in list_for_class]
        return list_for_class

    def print_values(self):
        for i in range(len(self.list_valutes)):
            print(f"{self.list_valutes[i]} : {self.list_prices_to_sell[i]} / {self.list_prices_to_buy[i]}")

    def combine(self, link, dict_elems):
        driver = webdriver.Chrome()
        driver.implicitly_wait(2)
        driver.get(link)
        self.list_valutes = self.creation_list(driver, dict_elems, "valute_selector")
        self.list_prices_to_sell = self.creation_list(driver, dict_elems, "sell_selector")
        self.list_prices_to_buy = self.creation_list(driver, dict_elems, "buy_selector")
        self.print_values()
        driver.close()



# Buy - гривні в долари. Я даю гривні, хочу отримати долари
# Sell - долари в гривні. Я даю долари
#
# national_bank = Valute_to_price()
# dict_elems1 = {"general" : "#exchangeRates tbody", "valute_selector" :  "tr td:nth-child(2)", "sell_selector" : "tr td:nth-child(5)", "buy_selector" : "tr td:nth-child(5)"}
# national_bank.combine("https://bank.gov.ua/ua/markets/exchangerates", dict_elems1)
#
# print("------------------------")

national_bank = Valute_to_price()
dict_elems1 = {"general" : ".module-exchange__list", "valute_selector" :  ".module-exchange__item .module-exchange__item-currency .module-exchange__item-text not(span)", "sell_selector" : ".module-exchange__item .module-exchange__item-currency .module-exchange__item-text not(span)", "buy_selector" : ".module-exchange__item .module-exchange__item-currency .module-exchange__item-text not(span)"}
national_bank.combine("https://kredobank.com.ua/info/kursy-valyut/commercial", dict_elems1)
#
# print("------------------------")
#
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
#
