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
import numpy as np
from datetime import timedelta
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome()
# driver = webdriver.Chrome(options=options)

class DovnloadedСurrency():
    def __init__(self, driver_link, name_of_currency, list_prices_to_sell = None, list_prices_to_buy = None, list_dates = None):
        self.driver_link = driver_link
        self.name_of_currency = name_of_currency
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
                    break
                except NoSuchElementException:
                    break
                except Exception:
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
        currency_and_date = set()
        try:
            with open(file_name, 'r', newline='') as bank:
                reader = csv.reader(bank, delimiter=',')
                header = next(reader)
                currency_index_column = header.index('currency')
                dates_index_column = header.index('date')
                for row in reader:
                    if row:
                        currency_and_date.add((row[currency_index_column], row[dates_index_column]))
        except:
            with open(file_name, 'w', newline='') as bank:
                bank.write("currency,date,buy,sell\n")
        return currency_and_date

    def write_in_file(self, file_name):
        currency_and_dates = self.read_file(file_name)
        with open(file_name, 'a') as bank:
            for i in range(len(self.list_dates)):
                new_pair = (self.name_of_currency, self.list_dates[i])
                if new_pair not in currency_and_dates:
                    bank.write(f"{self.name_of_currency},{self.list_dates[i]},{self.list_prices_to_buy[i]},{self.list_prices_to_sell[i]}\n")


    def create(self, list_to_click, link_dictionary, file_name, show_more_link = None):
        driver.get(self.driver_link)
        self.all_clicks(list_to_click)
        self.download_more(show_more_link)
        self.list_dates = self.create_list(link_dictionary, "link_date")
        self.list_dates = [date.replace('.', '-') for date in self.list_dates]
        self.list_prices_to_sell = self.create_list(link_dictionary, "link_sell")
        self.list_prices_to_buy = self.create_list(link_dictionary, "link_buy")
        self.write_in_file(file_name)




