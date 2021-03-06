import wikipedia
import re
import json
import pendulum
import requests
from bs4 import BeautifulSoup
from functools import reduce
from urllib.request import urlopen

wikipedia.set_lang('en')

# This function will be used to used to retrive raw html from the given query


def get_page_html(query):
    # Since there may be multiple items linked with a query
    # Let wikipedia suggest one for us
    content = None
    try:
        content = wikipedia.page(wikipedia.search(query)[0]).html()
    except:
        print('An error has occured when getting information from your query')
    return content


def get_page_html_from_url(link):
    content = None
    content = requests.get(link).text
    return content

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
        if re.search('agency', key, re.IGNORECASE) is not None:
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
    if html_raw is not None:
        bs_obj = BeautifulSoup(html_raw, "html.parser")
        tables = bs_obj.find_all('table', {'class': 'wikitable'})
        tables = list(map(lambda x: parse_table(x), tables))
        tables = list(filter(lambda x: len(x) > 0, tables))
        if len(tables) > 1:
            tables = list(reduce((lambda x, y: x+y), tables))
        tables = list(filter(item_filter, tables))
    else:
        tables = []
    return tables


def save_to_json(dict, name):
    output = json.dumps(dict)
    f = open(name, 'w')
    f.write(output)
    f.close()
    return


def remap_tables_keys(tables, mapping):
    # Clone the original tables to avoid mutating origianl list
    tables = list(tables)

    for table in tables:
        for key in list(table.keys()):
            for mapKey in list(mapping.keys()):
                if (re.search(mapKey, key, re.IGNORECASE)):
                    table[mapping[mapKey]] = table[key]
                    del table[key]
                    break
    return tables


def save_tables(tables, name):
    result = {}
    result['polling_data'] = tables
    result['access_time'] = pendulum.now().to_iso8601_string()
    result['name'] = name
    save_to_json(result, name)


def read_tables(name):
    f = open(name)
    return json.load(f)
