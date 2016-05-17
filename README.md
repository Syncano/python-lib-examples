
# This repository stores an extensive guide for using data objects in Syncano with our Python Library

Please use the newest version of [Syncano LIB](https://github.com/syncano/syncano-python/) for running these examples.

# Table of Contents
1. [Preface] (#preface)
2. [App core functionality] (#app-core-functionality)
3. [Create all needed models] (#create-all-needed-models)
4. [Query on geopoint field] (#query-on-a-geopoint-field)
5. [Query on relation field] (#query-on-a-relation-field)
6. [Query on datetime field] (#query-on-a-datetime-field)
7. [Query on string fields] (#query-on-string-fields)
8. [Query on multiples fields] (#query-on-multiple-fields)
9. [Made a table reservation] (#make-a-table-reservation)
10. [Add objects to relations] (#add-objects-to-relations)
11. [Remove objects from relations] (#remove-objects-from-relations)
12. [Handle the files] (#handle-files)
13. [Contribute] (#contribute)

## Preface

You want to build an app. Your app will store information about restaurants in your home town. Later on - in your country and eventually in the entire world. You're a genius who wants to revolutionize the table reservation process.  

And you use Syncano.

## App core functionality

* user can search for a restaurant by geo location;
* user can search for a restaurant by empty tables in there;
* user can search for a restaurant by tags (which can describe a menu or special properties like: "kid friendly");
* user can make a reservation for the table; 

## Create all needed models

Firstly you will need definitions of your classes.

On Syncano, to define a class, you use schemas. Schema is a description of your class, listing what fields it holds, of what type, and what type of indexing is used on your fields (if any).

E.g. this: 
```python
"name": "name", "type": "string", "filter_index": True
```
means your field is named `name`, its type is `string` and `filter_index` is enabled -- so you will be able to search for data based on that field.
 
To make things simple -- you want to release MVP first -- you define your classes using following schemas:

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
    {"name": "restaurant", "type": "reference", "target": "restaurant", "filter_index": True},
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
    {"name": "tag", "type": "string", "filter_index": True},
    {"name": "description", "type": "string"},
]

restaurant_schema = [
    {"name": "name", "type": "string", "filter_index": True},
    {"name": "location", "type": "geopoint", "filter_index": True},
    {"name": "phone_number", "type": "string"},
    {"name": "tables", "type": "relation", "target": "table", "filter_index": True},
    {"name": "tags", "type": "relation", "target": "tag", "filter_index": True},
]
```

You created the filter_index attribute for all the fields that are expected to be searchable.

Now, create a class in Syncano

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

Use the following pattern for rest of your classes. 

You can use a script we provided for you -- `init_data.py` -- that automates these tasks. For the script to work properly, you first need to update it with your account details. Open `init_data.py` file, and change following lines:

```python
INSTANCE_NAME = 'INSTANCE NAME'
API_KEY = 'ADMIN API KEY'
```
Replace `INSTANCE NAME` with name of your instance, and `ADMIN API KEY` with your Account Key (you can [find it in your Dashboard](https://dashboard.syncano.io/#/account/authentication)). 
After you provide connection data, run: `python init_data.py` to create all structures needed for you app to work properly. 

(IMPORTANT: running the script again would move you back to the starting point - it clears all the data you provide after running it for the first time). 
Script will also create some sample data objects for you.

```python

# you can use following syntax

item_class = Class.please.get(name='item')
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

It would be nice to know what objects we have initially. To get them, run following code:

```python

# these are available class names
ITEM = 'item'
MENU = 'menu'
RESERVATION = 'reservation'
TABLE = 'table'
TAG = 'tag'
RESTAURANT = 'restaurant'

# query about tags:

for tag in Object.please.list(class_name=TAG):
    print(tag.tag)
    
# query about restaurants:

for restaurant in Object.please.list(class_name=RESTAURANT):
    print(restaurant.name, restaurant.location)

```

### Query on a geopoint field

```python
restaurants = Object.please.list(class_name=RESTAURANT).filter(
    location__near=(
        GeoPoint(52.2297, 21.0122),
        Distance(kilometers=0.1)
    )
)

# or (if restaurant class is present)

restaurant_class = Class.please.get(name=RESTAURANT)
restaurants = restaurant_class.objects.filter(
    location__near=(
        GeoPoint(52.2297, 21.0122),
        Distance(kilometers=0.1)
    )
)

```

Such query will find all restaurants which are 0.1 kilometers from point: latitude = 52.2297, longitude = 21.0122 
- which in our example is `Pit Bull - London Steakhouse`.
 
if you prefer, you can also specify to use `miles` instead of `kilometers`:
 
```python
restaurant_class = Class.please.get(name=RESTAURANT)
restaurants = restaurant_class.objects.filter(
    location__near=(
        GeoPoint(52.2297, 21.0122),
        Distance(miles=0.1)
    )
)
```

### Query on a relation field

Now we will make a query which finds all the restaurants with specified tag.

```python
resturants = Object.please.list(class_name=RESTAURANT).filter(
    tags__tag__eq='pizza'
)

# or (when restaurant class is present)

restaurant_class = Class.please.get(name=RESTAURANT)
restaurants = restaurant_class.objects.filter(
    tags__tag__eq='pizza'
)

```

This will return all restaurants that are related to the tag: `pizza`

### Query on a datetime field

We prepared a `start_date` and `end_date` fields in `menu` class - it's because the menu can be seasonal.
  
Lets play with the datetime queries.

```python

from datetime import datetime

today = datetime.now()

menu_class = Class.please.get(name=MENU)
menus = menu_class.objects.filter(
    start_date__lte=today,
)

```

This query will return all menus that start in the past (earlier than today). Currently it will be both menus
for both defined restaurants.

Lets make a query which allows to obtain menu for a specified restaurant:

```python

# assume we already have the restaurant object, which can be obtained as follows:

restaurant_class = Class.please.get(name=RESTAURANT)
pit_bull = restaurant_class.objects.filter(
    location__near=(
        GeoPoint(52.2297, 21.0122),
        Distance(kilometers=0.1)
    )
).first()

# in menu we have a reference to the restaurant, lets use it:

menu_class = Class.please.get(name=MENU)
menus = menu_class.objects.filter(
    restaurant__eq=pit_bull.id,
    start_date__lte=today,
)

```

### Query on string fields

Python Lib currently supports only one string field specific lookup: starstwith, 

Lets find a menu items which starts with some word.

```python

item_class = Class.objects.get(name=ITEM)
items = item_class.objects.filter(
    name__startswith='Carbo'  # case sensitive
)

```

Currently we are working to add support with another string fields lookups, eg.: istartswith. 

### Query on multiple fields

Lets find all restaurants that have not-reserved tables for 4 people, situated by the window.
And lets make sure that the restaurant name starts with 'Pit';

```python
restaurant_class = Class.please.get(name=RESTAURANT)
restaurants = restaurant_class.objects.filter(
    location__near=(
        GeoPoint(52.2297, 21.0122),
        Distance(miles=0.1)
    ),
    name__startswith='Pit',
    tables__by_window__eq=True,
    tables__reserved__eq=False,
    tables__person_count__gte=4,
)

```

### Make a table reservation

Now when we already have restaurants that meet our criteria - lets make a table reservation;

```python
tables_ids = restaurants[0].tables

table_class = Class.please.get(name=TABLE)
table = table_class.objects.filter(
    id__in=tables_ids, 
    by_window__eq=True, 
    reserved__eq=False,
    person_count__gte=4
).update()

table.reserved = True
table.save()

# check if reservation is successful:
for table in table_class.objects.filter(id__in=tables_ids):
    print(table.reserved)

```

### Add objects to relations

We just mark table as reserved - but do not know to who it is reserved. 
Let's make a reservation object and assign it to the table above;

```python

from datetime import datetime 

reservation_class = Class.please.get(class_name=RESERVATION)
reservation = reservation_class.objects.create(
    user_identifier='user42@example.com',
    date=datetime.now()
)

# from script above
table.reservations_set.add(reservation)  # the table object is refreshed in such scenario;

```
### Remove objects from relations

Removing a object from relation is pretty straightforward, assume that above reservation was cancelled:

```python
table.reservation_set.remove(reservation)
```

### Handle files

We created a files in menu item schema - but there are empty. Lets fill it with some data.

```python

carbonara_item = item_class.objects.filter(
    name__startswith='Carbo'
).first()

header_picture = open('example_files/carbonara1.jpeg', 'r+')
body_picture = open('example_files/carbonara2.jpeg', 'r+')
carbonara_item.header_picture = header_picture
carbonara_item.body_picture = body_picture
carbonara_item.save()

header_picture.close()
body_picture.close()

```

When creating an object with files, you can use following syntax also:

```python
with open('example_files/carbonara1.jpeg', 'r+') as header_picture:
    item_class.objects.create(
        header_picture=header_picture
    )
```

You can use such syntax alternatively.

## Contribute

Contact us if you would like to see more examples here:

* Github: 
    * https://github.com/Syncano/
* Gitter:
    * https://gitter.im/Syncano/community
    * https://gitter.im/Syncano/community-pl
* Slack: 
    * http://syncano-community.github.io/slack-invite/
