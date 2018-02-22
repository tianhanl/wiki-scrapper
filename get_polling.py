import sys
# This filed is created to allow get polling data and save them using command line
# Usage: python3 get_polling.py "query"

if __name__ == '__main__':
    from sys import argv
    import wiki
    if len(argv) < 2:
        print('usage: python3 get_polling "query"')
    else:
        query = argv[1]
        polling_tables = wiki.get_poll_tables(wiki.get_page_html(query))
        wiki.save_tables(polling_tables,
                         query.lower().replace(' ', '_') + '.json')
