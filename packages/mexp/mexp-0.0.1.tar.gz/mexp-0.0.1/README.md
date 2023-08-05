*You can use mexp to help in filtering a list of objects using find and find_any of elements that mactch properties conditions*

**Exemple:**

file `test_mexp.py`:
```
from car_class import Car
from mexp import *


if __name__ == "__main__":
    listTesti = []
    listTesti.append(Car('Jack', 'benlalla', True, 1))
    listTesti.append(Car('Jack2', 'elarrs', False, 5))
    listTesti.append(Car('Marc', 'roro', False, 2))
    result = find(listTesti, lname = 'roro')
    print(result)
```

File `car_class.py`
```
class Car(object):
    def __init__(self, name, lname, active, rank):
        self.name = name
        self.lname = lname
        self.active = active
        self.rank = rank
```


find_any(list_of_object, **kwargs)
 ```
    Args:
        list_of_object: provide a list of objects you want to filter
        kwargs: properties with values you want to use as filter
    Returns:
        A filtered list of objects that match any of the filter properties
```

def find(list_of_object, **kwargs):   
```
    Args:
        list_of_object: provide a list of objects you want to filter
        kwargs: properties with values you want to use as filter
    Returns:
        A filtered list of objects that match the filter properties
```
[**mexp repo**](https://github.com/IbrahimABBAS85/mexp)