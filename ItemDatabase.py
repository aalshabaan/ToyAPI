from DatabaseAdapter import DatabaseAdapter,DatabaseError, ItemNotFoundError
from typing import Iterable

class InsufficientStockError(DatabaseError):
    pass

class ItemDatabase(DatabaseAdapter):
    """
    A subclass of DatabaseAdapter with additional methods to represent a database of items
    """
    allowed_keys = ['description', 'count', 'type']

    def __init__(self):
        """
        Initialize the item database with some items for testing
        """
        super().__init__()
        self.data_['sim'] = {'type': 'micro',
                             'description': 'A micro sim',
                             'count': 20}
        self.data_['router'] = {'type': 'bad',
                                'description': 'A shitty router',
                                'count': 999}

    def stock_item(self, name:str, count:int=1):
        """
        Increase the item stock by count
        :param name: The item's name, this is used as the key in the database
        :param count: The wanted increase
        :return: None
        :raises ItemNotFoundError if the item is not in the database
        """
        if name not in self.data_:
            raise ItemNotFoundError('Cannot stock a non-existing item!')
        else:
            self.data_[name]['count'] += count

    def take_item(self, name:str, count:int=1):
        """
        Reduce the item's stock by count, if count is bigger than the stock throws an error instead
        :param name: The item's name
        :param count: The wanter count to take
        :return: None
        :raises ItemNotFoundError if the item is not in the database
        :raises InsufficientStockError if the wanted quantity is bigger than the actual stock
        """
        if name not in self.data_:
            raise ItemNotFoundError('Cannot take a non-existing item!')
        elif count > self.data_[name]['count']:
            raise InsufficientStockError(f'Not enough items!, only {self.data_[name]["count"]} available')
        else:
            self.data_[name]['count'] -= count

    def get_count(self, name:str):
        """
        Returns the count of a certain item in the database
        :param name: item's name
        :return: item's current stock
        :raises ItemNotFoundError if the item is not in the database
        """
        if name not in self.data_:
            raise ItemNotFoundError(f'Unknown item {name}')
        else:
            return self.data_[name]['count']

    def count_query(self, names:Iterable[str]):
        """
        Returns the counts of items whose names are contained in names. This is a convenience method. This uses get_count so can raise ItemNotFoundError
        :param names: An iterable containing the wanted names
        :return: List, the counts in the same order as names
        """
        return [self.get_count(n) for n in names]
