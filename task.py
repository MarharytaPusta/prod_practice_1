from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Valute_to_price():
    def __init__(self, list_valutes = None, list_prices_to_sell = None, list_prices_to_buy = None):
        self.list_valutes = list_valutes
        self.list_prices_to_sell = list_prices_to_sell
        self.list_prices_to_buy = list_prices_to_buy

    def creation_valutes(self, driver, link, list_elem_lv_elem_lp):
        if self.list_valutes is None:
            self.list_valutes = []
        driver.get(link)
        elem = driver.find_element(By.CLASS_NAME, list_elem_lv_elem_lp[0])
        self.list_valutes = elem.find_elements(By.CSS_SELECTOR, list_elem_lv_elem_lp[1])
        self.list_valutes = [val.text for val in self.list_valutes]

    def creation_sell(self, driver, link, list_elem_lv_elem_lp):
        if self.list_prices_to_sell is None:
            self.list_prices_to_sell = []
        driver.get(link)
        elem = driver.find_element(By.CLASS_NAME, list_elem_lv_elem_lp[2])
        self.list_prices_to_sell = elem.find_elements(By.CSS_SELECTOR, list_elem_lv_elem_lp[3])
        self.list_prices_to_sell = [val.text for val in self.list_prices_to_sell]
        print(len(self.list_prices_to_sell))
        print(self.list_prices_to_sell)
        print(len(self.list_valutes))
        len_lv = len(self.list_valutes) * 3
        if(len(self.list_prices_to_sell) > len(self.list_valutes) * 3):
            self.list_prices_to_sell = self.list_prices_to_sell[: len_lv :]
            print(self.list_prices_to_sell)
        if(len(self.list_prices_to_sell) == len(self.list_valutes) * 3):
            new_elems = []
            for i in range(len(self.list_prices_to_sell)):
                if i % 3 == 0:
                    new_elems.append(self.list_prices_to_sell[i])
            self.list_prices_to_sell = new_elems
            print(self.list_prices_to_sell)


    # def creation_buy(self, driver, link, list_elem_lv_elem_lp):
    #     if self.list_prices_to_buy is None:
    #         self.list_prices_to_buy = []
    #     driver.get(link)
    #     elem = driver.find_element(By.CLASS_NAME, list_elem_lv_elem_lp[4])
    #     self.list_prices_to_sell = elem.find_elements(By.CSS_SELECTOR, list_elem_lv_elem_lp[5])
    #     #self.print_values(driver)


    def print_values(self):
        for i in range(len(self.list_valutes)):
            print(f"{self.list_valutes[i]} : {self.list_prices_to_sell[i]}")

    def combine(self, driver, link, list_elem_lv_elem_lp):
        self.creation_valutes(driver, link, list_elem_lv_elem_lp)
        self.creation_sell(driver, link, list_elem_lv_elem_lp)
        #self.creation_buy(driver, link, list_elem_lv)
        self.print_values()
        driver.close()


driver = webdriver.Chrome()
# driver.implicitly_wait(5)
money24 = Valute_to_price()
list_elem_lv_elem_lp = ["map__courses-list", ".currency-node-wrapper span", "map__courses-list", ".map__courses-list-li div"]
money24.combine(driver, "https://money24.com.ua/", list_elem_lv_elem_lp)





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