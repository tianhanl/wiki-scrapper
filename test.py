import wiki

print(wiki.get_poll_tables(wiki.get_page_html(
    'opinion polling french presidential election'))[0:10])