class Grafic_with_file:
    def __init__(self, file_name):
        self.file_name = file_name

    def data_for_grafic(self):
        currency_and_date = []
        with open(self.file_name, 'r', newline='') as bank:
            reader = csv.reader(bank, delimiter=',')
            header = next(reader)
            currency_index_column = header.index('currency')
            dates_index_column = header.index('date')
            buy_index_column = header.index('buy')
            sell_index_column = header.index('sell')
            for row in reader:
                if row:
                    currency_and_date.append([row[currency_index_column], row[dates_index_column], row[buy_index_column], row[sell_index_column]])

        dictionary_currency = {}
        for item in currency_and_date:
            key = item[0]
            if key not in dictionary_currency:
                dictionary_currency[key] = []
            dictionary_currency[key].append(item)

        return dictionary_currency

    def predict_currency_rate(self, dates_num, prices, num_days=30, window=7, jump_factor=0.5):
        if len(dates_num) < window:
            return [], []

        last_ma = np.mean(prices[-window:])
        prev_prices_segment = prices[-(window * 2):-window]
        prev_ma = np.mean(prev_prices_segment) if len(prev_prices_segment) == window else last_ma

        step = (last_ma - prev_ma) / window

        price_diffs = np.diff(prices)
        if len(price_diffs) > 0:
            max_daily_change = np.max(np.abs(price_diffs))
        else:
            max_daily_change = 0.5

        jump_limit = max_daily_change * jump_factor


        last_date_num = dates_num[-1]
        predict_dates_num = np.arange(last_date_num + 1, last_date_num + 1 + num_days)

        predicted_prices = []
        current_prediction = prices[-1]

        for i in range(num_days):
            random_jump_val = np.random.uniform(-1, 1)

            daily_change = step + (random_jump_val * jump_limit)

            current_prediction += daily_change
            predicted_prices.append(current_prediction)

        return predict_dates_num, np.array(predicted_prices)



    def graf(self, start_date_str, end_date_str, predict_days=0):
        dictionary_currency = self.data_for_grafic()

        date_format = "%d-%m-%Y"
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)

        if predict_days > 0:
            final_end_date = end_date + timedelta(days=predict_days)
        else:
            final_end_date = end_date

        fig, axes = pyplot.subplots(nrows=2, ncols=1, figsize=(10, 8))

        month_locator = mdates.MonthLocator(interval=1)
        month_formatter = mdates.DateFormatter('%b %Y')

        axes[0].xaxis.set_major_locator(month_locator)
        axes[0].xaxis.set_major_formatter(month_formatter)

        axes[1].xaxis.set_major_locator(month_locator)
        axes[1].xaxis.set_major_formatter(month_formatter)

        for currency, data in dictionary_currency.items():
            data.sort(key=lambda x: datetime.strptime(x[1], "%d-%m-%Y"))
            dates_str_all = [item[1] for item in data]
            buy_prices_all = [float(item[2]) for item in data]
            sell_prices_all = [float(item[3]) for item in data]

            dates_num_all = [mdates.date2num(datetime.strptime(d, "%d-%m-%Y")) for d in dates_str_all]

            if predict_days > 0:
                pred_dates_buy, pred_prices_buy = self.predict_currency_rate(dates_num_all, buy_prices_all,
                                                                             predict_days, 7, 0.30)
                pred_dates_sell, pred_prices_sell = self.predict_currency_rate(dates_num_all, sell_prices_all,
                                                                               predict_days, 7, 0.30)

            dates_num_plot = []
            buy_prices_plot = []
            sell_prices_plot = []

            for i, item in enumerate(data):
                current_date = datetime.strptime(item[1], date_format)
                if start_date <= current_date <= end_date:
                    dates_num_plot.append(dates_num_all[i])
                    buy_prices_plot.append(buy_prices_all[i])
                    sell_prices_plot.append(sell_prices_all[i])

            axes[0].plot(dates_num_plot, buy_prices_plot, label=f"Buy {currency}", linewidth=2)
            axes[1].plot(dates_num_plot, sell_prices_plot, label=f"Sell {currency}", linewidth=2)

            if predict_days > 0 and dates_num_plot:
                last_color = axes[0].lines[-1].get_color()

                axes[0].plot([dates_num_plot[-1], pred_dates_buy[0]],
                             [buy_prices_plot[-1], pred_prices_buy[0]],
                             linestyle='--', color=last_color, linewidth=1)
                axes[0].plot(pred_dates_buy, pred_prices_buy,
                             label=f"Buy {currency} (Forecast)",
                             linestyle='--', color=last_color, linewidth=1)

                axes[1].plot([dates_num_plot[-1], pred_dates_sell[0]],
                             [sell_prices_plot[-1], pred_prices_sell[0]],
                             linestyle='--', color=last_color, linewidth=1)
                axes[1].plot(pred_dates_sell, pred_prices_sell,
                             label=f"Sell {currency} (Forecast)",
                             linestyle='--', color=last_color, linewidth=1)

        if dates_num_plot:
            min_x = mdates.date2num(start_date)
            max_x = mdates.date2num(final_end_date)
            axes[0].set_xlim(min_x, max_x)
            axes[1].set_xlim(min_x, max_x)

        pred_str = f" & {predict_days}-Day Forecast" if predict_days > 0 else ''

        axes[0].set_title(f"Buy Rate (History{pred_str})")
        axes[0].set_xlabel("Date")
        axes[0].set_ylabel("Price")
        axes[0].legend()
        axes[0].tick_params(axis='x', rotation=45)

        axes[1].set_title(f"Sell Rate (History{pred_str})")
        axes[1].set_xlabel("Date")
        axes[1].set_ylabel("Price")
        axes[1].legend()
        axes[1].tick_params(axis='x', rotation=45)

        pyplot.tight_layout()
        pyplot.show()





def enter_bank(bank_link, name_of_currency, list_to_click, link_dictionary, file_name, show_more_link = None):
    bank_currency = DovnloadedСurrency(bank_link, name_of_currency)
    bank_currency.create(list_to_click, link_dictionary, file_name, show_more_link)

