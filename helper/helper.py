import logging 
import os 
import shutil
from getpass import getpass


class Helper:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.welcome_msg = 'Welcome to MainApp Bot.'
        self.main_selection = ''
        self.move_selection = ''
    
    def greeting(self):  
        print(f'\n{self.welcome_msg.center(shutil.get_terminal_size().columns)}')
        line = '-' * len(self.welcome_msg)
        print(f'{line.center(shutil.get_terminal_size().columns)}')
    
    def get_credentials(self):
        self.username = str(input("Username: "))
        self.password = getpass("Password: ")
        return self.username, self.password
    
    def get_decision(self):
        print()
        print("What action you wanna take?")
        print("[A]ssign Item")
        print("[R]elease Item")
        print("[E]nroll Item")
        print("[M]ove Item")
        self.main_selection = str(input("Your Input: ")).upper()
    
    def validate_main_selection(self):
        valid_chars = ['A', 'R', 'E', 'M']
        while len(self.main_selection) > 1 or self.main_selection not in valid_chars:
            print("ERROR: Please provide a valid input such as A, R, E, M")
            self.main_selection = str(input("Your Input: ")).upper()
        return self.main_selection
    def second_decision(self):
        print()
        print("What's the item destination?")
        print("[S7B]ite - Production B")
        print("[S7A]ite - Production A")
        print("[S6A]ite - Production A")
        print("[G]TI Stock")
        print("[L]aptops")
        print("[H]ome")
        self.move_selection = str(input("Your Input: ")).upper()
        valid_chars = ['S7B', 'S7A', 'S6A', 'G', 'L', 'H']
        while self.move_selection not in valid_chars:
            print("ERROR: Please provide a valid input such as S7A, S7B, S6A, G, L, H")
            self.move_selection = str(input("Your Input: ")).upper()
        return self.move_selection

    def initialize_logging(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '..\Logs\operations.log')
        if os.path.isfile(filename):
            os.remove(filename)
        logging.basicConfig(
            filename = filename,
            format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level = logging.INFO
        )

    def processing(self):
        print("\nWorking on it, go get a cup of tea until I finish your work.")
    
    def closure(self):
        author = "Developed by Taha Adel @ GTI Alexandria."
        line = "-" * int((len(author) / 2))
        print(f"\n{author.center(shutil.get_terminal_size().columns)}")
        print(f"{line.center(shutil.get_terminal_size().columns)}")