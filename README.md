# Main App Bot 

MainApp is a web based inventory application to keep track all the company's assets such as Computers and Screens that are used in production by the company's employees. 
The MainApp bot is written in Python and driven by selenium library to automate the four main tasks of MainApp application. 

# What the bot can do?

## Assignmnet 

The bot can assin assets to employees by providing it the required inputs such as Emp ID and the asset serial number. 
it can handle the following scenarios:

* The asset serial number doesn't exist in the system.
* The employee id doesn't exist in the system.
* The username and password of the admin that should interact with the system is not correct.
* There are successive entries that doesn't exist in the system.
* In mainapp system, the PRIMARY KEY is the asset TAG, not the serial number of the asset. But, we use the serial number when we search for asset and assign it to the employees. So, in some cases we get multiple entries for specific serial number. In this case, the bot will leave this particular asset to the admin for investigation.

After assigning the asset to the respective employee, the asset should be moved to the Work at Home section. The bot will ask the admin to choose where it should move the asset to when it finishs the assignment of the asset. So, the bot can do the assignment and the movement in one shot.

## Release

The bot can release an item from the employee by providing it the serial number of the asset. After releaseing the asset, it should be moved to location in the site to keep track of the assets location. The bot will ask the admin to choose where it should move the asset to after finishing the release movement. Just like the assignment feature, the bot can do the release and the movement in one shot.

## Movement

This feature is made in case if we need just to move a batch of assets from section to section in the system without assigning or releasing it.

## Register

When we have new computers and monitors in our stock, we should register should assets in the system's database to assign them th employee's in the future. The bot can take a batch of serial numbers associated to the assets to be registered and register them in the background automatically instead of the manual method that may cause human errors. The bot will do the following to register asset:

* It will search for the asset via its serial number.
* If the serial number is found in the database associated with any asset TAG, it won't register it.
* If, the serial number is not found in the database, it will register it via the asset TAG entered by the admin.

# How to use the bot?

## Downloading the bot

* Download the bot files from the release section of this repo.
* Extract the bot folder from the downloaded zip file.
* Move the bot folder to "C:".
* Download [Microsoft Edge Webdriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) - Chose the version that match your Edge browser version.
* Make a new folder "C:SeleniumDrivers" and move the downloaded driver to it.

## Using the bot

* As discussed before, the bot needs some input data to function properly. 
* Every function in the bot is associated with CSV template found in `data/` directory in the bot main directory. 
* So, to use the bot for assigning some assets, the admin should fill the `data/assignment.csv` template with the required data. 
* After the bot finish, it will populate `logs/operations.log` files with the execution logs. 
* In `logs/operations.log`, the admin can see what succeed and what failed during the bot execution.
* The admin can run the bot via cmd either by opening CMD terminal in the bot directory and run `pyapp.exe` or by adding the bot directory to the `PATH` environment variable and run it from anywhere. 

