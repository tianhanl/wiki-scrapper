import wikipedia
import re
from bs4 import BeautifulSoup
from functools import reduce

wikipedia.set_lang('en')

# This function will be used to used to retrive raw html from the given query


def get_page_html(query):
    # Since there may be multiple items linked with a query
    # Let wikipedia suggest one for us
    return wikipedia.page(wikipedia.search(query)[0]).html()

# This function will be used to clean the text values


def clean_text(text):
    result = re.sub('\n+', ' ', text)
    result = re.sub(' +', ' ', result)
    result = bytes(result, 'UTF-8')
    result = result.decode('ascii', 'ignore')
    result = result.strip()
    return result


# This function will try to extract each row in the table as a dictionary
def parse_table(table):
    # get all the keys
    keys = list(map(lambda x: x.text.replace(
        '\n', '').strip(), table.find_all('th')))
    keys = list(filter(lambda x: len(x.strip()), keys))
    result = []

    flag = False
    for key in keys[0:3]:
        if re.search('poll', key, re.IGNORECASE) is not None:
            flag = True
    # If no keys contain poll, assume the table is not related with polling data
    # if not any('poll' in key for key in keys):
    #     return []
    if not flag:
        return result

    for row in table.find_all('tr'):
        cells = row.find_all('td')

        # If the number of columns is smaller than the number of cells
        # The table may be broken
        if len(keys) < len(cells):
            return []

        curr_result = {}
        for index, cell in enumerate(cells):
            curr_result[keys[index]] = clean_text(cell.text)
        if len(curr_result) != 0:
            result.append(curr_result)
    return result


# This function will be used to filter invalid table in the final results

def item_filter(item):
    if(len(item) < 3):
        return False
    else:
        return True

# This funciton will try to extract tables from the given html


def get_poll_tables(html_raw):
    # Specify parser to avoid warning
    bs_obj = BeautifulSoup(html_raw, "html.parser")
    tables = bs_obj.find_all('table', {'class': 'wikitable'})
    tables = list(map(lambda x: parse_table(x), tables))
    tables = list(filter(lambda x: len(x) > 0, tables))
    tables = list(reduce((lambda x, y: x+y), tables))
    tables = list(filter(item_filter, tables))
    return tables
