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
        print("----------------------")
        print(self.list_prices_to_buy)
        print("----------------------")


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
# driver.implicitly_wait(5)
money24 = Valute_to_price()
dict_elems = {"general" : ".map__courses-list", "valute_selector" :  ".currency-node-wrapper span", "sell_selector" : "li div:first-child", "buy_selector" : "li div:last-child"}
money24.combine(driver, "https://money24.com.ua/", dict_elems)






#
# driver.get("https://money24.com.ua/")
# elem = driver.find_element(By.CLASS_NAME, "map__courses-list")
# elems = elem.find_elements(By.CSS_SELECTOR, ".map__courses-list-li div")

# new_elems = []
# for i in range(0, len(elems)):
#     if i % 3 == 0:
#         new_elems.append(elems[i])
#         new_elems.append(elems[i+2])
# for c in new_elems:
#     print(c.text)
#
# driver.close()

# print("----------------------------------------------------------------------------------------------------------------------------------\n"
#       "----------------------------------------------------------------------------------------------------------------------------------\n"
#       "----------------------------------------------------------------------------------------------------------------------------------\n"
#       "----------------------------------------------------------------------------------------------------------------------------------\n")
#
#
#
#
# """
# driver = webdriver.Chrome()
# driver.get("https://bank.gov.ua/ua/markets/exchangerates")
#
#
# # test1Element = driver.find_element(By.TAG_NAME, "table")
# # print(test1Element)
# # elems = test1Element.find_elements(By.CSS_SELECTOR, "td a")
# #
# # for el in elems:
# #     print(el.text)
#
# # elem = driver.find_elements(By.CLASS_NAME, "value-name")
# # elems = list()
# # for el in elem:
# #     elems = list(set(el.find_elements(By.CSS_SELECTOR, "a")).union(elems))
# # for c in elems:
# #     print(c.text)
# # driver.close()
#
#
# driver.get("https://money24.com.ua/")
# elem = driver.find_element(By.CLASS_NAME, "map__courses-list")
# elems = elem.find_elements(By.CSS_SELECTOR, ".currency-node-wrapper span")
# for c in elems:
#     print(c.text)
# driver.close()
#
# # elem = driver.find_element(By.NAME, "q")
# # elem.send_keys("pip")
# # elem.send_keys(Keys.RETURN)
# # elem = driver.find_element(By.CLASS_NAME, "list-recent-events")
# # childs = elem.find_elements(By.CSS_SELECTOR, "li a")
# #
# # for c in childs:
# #     print(c.text)
# # driver.close()
# """