"""
Webscrapes the RIT Dining website
"""

from bs4 import BeautifulSoup
import requests

MENU_URL = 'https://www.rit.edu/fa/diningservices/daily-specials'
GEN_MENU_URL = 'https://www.rit.edu/fa/diningservices/general-menus'

# # Each location has an unique ID that is used as the 'id' attribute of their
# # HTML div. This is hardcoded, but another possible way would be to find
# # the children of html_content.
# LOCATION_IDS = {"103", "104", "105", "107"}

def get_menus(menu_url):
    """
    Get menu for a location
    
    Parameters:
    location_id -- the id of the location to get
    menu_url -- url of menu to webscrape
    """

    page = requests.get(menu_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    html_content = soup.find('div', class_='ds-output')

    for children in html_content.findAll('div', recursive=False)[1:]:

    # # Div that contains all the content for a specific location
    # html_location_block = html_content.find('div', id=location_id)

        html_location_block = children

        # VALUE: Contains the dining location name
        location_name = html_location_block.find('h3').text
        print(location_name)

        # Contains the meals and their dishes
        html_meals_list = html_location_block.find('div', class_='ds-loc-title')

        # Only display content if the location has meals to display
        if html_meals_list.contents:

            # Get the individual meals
            html_meals = html_meals_list.findChildren(recursive=False)

            for html_meal in html_meals:

                # If the meal has dishes
                if html_meal.contents:

                    html_meal_type = html_meal.find('div', class_='menu-type')
                    # VALUE: breakfast, lunch, dinner
                    menu_type = html_meal_type.text[:-4]
                    print(menu_type)

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

    page = requests.get(GEN_MENU_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    html_content = soup.find('div', class_='ds-output')

    for children in html_content.findAll('div', recursive=False)[1:]:

    # # Div that contains all the content for a specific location
    # html_location_block = html_content.find('div', id=location_id)

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


def main():
    gen_menu()

main()