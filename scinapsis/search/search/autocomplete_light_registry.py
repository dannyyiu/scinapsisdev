import autocomplete_light
from search.models import PubProductName

class ProductAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['name1']
autocomplete_light.register(PubProductName, ProductAutocomplete)