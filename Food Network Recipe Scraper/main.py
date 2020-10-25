import general_functions as gf
import pandas as pd
import scraper_functions as sf
import time


def main():
    gf.display_settings()
    start_time = time.time()
    # todo allow user to select how many recipes they want to look at
    search_keyword = 'beef empanadas'
    search_url, search_html = get_search_html(search_keyword)
    gf.time_checkpoint('1', start_time)
    list_of_page_urls = get_page_urls(search_keyword, search_html)
    gf.time_checkpoint('2', start_time)
    list_of_html = get_html_texts(list_of_page_urls)
    gf.time_checkpoint('3', start_time)
    recipe_df = extract_recipe_info(list_of_html)
    gf.time_checkpoint('4', start_time)
    extract_recipe_ingredients(recipe_df)
    gf.time_checkpoint('5', start_time)
    analyze_df(recipe_df)
    gf.time_checkpoint('6', start_time)
    gf.save_df_to_excel(recipe_df, f'C:/Users/Jason Minhas/Documents/food_network_web_scrape/{search_keyword}')
    gf.time_checkpoint('7', start_time)


def get_search_html(search_keyword):
    #  get html for search page
    search_url = sf.clean_search_url(search_keyword)
    search_html = sf.get_html(search_url)

    return search_url, search_html


def get_page_urls(search_keyword, search_html):
    # get list of urls using first page html
    page_urls = search_html.find_all('li', class_='o-Pagination__a-ListItem')

    max_page = 1

    for page in page_urls:
        clean_page_num = page.text.strip()
        try:
            clean_page_num = int(clean_page_num)
            if clean_page_num > max_page:
                max_page = clean_page_num
        except:
            pass

    list_of_page_urls = [sf.clean_search_url(search_keyword)]

    # create list of reciepe urls
    if max_page >= 2:
        for page_num in range(2, max_page + 1):
            clean_url = sf.clean_search_url(search_keyword, page_num=page_num)
            list_of_page_urls.append(clean_url)

    return list_of_page_urls


def get_html_texts(list_of_page_urls):
    # get html text for all page that come up in search of keyword
    list_of_html = []

    for url in list_of_page_urls:
        html = sf.get_html(url)
        list_of_html.append(html)

    return list_of_html


def extract_recipe_info(list_of_html):
    # create df of name, author and link to recipe
    recipe_df = pd.DataFrame(columns=['name', 'author', 'ingredients', 'url'])

    for html in list_of_html:
            searches_html = html.find_all('section', class_='o-RecipeResult o-ResultCard')

            for recipe in searches_html:
                recipe_name = recipe.find('a', class_='').span.text
                try:
                    recipe_author = recipe.find('span', class_='m-Info__a-AssetInfo').text.lstrip('Courtesy of ')
                except:
                    recipe_author = 'Unknown Author'
                recipe_url = f"http://{recipe.find('a', class_='')['href'].lstrip('/')}"
                recipe_df = recipe_df.append({'name': recipe_name, 'author': recipe_author, 'url': recipe_url},
                                             ignore_index=True)

    return recipe_df


def extract_recipe_ingredients(recipe_df):
    for recipe_url in recipe_df.url:
        try:
            recipe_ingredients = sf.get_ingredients_from_url(recipe_url)
        except:
            recipe_ingredients = None

        url_index = recipe_df.url[recipe_df.url == recipe_url].index[0]
        recipe_df.at[url_index, 'ingredients'] = recipe_ingredients


def analyze_df(recipe_df):
    main_ingredients_series = pd.Series(dtype=str)

    for ingredients_list in recipe_df['ingredients']:
        if ingredients_list is not None:
            ingredients_series = pd.Series(ingredients_list)
            main_ingredients_series = main_ingredients_series.append(ingredients_series, ignore_index=True)

    # todo make percentage and make another tab to put this in
    freq_table = main_ingredients_series.value_counts()

    return main_ingredients_series


if __name__ == '__main__':
    main()
