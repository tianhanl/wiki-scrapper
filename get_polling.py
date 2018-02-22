import sys
# This filed is created to allow get polling data and save them using command line
# Usage: python3 get_polling.py "query"

if __name__ == '__main__':
    from sys import argv
    import wiki
    import re
    if len(argv) < 2:
        print('usage: python3 get_polling "query"')
    else:
        query = argv[1]
        url_pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        # check is query a link
        if re.search(url_pattern, query, re.IGNORECASE) is not None:
            # if query is a link, directly use the link to get page content
            polling_tables = wiki.get_poll_tables(
                wiki.get_page_html_from_url(query))
            wiki.save_tables(polling_tables,
                             'polling_data' + '.json')
        else:
            polling_tables = wiki.get_poll_tables(wiki.get_page_html(query))
            wiki.save_tables(polling_tables,
                             query.lower().replace(' ', '_') + '.json')
