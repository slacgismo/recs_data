Residential Energy Consumption Survey data access

This package downloads and organizes access to the EIA RECS database.

# Examples

## Housing Characteristics

The following example illustrates accessing the HC tables. These are based on the following context:

~~~
>>> import eia_recs
>>> hc = HousingCharacteristics(table="1.1")
~~~

### Example 1: Getting all the top-level keys

~~~
>>> hc.find('data')
[['total', 'fuel-used', 'electric-end-use', 'natural-gas-end-use', 'wood-end-use', 'fuel-oil-end-use'], ['total', 'unit-type']]
~~~

### Example 2: Getting a single top-level value

~~~
>>> hc.find('data',['total'],['total'])
118.2e6
~~~

### Example 3: Getting a single sub-level value

~~~
>>> hc.find('data',['total'],['unit-type','single-family-detached'])
>>> 73.9e6
~~~

### Example 4: Getting the available keys

~~~
>>> hc.find('data',['electric-end-use','space-heating'],['total']),
>>> [['total', 'main', 'secondary'], 'B']
~~~

## Microdata

The following example illustrates accessing the microdata. These are based on the following context:

~~~
>>> import eia_recs
>>> md = Microdata()
~~~

### Example 4: Getting a single value

~~~
>>> md["LPXBTU"][0]
>>> 91.33
~~~
