
# This repository stores an extensive guide for using data objects in Syncano with Python Library


## Preface

You want to build an app. This app is going to store information about restaurant in your town. Later in your country 
 and later in the entire world. You're a genius who want to revolution the table reservation process.  

And you're using Syncano.

## App core functionality

* user can search restaurant by geo location;
* user can search restaurant by empty tables in there;
* user can search restaurant by tags (which can describe a menu or some special abilities like: "kid friendly");
* user can make a reservation for the table; 

## Create all needed models

Firstly you will need some classes definition - based on that you will be storing your data.
 
To make things simple - you want to release MVP first - you defined following schemas:

```python
item_schema = [
    {"name": "name", "type": "string", "filter_index": True},
    {"name": "description", "type": "string"},
    {"name": "price", "type": "integer"},
    {"name": "header_picture", "type": "file"},
    {"name": "body_picture", "type": "file"},
]

menu_schema = [
    {"name": "name", "type": "string"},
    {"name": "items", "type": "relation", "target": "item"},
    {"name": "start_date", "type": "datetime", "filter_index": True},
    {"name": "end_date", "type": "datetime", "filter_index": True},
]

reservation_schema = [
    {"name": "date", "type": "datetime"},
    {"name": "user_identifier", "type": "string"},
]

table_schema = [
    {"name": "identifier", "type": "string"},
    {"name": "person_count", "type": "integer", "filter_index": True},
    {"name": "by_window", "type": "boolean", "filter_index": True},
    {"name": "reserved", "type": "boolean", "filter_index": True},
    {"name": "reservations", "type": "relation", "target": "reservation"},
]

tag_schema = [
    {"name": "name", "type": "string"},
    {"name": "description", "type": "string"},
]

restaurant_schema = [
    {"name": "name", "type": "string", "filter_index": True},
    {"name": "location", "type": "geopoint", "filter_index": True},
    {"name": "phone_number", "type": "string"},
    {"name": "menus", "type": "relation", "target": "menu"},
    {"name": "tables", "type": "relation", "target": "table"},
    {"name": "tags", "type": "relation", "target": "tag"},
]
```

You created the filter_index attribute for all the fields that are expected to be searchable.

Now create a class in Syncano

```python
import syncano
from syncano.models import Class, GeoPoint, Object

INSTANCE_NAME = 'INTANCE_NAME'  # provide an instance name here
API_KEY = 'API_KEY'  # provide an admin api_key here

connection = syncano.connect(
    api_key=API_KEY,
    instance_name=INSTANCE_NAME,
)

item_class = Class.objects.create(
    name='item',
    schema=item_schema,
)

```

Use the following pattern for rest of the classes - this can be found in `init_data.py` script. If you provide 
connection data, run: `python init_data.py` to create all needed structures (running the script again will move you to 
the starting point - will clear all the later provided data). The script will also creates sample data objects for you

```python

# you can use following syntax

pasta = item_class.objects.create(
    name="Carbonara", 
    description="Pasta with bacon and eggs", 
    price=35
)

# or:

pasta = Object.please.create(
    class_name='item', 
    name="Carbonara", 
    description="Pasta with bacon and eggs", 
    price=35
)
```

It would be nice to know what objects we have initially, so run following code:

```python

# this are available class names
ITEM = 'item'
MENU = 'menu'
RESERVATION = 'reservation'
TABLE = 'table'
TAG = 'tag'
RESTAURANT = 'restaurant'

# query about tags:

for tag in Object.please.list(class_name=TAG):
    print(tag.name)
    
# query about restaurants:

for restaurant in Object.please.list(class_name='restaurant'):
    print(restaurant.name, restaurant.location)

```

### Query on geopoint field

```python
restaurants = Object.please.list(class_name='restaurant').filter(
    location__near=(
        GeoPoint(52.2297, 21.0122),
        Distance(kilometers=0.1)
    )
)

# or (if restauratn class is present)

restaurant_class = Class.please.get(name='restaurant')
restaurants = restaurant_class.objects.filter(
    location__near=(
        GeoPoint(52.2297, 21.0122),
        Distance(kilometers=0.1)
    )
)

```

Such query will find all restaurants which are 0.1 kilometers from point: latitude = 52.2297, longitdue = 21.0122.
 
You can also specify the miles there - if you prefer:
 
```python
restaurant_class = Class.please.get(name='restaurant')
restaurants = restaurant_class.objects.filter(
    location__near=(
        GeoPoint(52.2297, 21.0122),
        Distance(miles=0.1)
    )
)
```

### Query on relation field

### Query on datetime field

### Query on string fields

### Query on multiples fields

### Query on related tags

### Handle the files

### Add objects to relations

### Remove objects from relations

### Made a table reservation
