# modelldcatnotordf

![Tests](https://github.com/Informasjonsforvaltning/modelldcatnotordf/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/Informasjonsforvaltning/modelldcatnotordf/branch/master/graph/badge.svg)](https://codecov.io/gh/Informasjonsforvaltning/modelldcatnotordf)
[![PyPI](https://img.shields.io/pypi/v/modelldcatnotordf.svg)](https://pypi.org/project/modelldcatnotordf/)
[![Read the Docs](https://readthedocs.org/projects/modelldcatnotordf/badge/)](https://modelldcatnotordf.readthedocs.io/)


A small Python library for mapping a modell catalog to rdf

The library contains helper classes for the following dcat classes:
 - [Catalog](https://www.w3.org/TR/vocab-dcat-2/#Class:Catalog)
 - [Dataset](https://www.w3.org/TR/vocab-dcat-2/#Class:Dataset)
 - [Distribution](https://www.w3.org/TR/vocab-dcat-2/#Class:Distribution)
 - [Data Service](https://www.w3.org/TR/vocab-dcat-2/#Class:Data_Service)

 Other relevant classes are also supported, such as:
 - Contact [vcard:Kind](https://www.w3.org/TR/2014/NOTE-vcard-rdf-20140522/#d4e1819)

 The library will map to [the Norwegian Application Profile](https://informasjonsforvaltning.github.io/modelldcat-ap-no/).

## Usage
### Install
```
% pip install modelldcatnotordf
```
### Getting started
```
from datacatalogtordf import Catalog
from modelldcatnotordf import InformationModel

# Create catalog object
catalog = Catalog()
catalog.identifier = "http://example.com/catalogs/1"
catalog.title = {"en": "A model catalog"}
catalog.publisher = "https://example.com/publishers/1"

# Create a model:
model = InformationModel()
model.identifier = "http://example.com/models/1"
model.description = {"nb": "En adressemodell"}
# ... and further attributes ...
#
# Add model to catalog:
catalog.model.append(model)

# get rdf representation in turtle (default)
rdf = catalog.to_rdf()
print(rdf.decode())
```
## Development
### Requirements
- python3
- [pyenv](https://github.com/pyenv/pyenv)
- [pipx] (https://github.com/pipxproject/pipx)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)

```
% pipx install poetry==1.0.5
% pipx install nox==2019.11.9
```
### Install
```
% git clone https://github.com/Informasjonsforvaltning/modelldcatnotordf.git
% cd modelldcatnotordf
% pyenv install 3.8.6
% pyenv install 3.7.9
% pyenv local 3.8.6 3.7.9
% poetry install
```
### Run all sessions
```
% nox
```
### Run all tests with coverage reporting
```
% nox -rs tests
```
### Debugging
You can enter into [Pdb](https://docs.python.org/3/library/pdb.html) by passing `--pdb` to pytest:
```
nox -rs tests -- --pdb
```
You can set breakpoints directly in code by using the function `breakpoint()`.
