import time
from sbol2 import *

igem = PartShop('https://synbiohub.org/public/igem')
records = []
search_term = 'plasmid'
limit = 25
total_hits = igem.searchCount(search_term)
for offset in range(0, total_hits, limit):
    records.extend( igem.search(search_term, SBOL_COMPONENT_DEFINITION, offset, limit) )
    time.sleep(0.1)
