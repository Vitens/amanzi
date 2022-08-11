# Amanzi

Amanzi is the back-end processor for SLIMM Designer files. It takes a `project.slm` as input and calculates each scenario.
## Installation

Clone and install this repository

```bash
git clone https://github.com/Vitens/amanzi

python setup.py install
```

## Usage
### print summary
```
python main.py
```
### or

```python
from amanzi.core import Project

# initialize project
project = Project("input/ProjectC.slm")

# returns scenarios
project.scenarios
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Apache Licence 2.0](https://choosealicense.com/licenses/apache-2.0/)
