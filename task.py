from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import csv
from matplotlib import pyplot
import matplotlib.dates as mdates
from prophet import Prophet



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
# # print("-------------------------")
# #
# money24 = Valute_to_price()
# dict_elems = {"general" : ".map__courses-list", "valute_selector" :  ".currency-node-wrapper span", "sell_selector" : "li div:first-child", "buy_selector" : "li div:last-child"}
# money24.combine("https://money24.com.ua/", dict_elems)
#
# print("-------------------------")
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

driver = webdriver.Chrome()

class Dovnloaded_valutes():
    def __init__(self, driver_link, name_of_valute, list_prices_to_sell = None, list_prices_to_buy = None, list_dates = None):
        self.driver_link = driver_link
        self.name_of_valute = name_of_valute
        self.list_prices_to_sell = list_prices_to_sell
        self.list_prices_to_buy = list_prices_to_buy
        self.list_dates = list_dates

    def all_clicks(self, list_to_click = None):
        if (list_to_click != None):
            for link in list_to_click:
                elem = driver.find_element(By.XPATH, link)
                driver.execute_script("arguments[0].click()", elem)

    def download_more(self, show_more_link):
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


    def create_list(self, link_dictionary, name_in_dict):
        elem = driver.find_element(By.CSS_SELECTOR, link_dictionary["general"])
        some_list = elem.find_elements(By.CSS_SELECTOR, link_dictionary[name_in_dict])
        some_list = [val.text for val in some_list]
        self.replace_comas(some_list)
        return some_list

    def read_file(self, file_name):
        valuta_and_date = set()
        try:
            with open(file_name, 'r', newline='') as bank:
                reader = csv.reader(bank, delimiter=',')
                header = next(reader)
                valute_index_column = header.index('valute')
                dates_index_column = header.index('date')
                for row in reader:
                    if row:
                        valuta_and_date.add((row[valute_index_column], row[dates_index_column]))
        except:
            with open(file_name, 'w', newline='') as bank:
                bank.write("valute,date,buy,sell\n")
        # print(valuta_and_date)
        return valuta_and_date

    def write_in_file(self, file_name):
        valuta_and_dates = self.read_file(file_name)
        with open(file_name, 'a') as bank:
            for i in range(len(self.list_dates)):
                new_pair = (self.name_of_valute, self.list_dates[i])
                if new_pair not in valuta_and_dates:
                    # list_to_append.append()
                    bank.write(f"{self.name_of_valute},{self.list_dates[i]},{self.list_prices_to_buy[i]},{self.list_prices_to_sell[i]}\n")


    def create(self, list_to_click, link_dictionary, file_name, show_more_link = None):
        driver.get(self.driver_link)
        self.all_clicks(list_to_click)
        self.download_more(show_more_link)
        self.list_dates = self.create_list(link_dictionary, "link_date")
        self.list_dates = [date.replace('.', '-') for date in self.list_dates]
        self.list_prices_to_sell = self.create_list(link_dictionary, "link_sell")
        self.list_prices_to_buy = self.create_list(link_dictionary, "link_buy")
        self.write_in_file(file_name)


# TODO class All_valutes, which will create a graphic


