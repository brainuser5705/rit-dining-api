"""
Webscrapes the RIT Dining website

@author Ashley Liew (brainuser5705)
"""

from bs4 import BeautifulSoup
import requests

# URLs to the dining menus
MENU_URL = 'https://www.rit.edu/fa/diningservices/daily-specials'
GEN_MENU_URL = 'https://www.rit.edu/fa/diningservices/general-menus'


def get_menus():
    """
    Get menu for a location from the general menu
    """

    # sets up the BeautifulSoup object
    page = requests.get(MENU_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    # where all the content is stored
    html_content = soup.find('div', class_='ds-output')

    # Skips the first element, which is an unecessary div
    for children in html_content.findAll('div', recursive=False)[1:]:

        html_location_block = children

        # VALUE: Contains the dining location name
        location_name = html_location_block.find('h3').text
        print(location_name)

        # Contains the meals and dishes of the location
        html_meals_list = html_location_block.find('div', class_='ds-loc-title')

        # Only display content if the location has meals to display
        if html_meals_list.contents:

            # Get the individual meals div (breakfast, lunch, dinner)
            html_meals = html_meals_list.findChildren(recursive=False)

            for html_meal in html_meals:

                # If the meal has dishes
                if html_meal.contents:

                    html_meal_type = html_meal.find('div', class_='menu-type')
                    # VALUE: breakfast, lunch, dinner
                    menu_type = html_meal_type.text[:-4]
                    print(menu_type)

                    # where the station divs are
                    stations = html_meal.findAll('div', class_='col-xs-12 col-md-6 menu-category-list')

                    for station in stations:

                        html_station = station.find('div', class_='menu-category')
                        # VALUE
                        station_name = html_station.text
                        print(station_name)

                        # VALUE
                        dishes_list = []
                        html_meal_items = station.find('div', class_='menu-items')
                        for content in html_meal_items.contents[:-1]:  # there is a new line at the end
                            if str(content) != '<br/>':
                                dishes_list.append(content)

                        print(dishes_list)

                    print("\n")

def gen_menu():
    """
    Gets menu items from the general menu
    """

    page = requests.get(GEN_MENU_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    html_content = soup.find('div', class_='ds-output')

    for children in html_content.findAll('div', recursive=False)[1:]:

        html_location_block = children

        # VALUE: Contains the dining location name
        location_name = html_location_block.find('h3').text
        print(location_name)

        # Contains the meals and their dishes
        html_meals_list = html_location_block.find('div', class_='ds-loc-title')

        # Get the individual meals
        html_meals = html_meals_list.findAll('div', class_='menu-category-list')

        for html_meal in html_meals:

            html_meal_category = html_meal.find('div', class_='menu-category')
            menu_category = html_meal_category.text
            print(menu_category)

            # VALUE
            dishes_list = []
            html_meal_items = html_meal.find('div', class_='menu-items')
            for content in html_meal_items.contents[:-1]:  # there is a new line at the end
                if str(content) != '<br/>':
                    dishes_list.append(content)

            print(dishes_list)

        print("\n")