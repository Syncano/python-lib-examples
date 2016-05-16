
import syncano
from syncano.models import Class, Instance, Object, GeoPoint


INSTANCE_NAME = ''
API_KEY = ''
SYNCANO_HOST = ''

connection = syncano.connect(
    host=SYNCANO_HOST,
    api_key=API_KEY,
    instance_name=INSTANCE_NAME,
    verify_ssl=False
)


for restaurant in Object.please.list(class_name='restaurant'):
    print(restaurant.name, restaurant.location)

# filter with geo

# filter on relation field

# filter on datetime field (create new menu)

# filter on string fields

# filter on multiples fields

# filter on tags

# add files to the menu items

# add relations

# remove relations

# table reservation

