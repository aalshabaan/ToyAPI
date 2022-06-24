from DatabaseAdapter import DatabaseAdapter, InsufficientStockError, ItemNotFoundError

class ItemDatabase(DatabaseAdapter):
    """
    Basic data structure class, to be replaced with a class interfacing with an actual database.
    """
    allowed_keys = ['description', 'count', 'type']

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
