from bs4 import BeautifulSoup
import re
import requests


def clean_search_url(search_keyword, page_num=None):
    # lower case everything and replace space with '-' and then add '-' at the end
    search_keyword = search_keyword.lower()
    search_keyword = search_keyword.strip()
    search_keyword = search_keyword.replace(" ", "-")
    search_keyword = search_keyword + '-'

    if page_num is None:
        search_url = f'https://www.foodnetwork.com/search/{search_keyword}/CUSTOM_FACET:RECIPE_FACET'
    else:
        search_url = f'https://www.foodnetwork.com/search/{search_keyword}/p/{page_num}/CUSTOM_FACET:RECIPE_FACET'

    return search_url


def get_html(url):
    source = requests.get(url).text
    html_text = BeautifulSoup(source, 'lxml')

    return html_text


def get_ingredients_from_url(recipe_url):
    # todo attach each recipe to a list of ingredient
    recipe_html = get_html(recipe_url)
    recipe_ingredients = recipe_html.find_all('span', class_='o-Ingredients__a-Ingredient--CheckboxLabel')

    list_of_ingredients = []

    for html_ingredients in recipe_ingredients:
        ingredient = html_ingredients.text.lower()
        ingredient = ingredient.replace('\xa0', ' ')
        regex_list = [r'\s*\(.*\)', r'\s*\d/\d\s', r'^[0-9]*', r'\,.*$']
        for regex in regex_list:
            ingredient = re.sub(regex, '', ingredient)

        list_of_measurements = ['cup', 'cups', 'teaspoon', 'teaspoons', 'tablespoon', 'tablespoons',
                                'large', 'medium', 'small', 'inch', 'pound', 'pounds', 'ounce', 'ounces',
                                'bunch', 'slice', 'slices', 'package', 'can', 'cans', 'whole', 'piece',
                                'frozen', 'melted', 'refrigerated', 'uncooked', 'gram', 'grams']
        for measurement in list_of_measurements:
            regex = rf'^(.*{measurement}\s)'
            ingredient = re.sub(regex, '', ingredient)
        ingredient = ingredient.strip()

        list_of_ingredients.append(ingredient)

    list_of_ingredients.remove('deselect all')

    return list_of_ingredients
