import wikipedia
from bs4 import BeautifulSoup

wikipedia.set_lang('en')


def get_page_html(query):
    # Since there may be multiple items linked with a query
    # Let wikipedia suggest one for us
    return wikipedia.page(wikipedia.search(query)[0]).html()


def parse_table(table):
    # get all the keys
    keys = list(map(lambda x: x.text.replace('\n', ''), table.find_all('th')))

    # If no keys contain poll, assume the table is not related with polling data
    # if not any('poll' in key for key in keys):
    #     return []

    result = []
    for row in table.find_all('tr'):
        cells = row.find_all('td')

        # If the number of columns is smaller than the number of cells
        # The table may be broken
        if len(keys) < len(cells):
            return []

        curr_result = {}
        for index, cell in enumerate(cells):
            curr_result[keys[index]] = cell.text.replace('\n', '')
        if len(curr_result) != 0:
            result.append(curr_result)
    return result


def get_poll_tables(html_raw):
    # Specify parser to avoid warning
    bs_obj = BeautifulSoup(html_raw, "html.parser")
    tables = bs_obj.find_all('table', {'class': 'wikitable'})
    tables = list(map(lambda x: parse_table(x), tables))
    tables = list(filter(lambda x:len(x ), tables))
    return tables
