from mainapp.mainapp import MainApp
from mainapp.constants import *
from selenium.common.exceptions import TimeoutException
from helper.helper import Helper 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
from sys import exit 
import os
import timeit
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait


start = timeit.default_timer()


helper = Helper()
helper.initialize_logging()
helper.greeting()
username, password = helper.get_credentials()
helper.get_decision()
selection = helper.validate_main_selection()
destination = helper.second_decision()

with MainApp(headless=True) as bot:
    bot.land_first_page()
    try:
        bot.sign_in(username, password)
        WebDriverWait(bot, TIMEOUT).until(
            EC.presence_of_element_located(
                (By.ID, 'collapseExample')
            )
        )
    except TimeoutException:
        print("\nERROR: Wrong username or password.")
        helper.closure()
        exit()
    helper.processing()
    if selection == "A":
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'data/assignment.csv')
        with open(file=filename, mode="r") as assignment_data:
            assignment_data_reader = csv.DictReader(assignment_data)
            all_assets = []
            for i in list(assignment_data_reader):
                current_row = []
                current_row = [
                    i['PC ST'],
                    i['Monitor ST 1'],
                    i['Monitor ST 2']
                ]
                for cell in current_row:
                    if cell:
                        if bot.isexist(cell, selection):
                            try:
                                bot.select_asset(cell)
                            except TimeoutException:
                                continue
                            if bot.isassigned(cell):
                                all_assets.append(cell)
                                continue
                            else:
                                try:
                                    bot.assign(cell, i['Employee ID'])
                                    all_assets.append(cell)
                                except TimeoutException:
                                    bot.main_logger.warning(f"{i['Employee ID']} is not exist.")
                                    continue 
                        else:
                            continue
    
            bot.load_movement_page()
            for asset in all_assets:
                if bot.isexist(asset, selection):
                    try:
                        bot.move(asset, destination)
                    except TimeoutException:
                        bot.main_logger.warning(f"Can't move {asset} due to timeout.")
                        continue
                else:
                    continue

    elif selection == "R":
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'data/release.csv')
        with open(file=filename, mode="r") as release_data:
            release_data_reader = csv.DictReader(release_data)
            all_assets = []
            for j in list(release_data_reader):
                try:
                    if bot.isexist(j["Serial Number"], selection):
                        try:
                            bot.select_asset(j["Serial Number"])
                        except TimeoutException:
                            continue
                        if bot.isassigned(j["Serial Number"]):
                            try:
                                bot.release(j["Serial Number"])
                                all_assets.append(j["Serial Number"])
                            except TimeoutException:
                                bot.main_logger.warning(f"Can't release {j['Serial Number']} due to timeout.")
                        else:
                            bot.main_logger.info(f"{j['Serial Number']} is already free.")
                            all_assets.append(j["Serial Number"])
                    else:
                        continue
                except UnexpectedAlertPresentException:
                    continue
        
        bot.load_movement_page()
        for asset in all_assets:
            if bot.isexist(asset, selection):
                try:
                    bot.move(asset, destination)
                except TimeoutException:
                    bot.main_logger.warning(f"Can't move {asset} due to timeout.")
            else:
                continue

    elif selection == "E":
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'data/enrollment.csv')
        with open(file=filename, mode="r") as enrollment_data:
            enrollment_data_reader = csv.DictReader(enrollment_data)
            all_assets = []
            for a in list(enrollment_data_reader):
                if not bot.isexist(a["Serial Number"], selection):
                    to_be_registered_asset = {
                        "Serial Number": a["Serial Number"],
                        "Asset TAG": a["Asset TAG"],
                        "PO Number": a["PO Number"],
                        "Manufacturer": a["Manufacturer"],
                        "Model": a["Model"],
                        "Destination": destination
                    }
                    all_assets.append(to_be_registered_asset)
                else:
                    continue
            bot.load_register_page()
            for k in all_assets:
                try:
                    bot.enroll(
                        serial_number = k["Serial Number"],
                        asset_tag = k["Asset TAG"],
                        po_number = k["PO Number"],
                        manfacturer = k["Manufacturer"],
                        model = k["Model"],
                        destination = destination
                    )
                except TimeoutException:
                    bot.main_logger.warning(f"Can't register {k['Serial Number']} due to timeout.")

    elif selection == "M":
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'data/movement.csv')
        with open(file=filename, mode="r") as movement_data:
            movement_data_reader = csv.DictReader(movement_data)
            bot.load_movement_page()
            for L in list(movement_data_reader):
                if bot.isexist(L["Serial Number"], selection):
                    try:
                        bot.move(L["Serial Number"], destination)
                    except TimeoutException:
                        bot.main_logger.warning(f"Can't move {L['Serial Number']} due to timeout.")
                        continue
                else:
                    continue
    stop = timeit.default_timer()
    exec_time = stop - start
    print("It's Done. Check out the logs for further detailed information.")
    print("The bot took {:.2f} seconds to execute".format(float(exec_time)))
    helper.closure()




