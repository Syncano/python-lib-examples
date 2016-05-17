
from datetime import datetime

import syncano
from syncano.models import Class, Distance, GeoPoint, Object

INSTANCE_NAME = 'INSTANCE NAME'
API_KEY = 'ADMIN API KEY'

connection = syncano.connect(
    api_key=API_KEY,
    instance_name=INSTANCE_NAME,
)

# get the list of restaurant;
print('Restaurants:')
for restaurant in Object.please.list(class_name='restaurant'):
    print(restaurant.name, restaurant.location)

# get the list of tags;
print('Tags:')
for tag in Object.please.list(class_name='tag'):
    print(tag.tag)


# Query on geopoint field

restaurants = Object.please.list(class_name='restaurant').filter(
    location__near=(
        GeoPoint(52.2297, 21.0122),
        Distance(kilometers=0.1)
    )
)

print('Restaurants with 0.1 km from the 52.2297, 21.0122 location:')
for restaurant in restaurants:
    print(restaurant.name)

# or, if you already have the class:

restaurant_class = Class.please.get(name='restaurant')
restaurants = restaurant_class.objects.filter(
    location__near=(
        GeoPoint(52.2297, 21.0122),
        Distance(kilometers=0.1)
    )
)

print('Restaurants with 0.1 km from the 52.2297, 21.0122 location:')
for restaurant in restaurants:
    print(restaurant.name)


# Query on relation field

resturants = Object.please.list(class_name='restaurant').filter(
    tags__tag__eq='pizza'
)

print('Restaurants with tag: pizza')
for restaurant in restaurants:
    print(restaurant.name)

# or, if you have the class:

restaurant_class = Class.please.get(name='restaurant')
restaurants = restaurant_class.objects.list().filter(
    tags__tag__eq='pizza'
)

print('Restaurants with tag: pizza')
for restaurant in restaurants:
    print(restaurant.name)


# Query on datetime field

today = datetime.now()

menu_class = Class.please.get(name='menu')
menus = menu_class.objects.filter(
    start_date__lte=today,
)

print('Menu that has start_date less or equal and end_date equal to null (the current valid menu):')
for menu in menus:
    print(menu.name)

restaurant_class = Class.please.get(name='restaurant')
pit_bull = restaurant_class.objects.filter(
    location__near=(
        GeoPoint(52.2297, 21.0122),
        Distance(miles=0.1)
    )
).first()

# in menu we have a reference to the restaurant, lets use it

menus = menu_class.objects.filter(
    restaurant__eq=pit_bull.id,
    start_date__lte=today,
)

print('Menu that has start_date less or equal and end_date equal to null (the current valid menu) and'
      'belongs to the Pit Bull restaurant:')
for menu in menus:
    print(menu.name)

# Query on string fields

item_class = Class.please.get(name='item')
items = item_class.objects.filter(
    name__startswith='Carbo'
)

print('A menu items which starts from Carbo (case sensitive)')
for item in items:
    print(item.name)

# Query on multiples fields

restaurants = restaurant_class.objects.filter(
    location__near=(
        GeoPoint(52.2297, 21.0122),
        Distance(miles=0.1)
    ),
    name__startswith='Pit',
    tables__by_window__eq=True,
    tables__person_count__gte=4,
)

print("Restaurants with tables by window for 4 people in provided location wich name starts with Pit")
for restaurant in restaurants:
    print(restaurant.name)

# Made a table reservation

tables_ids = restaurants[0].tables

table_class = Class.please.get(name='table')

table = table_class.objects.filter(
    id__in=tables_ids,
    by_window__eq=True,
    reserved__eq=False,
    person_count__gte=4
).first()

table.reserved = True
table.save()

print('Check if reservation was successful:')
for _table in table_class.objects.filter(id__in=tables_ids):
    if _table.reserved:
        print('Reservation successful.')

# Add objects to relations

reservation_class = Class.please.get(name='reservation')
reservation = reservation_class.objects.create(
    user_identifier='user42@example.com',
    date=datetime.now()
)

# from script above
table.reservations_set.add(reservation)  # the table object is refreshed in such scenario;

print('Table {} reservations:'.format(table.identifier))
print(table.reservations)

# Remove objects from relations
table.reservations_set.remove(reservation)

print('Table {} reservations after remove:'.format(table.identifier))
print(table.reservations)

table.reserved = False
table.save()  # to make sure that examples will be working all the time

# Handle the files

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

carbonara_item.reload()

print('Menu item images:')
print(carbonara_item.header_picture)
print(carbonara_item.body_picture)
