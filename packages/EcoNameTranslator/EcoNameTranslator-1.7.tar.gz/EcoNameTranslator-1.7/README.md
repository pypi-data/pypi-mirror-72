# The Ecological Name Translator

### What is it?

A lightweight python package for:

- Translating ecological names in any format [e.g. at the species level (e.g. "Panthera tigris"), higher levels of taxonomy (such as genus, or family), or common name ("Tiger")] to the standardised species name equivalent.
- Translating scientific names at any taxonomic level to the English common name equivalent

### Input & Output

##### The EcoNameTranslator (any name -> scientific name)

A list of names describing species is accepted as input. This undergoes a data-cleaning procedure, after which, the following actions are taken:

- Names that are already in a standard species format (that is, genus + species extension), have any spelling errors corrected

- Names at higher levels of taxonomy (currently family, sub-family and genus are supported) again have any spelling mistakes corrected, and are then mapped to a list of specific species belonging to that taxonomic rank

- Common names (currently, English only) are mapped to their scientific name (or all scientific names that could be described by the common English name)

The output is a python dictionary which maps each item in the input list to the equivalent standard scientific name(s).

##### The ReverseTranslator (scientific name -> common English name)

A list of names describing species is accepted as input. This undergoes a data-cleaning procedure, after which, the following actions are taken:

- Input Scientific names have any spelling errors corrected

- Names at higher levels of taxonomy are then mapped to a list of specific species belonging to that taxonomic rank

- These scientific names are mapped to a list of possible common English names that describe the scientific name

The output is a python dictionary which maps each scientific name in the input list to the equivalent common English name(s).

### Examples

##### Already a scientific name at the species level

If correct, the name will be returned as is, and if there are any spelling mistakes, they will be corrected.

```python
from EcoNameTranslator import EcoNameTranslator
unstandardised_names = ['Panhera tigris'] #Should be "Panthera tigris"       
translator = EcoNameTranslator()   
index = translator.translate(unstandardised_names)
print(index)
# {'Panera tigris':['panthera tigris']}    
```

##### Higher levels of taxonomy

If an entry in your list is at a higher taxonomic rank, all species under that rank will be returned

```python
from EcoNameTranslator import EcoNameTranslator
unstandardised_names = ['Panthera'] # A genus of various big cats       
translator = EcoNameTranslator()   
index = translator.translate(unstandardised_names)
print(index)
# {'Panthera': ['panthera leo', 'panthera uncia', 'panthera tigris', 'panthera onca', 'panthera pardus','panthera spec']}    
```

##### Common names

A common name can also be provided, in which case all possible scientific names described by the common name are returned. Be careful; quite generic common names, e.g. "monkey", can return hundreds of species!

```python
from EcoNameTranslator import EcoNameTranslator
unstandardised_names = ['Bengal Tiger']
translator = EcoNameTranslator()   
index = translator.translate(unstandardised_names)
print(index)
# {'Bengal Tiger': ['panthera tigris']}    
```

Note: this feature should be used with caution, as partial matching is included- that is, a list item of just "Tiger" would also bring unwanted results of things like a Tiger Beetle.

##### Reverse Translation

```python
from EcoNameTranslator import ReverseTranslator
unstandardised_names = ["vulpes vulpes",'ursus']
translator = ReverseTranslator()   
index = translator.translate(unstandardised_names)
print(index)
# {
#   'vulpes vulpes': ['Red Fox','Renard Roux'],
#   'ursus': ['Asiatic Black Bear', 'Mexican Grizzly Bear', 'American Black Bear', ...]
# }    
```

##### Saving

Two convenience functions are provided to save the returned python data structure to file. Simple call one of:

```python
from EcoNameTranslator import EcoNameTranslator
items = [...]
index = translator.translate(items)
translator.toPickleFile('C:/Users/...','filename') # Python serialization
translator.toCSV('C:/Users/...','filename') # CSV 
```

### Why did we build it?

This package was refactored as part of a larger species interaction networks project. Our project required large datasets of standardised, scientific species names; and while there is plenty of species data, the existing datasets are often incredibly messy and constructed ad-hoc- meaning assembling a standard collection of species is difficult. To help, we made this package that takes in ecological names in any format, and makes a best-effort attempt to translate the input to a standardised set of scientific names. 

### Known issues

Currently, calls to APIs are made asynchronously with grequests. This library has a known issue when used in conjunction with the requests library; if you do need the requests library along the EcoNameTranslator, make sure to import requests after EcoNameTranslator:

```python
from EcoNameTranslator import EcoNameTranslator
import requests
...  
```

### Detailed Docs + Contributing

See the Github page for both, [here](https://github.com/Daniel-Davies/MedeinaTranslator)

### Credit 

The package uses various APIs for conversions of names. These are:

- [The Global Names Resolver](https://resolver.globalnames.org/)
- [The Integrated Taxonomic Information System](https://www.itis.gov/)
- [The Global Biodiversity Information Facility](https://www.gbif.org/)
