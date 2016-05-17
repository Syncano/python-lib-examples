
import syncano
from syncano.models import Class, Distance, GeoPoint, Object


INSTANCE_NAME = ''
API_KEY = ''
SYNCANO_HOST = ''

connection = syncano.connect(
    host=SYNCANO_HOST,
    api_key=API_KEY,
    instance_name=INSTANCE_NAME,
    verify_ssl=False
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

# Query on string fields

# Query on multiples fields

# Query on related tags

# Handle the files

# Add objects to relations

# Remove objects from relations

# Made a table reservation
