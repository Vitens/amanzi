from typing import Any
import pandas as pd
from pathlib import Path

# sentinel object to indicate that a key figure was not found in the database
_sentinel = object()
# key-figure database
class Database:
  def __init__(self, database_file=None):

    if not database_file:
      database_file = Path(__file__).parent.parent / 'database' / 'key_figures.csv'
    
    # get path relative to the package
    self.db = pd.read_csv(database_file, sep=';', keep_default_na=False)
    self.overwrites = {}
  
  def __getattr__(self, name: str) -> Any:
    try: 
      return self.get(name)
    except:
      return super().__getattribute__(name)
  
  def get(self, key, default=_sentinel):
    if key in self.overwrites:
      return float(self.overwrites[key])

    row = self.db[self.db['name'] == key]

    if not row.empty:
      return float(row['default'].values[0])
    elif default is not _sentinel:
      return default
    else:
      raise KeyError(f'Key figure {key} not found in database')

  
  # overwrite key figures for the whole project
  def overwrite(self, key_figures):
    for key, value in key_figures.items():
      self.db.loc[self.db['name'] == key, 'default'] = value

  @property
  def rows(self):
    return self.db.values.tolist()