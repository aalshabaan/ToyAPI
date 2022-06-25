from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from ItemDatabase import ItemDatabase, InsufficientStockError
from DatabaseAdapter import ItemAlreadyExistsError, ItemNotFoundError, DatabaseError
from OrderDatabase import OrderDatabase
from utils import IntCommaSeparatedList, CommaSeparatedList

app = Flask(__name__)
api = Api(app)

item_db = ItemDatabase()
order_db = OrderDatabase()

item_parser = RequestParser()
item_parser.add_argument('name', help='Item name, a unique string', default=None)
item_parser.add_argument('type', help='Item type, a string', default='')
item_parser.add_argument('count', help='Count to add or take, an integer', type=int, default=1)
item_parser.add_argument('desc', help='The item description, a string', default='')

order_parser = RequestParser()
order_parser.add_argument('order_id', help='The unique order id', default=None)
order_parser.add_argument('action', help='Fulfill or cancel the order', default=None, choices=['fulfill', 'cancel'])
order_parser.add_argument('contents', help='The names of the order\'s contents', default=None, type=CommaSeparatedList)
order_parser.add_argument('content_counts', help='The counts of the order\'s contents in the same order as the names',
                          default=None, type=IntCommaSeparatedList)



class Order(Resource):
    def get(self, id):
        try:
            order = order_db.item_info(id)
        except ItemNotFoundError as e:
            return e.args[0], 404
        else:
            return order

    def put(self, id):
        args = order_parser.parse_args(strict=True)
        if args['action'] == 'cancel':
            try:
                order_db.cancel_order(id)
            except ItemNotFoundError as e:
                return e.args[0], 404
            else:
                return f'Order {id} cancelled!'

        elif args['action'] == 'fulfill':
            try:
                contents = order_db.get_contents(id)
            except ItemNotFoundError as e:
                return e.args[0], 404
            else:
                available_counts = item_db.count_query(contents.keys())
                for item, available in zip(contents, available_counts):
                    if available < contents[item]:
                        return f'Not enough of item {item}', 409
                # All items are available enough, fulfill the order!
                for item, count in contents.items():
                    try:
                        item_db.take_item(item, count=count)
                    except ItemNotFoundError as e:
                        return e.args[0], 404
                    except InsufficientStockError as e:
                        return e.args[0], 409
                try:
                    order_db.fulfill_order(id)
                except ItemNotFoundError as e:
                    return e.args[0], 404
                else:
                    return f'Order {id} fulfilled!'


class OrderList(Resource):
    def get(self):
        try:
            return order_db.get_item_list()
        except DatabaseError as e:
            return e.args[0], 500

    def post(self):
        args = order_parser.parse_args(strict=True)
        print(args['contents'])

        if args['order_id'] is None:
            return 'New order must have an ID!', 400

        if args['contents'] is None or args['content_counts'] is None:
            return 'New order must have contents and counts!', 400



        known_products = item_db.get_item_list().keys()

        contents = {}

        # Check for unknown items and add known items to order contents
        for item, count in zip(args['contents'], args['content_counts']):
            if item not in known_products:
                return f'Unknown product {item}', 400
            else:
                try:
                    contents[item] = int(count)
                except ValueError as e:
                    return e.args[0], 400

        try:
            order_db.add_item(args['order_id'], contents=contents)
        except DatabaseError as e:
            return e.args[0], 400
        else:
            return 'New order created!'







class Item(Resource):
    def get(self, name):
        try:
            info = item_db.item_info(name)
        except ItemNotFoundError:
            return 'Item not found', 404
        else:
            return info

    def put(self, name):
        args = item_parser.parse_args(strict=True)
        count = args['count']
        if count >= 0:
            try:
                item_db.stock_item(name, count)
            except ItemNotFoundError as e:
                return e.args[0], 404
            else:
                return f'Added {count} items to {name}!'
        else:
            try:
                item_db.take_item(name, -count)
            except ItemNotFoundError as e:
                return e.args[0], 404
            except InsufficientStockError as e:
                return e.args[0], 409
            else:
                return f'Took {abs(count)} items fom {name}!'

    def delete(self, name):
        try:
            item_db.delete_item(name)
        except ItemNotFoundError as e:
            return e.args[0], 404
        else:
            return f'Deleted {name}'

class ItemList(Resource):

    def get(self):
        try:
            return item_db.get_item_list()
        except DatabaseError as e:
            return e.args[0], 500

    def post(self):
        args = item_parser.parse_args(strict=True)
        if args['name'] is None:
            return 'Item needs a name!', 400
        else:
            try:
                item_db.add_item(args['name'],
                                 type=args['type'],
                                 description=args['desc'],
                                 count=args['count'])
            except ItemAlreadyExistsError:
                return 'Item already exists!', 409
            else:
                return 'Item created!', 201


api.add_resource(Item, '/items/<name>')
api.add_resource(ItemList, '/items')
api.add_resource(Order, '/orders/<id>')
api.add_resource(OrderList, '/orders')

def main():


    app.run()

if __name__ == '__main__':
    main()
