from DatabaseAdapter import DatabaseAdapter,DatabaseError, ItemNotFoundError
from typing import Iterable

class InsufficientStockError(DatabaseError):
    pass

class ItemDatabase(DatabaseAdapter):
    """
    Basic data structure class, to be replaced with a class interfacing with an actual database.
    """
    allowed_keys = ['description', 'count', 'type']

    def __init__(self):
        super().__init__()
        self.data_['sim'] = {'type': 'micro',
                             'description': 'A micro sim',
                             'count': 20}
        self.data_['router'] = {'type': 'bad',
                                'description': 'A shitty router',
                                'count': 999}

    def stock_item(self, name:str, count:int=1):
        if name not in self.data_:
            raise ItemNotFoundError('Cannot stock a non-existing item!')
        else:
            self.data_[name]['count'] += count

    def take_item(self, name:str, count:int=1):
        if name not in self.data_:
            raise ItemNotFoundError('Cannot take a non-existing item!')
        elif count > self.data_[name]['count']:
            raise InsufficientStockError(f'Not enough items!, only {self.data_[name]["count"]} available')
        else:
            self.data_[name]['count'] -= count

    def get_count(self, name:str):
        if name not in self.data_:
            raise ItemNotFoundError(f'Unknown item {name}')
        else:
            return self.data_[name]['count']

    def count_query(self, names:Iterable[str]):
        return [self.get_count(n) for n in names]