class Grafic_with_file:
    def __init__(self, file_name):
        self.file_name = file_name

    def data_for_grafic(self):
        valuta_and_date = []
        with open(self.file_name, 'r', newline='') as bank:
            reader = csv.reader(bank, delimiter=',')
            header = next(reader)
            valute_index_column = header.index('valute')
            dates_index_column = header.index('date')
            buy_index_column = header.index('buy')
            sell_index_column = header.index('sell')
            for row in reader:
                if row:
                    valuta_and_date.append([row[valute_index_column], row[dates_index_column], row[buy_index_column], row[sell_index_column]])

        dictionary_valut = {}
        for item in valuta_and_date:
            key = item[0]
            if key not in dictionary_valut:
                dictionary_valut[key] = []
            dictionary_valut[key].append(item)

        return dictionary_valut


    def graf(self, start_date_str, end_date_str):

        dictionary_valut = self.data_for_grafic()

        date_format = "%d-%m-%Y"
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)

        fig, axes = pyplot.subplots(nrows=2, ncols=1, figsize=(10, 8))

        # Налаштування формату дати для обох осей
        # Ми хочемо, щоб мітки були тільки на початку місяців
        month_locator = mdates.MonthLocator(interval=1)
        # Формат міток: скорочена назва місяця ('%b') та рік ('%Y')
        month_formatter = mdates.DateFormatter('%b %Y')

        # 1. Налаштовуємо вісь X для верхнього графіку (Купівля)
        axes[0].xaxis.set_major_locator(month_locator)
        axes[0].xaxis.set_major_formatter(month_formatter)

        # 2. Налаштовуємо вісь X для нижнього графіку (Продаж)
        axes[1].xaxis.set_major_locator(month_locator)
        axes[1].xaxis.set_major_formatter(month_formatter)


        for currency, data in dictionary_valut.items():
            data.sort(key=lambda x: datetime.strptime(x[1], "%d-%m-%Y"))
            dates_str = []
            buy_prices = []
            sell_prices = []

            for item in data:
                current_date = datetime.strptime(item[1], date_format)
                if start_date <= current_date <= end_date:
                    dates_str.append(item[1])
                    buy_prices.append(float(item[2]))
                    sell_prices.append(float(item[3]))


            dates_num = [mdates.date2num(datetime.strptime(d, "%d-%m-%Y")) for d in dates_str]

            axes[0].plot(dates_num, buy_prices, label=f"Buy {currency}")
            axes[1].plot(dates_num, sell_prices, label=f"Sell {currency}")

            # Налаштування графіків

        axes[0].set_title("Buy")
        axes[0].set_xlabel("date")
        axes[0].set_ylabel("prise")
        axes[0].legend()
        axes[0].tick_params(axis='x', rotation=45)  # Повертаємо дати для читабельності
        # axes[0].grid(True)

        axes[1].set_title("Sell")
        axes[1].set_xlabel("date")
        axes[1].set_ylabel("prise")
        axes[1].legend()
        axes[1].tick_params(axis='x', rotation=45)
        # axes[1].grid(True)

        pyplot.tight_layout()
        pyplot.show()





def enter_bank(bank_link, name_of_valute, list_to_click, link_dictionary, file_name, show_more_link = None):
    bank_currency = Dovnloaded_valutes(bank_link, name_of_valute)
    bank_currency.create(list_to_click, link_dictionary, file_name, show_more_link)

def bank_graph(start_date, end_date, file_name):
    gr = Grafic_with_file(file_name)
    gr.graf(start_date, end_date)



