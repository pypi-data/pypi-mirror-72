# pycorona
pycovid is a library that is used to get coronavirus condition (i.e. active cases, deaths, etc) of any country.

# Usage
```python
from pycorona import Country
    
country = Country("USA")
cases = country.total_cases()
print(cases)
> 2,234,475
```

Attributes for countries -
```python
continent()
flag()
total_cases()
today_cases()
total_deaths()
today_deaths()
recovered()
critical_cases()
active_cases()
tests()
```
The package raises KeyError if the given country is not found

```python
from pycorona import World

world = World()
cases = world.total_cases()
print(cases)
> 8,486,923
```

Attributes for world -
```python
affected_countries()
total_cases()
today_cases()
total_deaths()
today_deaths()
recovered()
active_cases()
tests()
critical_cases()
```

Note - This package is currently under development