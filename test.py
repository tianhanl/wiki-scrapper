import wiki

# french_polling_tables = wiki.get_poll_tables(wiki.get_page_html(
#     'opinion polling french presidential election'))

# wiki.save_tables(french_polling_tables,
#                  'opinion_polling_french_presidential_election_2017.json')

french_polling_tables = wiki.get_poll_tables(wiki.get_page_html(
    'Opinion polling united kingdom general election'))

wiki.save_tables(french_polling_tables,
                 'opinion_polling_united_kingdom_general_election_2017.json')
