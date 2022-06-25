class DatabaseError(Exception):
    pass

class ItemAlreadyExistsError(DatabaseError):
    pass

class ItemNotFoundError(DatabaseError):
    pass

class IllegalKeyError(DatabaseError):
    pass


class DatabaseAdapter:
    """
    Basic data structure class emulating a NoSQL database, to be replaced with a class interfacing with an actual database.

    The class member "allowed_keys" contains the keys allowed to exist in an item as a measure of security, to be filled by subclasses.
    """
    allowed_keys = []
    def __init__(self):
        self.data_ = {}

    def item_info(self, key:str):
        """
        Return the item having the key key
        :param key: The item's key in the database
        :return: dict: The item's information
        :raises: ItemNotFoundError if the key isn't in the database
        """
        if key not in self.data_:
            raise ItemNotFoundError('Item not found!')
        else:
            return self.data_[key]

    def add_item(self, key:str, **kwargs):
        """
        Add an item to the database
        :param key: The new item's key
        :param kwargs: A python dict containing the item's information, must contain all keys from self.allowed_keys
        :return: None
        :raises: IllegalKeyError: If kwargs contains an unknown key
        :raises: ItemAlreadyExistsError: If the key already exists in the database, keys must be unique
        """
        print(self.allowed_keys)
        if kwargs.keys() - set(self.allowed_keys):
                raise IllegalKeyError(f'Unknown properties {kwargs.keys() - set(self.allowed_keys)}')
        if key in self.data_:
            raise ItemAlreadyExistsError('Item already exists!')
        else:
            self.data_[key] = kwargs

    def delete_item(self, key:str):
        """
        Delete an item from the database
        :param key: The key to delete
        :return: None
        :raises: ItemNoteFoundError if key is not in the database
        """
        if key not in self.data_:
            raise ItemNotFoundError('Cannot delete a non-existing item!')
        else:
            del self.data_[key]

    def get_item_list(self):
        """
        Return a copy of the entire contents of the database
        :return: dict
        """
        return self.data_.copy()
