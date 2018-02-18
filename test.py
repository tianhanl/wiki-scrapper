import wiki

# french_polling_tables = wiki.get_poll_tables(wiki.get_page_html(
#     'opinion polling french presidential election'))

# wiki.save_tables(french_polling_tables,
#                  'opinion_polling_french_presidential_election_2017.json')

# french_polling_tables = wiki.get_poll_tables(wiki.get_page_html(
#     'Opinion polling united kingdom general election'))

# wiki.save_tables(french_polling_tables,
#                  'opinion_polling_united_kingdom_general_election_2017.json')

uk_candidates = ['Theresa May', 'Jeremy Corbyn',
                 'Nicola Sturgeon', 'Tim Farron', 'Arlene Foster', 'Gerry Adams', 'Leanne Wood', 'Jonathan Bartley Caroline Lucas', 'John Bercow', 'Sylvia Hermon']
fr_candidates = ['Nicolas Dupont-Aignan', 'Marine Le Pen',
                 'Emmanuel Macron', 'Benoît Hamon', 'Nathalie Arthaud', 'Philippe Poutou', 'Jacques Cheminade', 'Jean Lassalle', 'Jean-Luc Mélenchon', 'François Asselineau', 'François Fillon']

tables = wiki.read_tables(
    './opinion_polling_french_presidential_election_2017.json')['polling_data']
mappingFr = {
    'macron': 'Emmanuel Macron',
    'le pen': 'Marine Le Pen',
    'dupont-Aignan': 'Nicolas Dupont-Aignan',
    'hamon': 'Benoît Hamon',
    'arthaud': 'Nathalie Arthaud',
    'poutou': 'Philippe Poutou',
    'cheminade': 'Jacques Cheminade',
    'lassalle': 'Jean Lassalle',
    'mélenchon': 'Jean-Luc Mélenchon',
    'asselineau': 'François Asselineau',
    'fillon': 'François Fillon'
}
tables = wiki.remap_tables_keys(tables, mappingFr)

wiki.save_tables(tables, 'cleaned_frech_presidential_election_polling.json')
