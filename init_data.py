
from datetime import datetime

import syncano
from syncano.models import Class, GeoPoint, Object

INSTANCE_NAME = 'INSTANCE NAME'
API_KEY = 'ADMIN API KEY'

connection = syncano.connect(
    api_key=API_KEY,
    instance_name=INSTANCE_NAME,
)


class RestaurantAppDataCreator(object):

    ITEM = 'item'
    MENU = 'menu'
    RESERVATION = 'reservation'
    TABLE = 'table'
    TAG = 'tag'
    RESTAURANT = 'restaurant'

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

    def clear_classes(self):
        for class_name in [self.ITEM, self.MENU, self.TABLE, self.TAG, self.RESTAURANT, self.RESERVATION]:
            try:
                Class.please.delete(name=class_name)
            except Class.DoesNotExist:
                continue

    def populate_classes(self):

        classes = [
            (self.RESERVATION, self.reservation_schema),
            (self.TABLE, self.table_schema),
            (self.TAG, self.tag_schema),
            (self.RESTAURANT, self.restaurant_schema),
            (self.ITEM, self.item_schema),
            (self.MENU, self.menu_schema),
        ]

        for cl in classes:
            class_name = cl[0]
            class_schema = cl[1]
            Class.please.create(name=class_name, schema=class_schema)

    def populate_initial_objects(self):
        # create restaurants
        # you can do it that way
        pit_bull = Object.please.create(
            class_name=self.RESTAURANT,
            name='Pit Bull - London Steakhouse',
            phone_number='+48 444 333 222',
            location=GeoPoint(52.2297, 21.0122),
        )
        # or that way (this one is shorter and looks better)
        restaurant_class = Class.please.get(name=self.RESTAURANT)  # this can be assigned when class was created;
        blue_pizza = restaurant_class.objects.create(
            name='Blue Pizza',
            phone_number='+48 444 333 111',
            location=GeoPoint(51.2000, 20.0100),
        )

        # create tags

        steaks_tag = Object.please.create(class_name=self.TAG, tag='steaks')
        burgers_tag = Object.please.create(class_name=self.TAG, tag='burgers')
        pizza_tag = Object.please.create(class_name=self.TAG, tag='pizza')
        pasta_tag = Object.please.create(class_name=self.TAG, tag='pasta')

        # assing tags to restaurants
        pit_bull.tags_set.add(steaks_tag, burgers_tag)
        blue_pizza.tags_set.add(pizza_tag, pasta_tag)

        # create tables
        table_in_pit_bull_a = Object.please.create(
            class_name=self.TABLE,
            person_count=4,
            by_window=True,
            reserved=False,
            identifier='Table A',
        )
        table_in_pit_bull_b = Object.please.create(
            class_name=self.TABLE,
            person_count=2,
            by_window=False,
            reserved=False,
            identifier='Table B'
        )

        table_in_blue_pizza_c = Object.please.create(
            class_name=self.TABLE,
            person_count=4,
            by_window=True,
            reserved=False,
            identifier='Table C',
        )
        table_in_blue_pizza_d = Object.please.create(
            class_name=self.TABLE,
            person_count=2,
            by_window=False,
            reserved=False,
            identifier='Table D'
        )

        # assign to restaurants
        pit_bull.tables_set.add(table_in_pit_bull_a, table_in_pit_bull_b)
        blue_pizza.tables_set.add(table_in_blue_pizza_c, table_in_blue_pizza_d)

        # create menu items

        steak = Object.please.create(
            class_name=self.ITEM,
            name="T Bone",
            description="T Bone steak",
            price=60
        )
        burger = Object.please.create(
            class_name=self.ITEM,
            name="The Killer",
            description="300 g burger with 200 g of bacon",
            price=35
        )
        pizza = Object.please.create(
            class_name=self.ITEM,
            name="Four seasons",
            description="Four kinds of cheese",
            price=30
        )
        pasta = Object.please.create(
            class_name=self.ITEM,
            name="Carbonara",
            description="Pasta with bacon and eggs",
            price=35
        )

        # create menus
        now = datetime.now()
        steakhouse_menu = Object.please.create(  # noqa
            class_name=self.MENU,
            name="Burger promo 1",
            restaurant=pit_bull.id,
            start_date=now,
            items=[steak, burger]
        )
        pizza_menu = Object.please.create(  # noqa
            class_name=self.MENU,
            name="Calzone promo 1",
            restaurant=blue_pizza.id,
            start_date=now,
            items=[pizza, pasta]
        )

    def rebuild_data(self):
        self.clear_classes()
        self.populate_classes()
        self.populate_initial_objects()

r_app = RestaurantAppDataCreator()
r_app.rebuild_data()
