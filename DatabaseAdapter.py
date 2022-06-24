class DatabaseError(Exception):
    pass

class ItemAlreadyExistsError(DatabaseError):
    pass

class ItemNotFoundError(DatabaseError):
    pass

class InsufficientStockError(DatabaseError):
    pass

class IllegalKeyError(DatabaseError):
    pass


class DatabaseAdapter:
    """
    Basic data structure class, to be replaced with a class interfacing with an actual database.
    """
    allowed_keys = []
    def __init__(self):
        self.data_ = {}

    def item_info(self, name:str):
        if name not in self.data_:
            raise ItemNotFoundError('Item not found!')
        else:
            return self.data_[name]

    def add_item(self, name:str, **kwargs):
        print(self.allowed_keys)
        if kwargs.keys() - set(self.allowed_keys):
                raise IllegalKeyError(f'Unknown properties {kwargs.keys() - set(self.allowed_keys)}')
        if name in self.data_:
            raise ItemAlreadyExistsError('Item already exists!')
        else:
            self.data_[name] = kwargs

    def delete_item(self, name:str):
        if name not in self.data_:
            raise ItemNotFoundError('Cannot delete a non-existing item!')
        else:
            del self.data_[name]

    def get_item_list(self):
        return self.data_.copy()