def menu():
    while True:
        print("What do you want to see: ")
        print("1 - data of Privat bank")
        print("2 - data of Meta bank")
        print("To stop it print other number")
        n = int(input())
        if n == 1 or n == 2:
            print("Period start (01-01-2025): ")
            start_date = input()
            print("Period end (01-01-2025): ")
            end_date = input()

        if n == 1:
            list_to_click = ["//span[@plerdy-tracking-id='35644584901']",
                             "/html/body/div[5]/article[2]/div[3]/article/div[1]/div/div/div/div[2]",
                             "//button[@plerdy-tracking-id='16681147801']"]
            link_dictionary = {"general": ".insert_table", "link_date": "tr td:nth-child(1)",
                               "link_sell": "tr td:nth-child(5)",
                               "link_buy": "tr td:nth-child(4)"}
            enter_bank("https://privatbank.ua/obmin-valiut", "USD", list_to_click, link_dictionary, "privat.csv", "div.download-more")

            list_to_click = ["//span[@plerdy-tracking-id='35644584901']", "/html/body/div[5]/article[2]/div[3]/article/div[1]/div/div/div/div[2]","//button[@plerdy-tracking-id='16681147801']", "//button[@data-id='s-r_currency_by_table']","//*[@id='bs-select-2-2']"]
            link_dictionary = {"general": ".insert_table", "link_date": "tr td:nth-child(1)",
                               "link_sell": "tr td:nth-child(5)",
                               "link_buy": "tr td:nth-child(4)"}
            enter_bank("https://privatbank.ua/obmin-valiut", "EUR", list_to_click, link_dictionary, "privat.csv",
                       "div.download-more")
            bank_graph(start_date, end_date, "privat.csv")

        elif n == 2:
            list_to_click = []
            link_dictionary = {"general" : ".editor_table tbody", "link_date" : "tr:not(:first-child) td:first-child", "link_sell" : "tr:not(:first-child) td:nth-child(4)", "link_buy" : "tr:not(:first-child) td:nth-child(3)"}
            enter_bank("https://www.mbank.com.ua/content/view/41/51/150/0/waHiddenStatus_Filter_frontGridForm_wa_rate_currency_ident,1/lang,uk/", "USD", list_to_click, link_dictionary, "meta_bank.csv")

            list_to_click = []
            link_dictionary = {"general" : ".editor_table tbody", "link_date" : "tr:not(:first-child) td:first-child", "link_sell" : "tr:not(:first-child) td:nth-child(4)", "link_buy" : "tr:not(:first-child) td:nth-child(3)"}
            enter_bank("https://www.mbank.com.ua/content/view/41/51/150/0/lang,uk/waHiddenStatus_Filter_frontGridForm_wa_rate_currency_ident,3/", "EUR", list_to_click, link_dictionary, "meta_bank.csv")
            bank_graph(start_date, end_date, "meta_bank.csv")

        else:
            return

menu()

# print("---------------------------------------------------------------------------------------555543333333333333333333333333322222222222222222222222222277777777777")
#
# meta_bank_usd = Dovnloaded_valutes("https://www.mbank.com.ua/content/view/41/51/150/0/waHiddenStatus_Filter_frontGridForm_wa_rate_currency_ident,1/lang,uk/", "USD")
# list_to_click = []
# link_dictionary = {"general" : ".editor_table tbody", "link_date" : "tr:not(:first-child) td:first-child", "link_sell" : "tr:not(:first-child) td:nth-child(4)", "link_buy" : "tr:not(:first-child) td:nth-child(3)"}
# meta_bank_usd.create(list_to_click, link_dictionary, "meta_bank.csv")
#
# print("---------------------------------------------------------------------------------------555543333333333333333333333333322222222222222222222222222277777777777")
#
# meta_bank_eur = Dovnloaded_valutes("https://www.mbank.com.ua/content/view/41/51/150/0/lang,uk/waHiddenStatus_Filter_frontGridForm_wa_rate_currency_ident,3/", "EUR")
# list_to_click = []
# link_dictionary = {"general" : ".editor_table tbody", "link_date" : "tr:not(:first-child) td:first-child", "link_sell" : "tr:not(:first-child) td:nth-child(4)", "link_buy" : "tr:not(:first-child) td:nth-child(3)"}
# meta_bank_eur.create(list_to_click, link_dictionary, "meta_bank.csv")
#
# meta_gr = Grafic_with_file("meta_bank.csv")
# meta_gr.graf()


# print("---------------------------------------------------------------------------------------555543333333333333333333333333322222222222222222222222222277777777777")
#
# meta_bank_usd = Dovnloaded_valutes("https://www.mbank.com.ua/content/view/41/51/150/150/waHiddenStatus_Filter_frontGridForm_wa_rate_currency_ident,1/lang,uk/", "USD")
# list_to_click = []
# link_dictionary = {"general" : ".editor_table tbody", "link_date" : "tr:not(:first-child) td:first-child", "link_sell" : "tr:not(:first-child) td:nth-child(3)", "link_buy" : "tr:not(:first-child) td:nth-child(4)"}
# meta_bank_usd.create(list_to_click, link_dictionary, "meta_bank.csv", "div.download-more")


# driver.close()