def bank_graph(start_date, end_date, file_name, predict_days=0):
    gr = Grafic_with_file(file_name)
    gr.graf(start_date, end_date, predict_days)


def menu():
    print("Do you want to update the data?")
    print("1 - Yes (a little bit longer)")
    print("something else if no")
    try:
        is_update = int(input())
    except:
        is_update = 0
        pass

    file_privat = "privat.csv"
    file_meta = "meta_bank.csv"
    if is_update == 1:
        try:
            print("...please wait...")
            list_to_click = ["//*[@id='archive-block']", "//*[@id='table-currency']",
                             "//*[@id='one_year_by_table']"]
            link_dictionary = {"general": ".insert_table", "link_date": "tr td:nth-child(1)",
                               "link_sell": "tr td:nth-child(5)", "link_buy": "tr td:nth-child(4)"}
            # enter_bank("https://privatbank.ua/obmin-valiut", "USD", list_to_click, link_dictionary, file_privat,
            #            "div.download-more")

            list_to_click.append("//*[@id='mainWrapArchive']/div[2]/article/div/div[1]/div[3]/div/button/div")
            list_to_click.append("//*[@id='bs-select-2-2']")
            enter_bank("https://privatbank.ua/obmin-valiut", "EUR", list_to_click, link_dictionary, file_privat,
                       "div.download-more")

            link_dictionary = {"general": ".editor_table tbody", "link_date": "tr:not(:first-child) td:first-child",
                               "link_sell": "tr:not(:first-child) td:nth-child(4)",
                               "link_buy": "tr:not(:first-child) td:nth-child(3)"}
            enter_bank(
                "https://www.mbank.com.ua/content/view/41/51/150/0/waHiddenStatus_Filter_frontGridForm_wa_rate_currency_ident,1/lang,uk/",
                "USD", [], link_dictionary, file_meta)

            link_dictionary = {"general": ".editor_table tbody", "link_date": "tr:not(:first-child) td:first-child",
                               "link_sell": "tr:not(:first-child) td:nth-child(4)",
                               "link_buy": "tr:not(:first-child) td:nth-child(3)"}
            enter_bank(
                "https://www.mbank.com.ua/content/view/41/51/150/0/lang,uk/waHiddenStatus_Filter_frontGridForm_wa_rate_currency_ident,3/",
                "EUR", [], link_dictionary, file_meta)
        except:
            print("Something went wrong with the website, so we use the downloaded data")
    while True:
        print("What do you want to see: ")
        print("1 - data of Privat bank (no forecast)")
        print("2 - data of Meta bank (no forecast)")
        print("3 - data of Privat bank with forecast")
        print("4 - data of Meta bank with forecast")
        print("To stop it print something else")
        predict_days = 0

        try:
            n = int(input())
        except:
            return

        if n in [1, 2, 3, 4]:
            date_format = "%d-%m-%Y"
            while True:
                start_date = input("Period start (as DD-MM-YYYY): ")
                end_date = input("Period end (as DD-MM-YYYY): ")
                try:
                    datetime_object_start = datetime.strptime(start_date, date_format)
                    datetime_object_end = datetime.strptime(end_date, date_format)
                    if datetime_object_start == datetime_object_end:
                        print("It is the same dates")
                        continue
                    break
                except:
                    print("You should use the 'DD-MM-YYYY' format")
                    continue


            if datetime.strptime(start_date, "%d-%m-%Y") > datetime.strptime(end_date, "%d-%m-%Y"):
                start_date, end_date = end_date, start_date

            if n in [3, 4]:
                while True:
                    try:
                        predict_days = int(input("Enter count of predict days: "))
                        break
                    except:
                        print("You should enter integer")


        try:
            if n == 1 or n == 3:
                bank_graph(start_date, end_date, file_privat, predict_days)
            elif n == 2 or n == 4:
                bank_graph(start_date, end_date, file_meta, predict_days)
            else:
                return
        except:
            print("There is no data in file! Try to update it next time!")

        print("---------------------------------------------------")
        print("Your graph is ready")
        print("---------------------------------------------------")


menu()
driver.close()