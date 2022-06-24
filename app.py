from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from ItemDatabase import ItemDatabase
from DatabaseAdapter import ItemAlreadyExistsError, ItemNotFoundError, InsufficientStockError

app = Flask(__name__)
api = Api(app)

database = ItemDatabase()

parser = RequestParser()
parser.add_argument('name', help='Item name, a unique string', default='')
parser.add_argument('type', help='Item type, a string', default='')
parser.add_argument('count', help='Count to add or take, an integer', type=int, default=1)
parser.add_argument('desc', help='The item description, a string', default='')

class Item(Resource):
    def get(self, name):
        try:
            info = database.item_info(name)
        except ItemNotFoundError:
            return 'Item not found', 404
        else:
            return info

    def put(self, name):
        args = parser.parse_args(strict=True)
        count = args['count']
        if count >= 0:
            try:
                database.stock_item(name, count)
            except ItemNotFoundError as e:
                return e.args[0], 404
            else:
                return f'Added {count} items to {name}!'
        else:
            try:
                database.take_item(name, -count)
            except ItemNotFoundError as e:
                return e.args[0], 404
            except InsufficientStockError as e:
                return e.args[0], 409
            else:
                return f'Took {abs(count)} items fom {name}!'

    def delete(self, name):
        try:
            database.delete_item(name)
        except ItemNotFoundError as e:
            return e.args[0], 404
        else:
            return f'Deleted {name}'

class ItemList(Resource):

    def get(self):
        return database.get_item_list()

    def post(self):
        args = parser.parse_args(strict=True)
        if args['name'] is None:
            return 'Item needs a name!', 400
        else:
            try:
                database.add_item(args['name'],
                                  type=args['type'],
                                  description=args['desc'],
                                  count=args['count'])
            except ItemAlreadyExistsError:
                return 'Item already exists!', 409
            else:
                return 'Item created!', 201


api.add_resource(Item, '/<name>')
api.add_resource(ItemList, '/')

def main():


    app.run()

if __name__ == '__main__':
    main()
