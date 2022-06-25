from DatabaseAdapter import DatabaseAdapter, ItemNotFoundError

class OrderDatabase(DatabaseAdapter):
    """
    A subclass of DatabaseAdapter with additional methods to treat orders.
    """
    allowed_keys = ['contents', 'status']

    def add_item(self, id:str, **kwargs):
        """
        Add a new order with the status 'pending'. It can later be fulfilled or cancelled using appropriate methods
        :param id: The new order id, this is the key in the database
        :param kwargs: Other parameters of the object, a python dict
        :return: None
        """
        super(OrderDatabase, self).add_item(id, status='pending', **kwargs)

    def cancel_order(self, id:str):
        """
        Mark the wanted order as cancelled
        :param id: wanter order id
        :return: None
        :raises: ItemNotFoundError if the id is not in the order database
        """
        if id in self.data_:
            self.data_[id]['status'] = 'cancelled'
        else:
            raise ItemNotFoundError(f'Unknown order {id}')

    def fulfill_order(self, id:str):
        """
        Mark the wanted order as fulfilled
        :param id: The order's id
        :return: None
        :raises ItemNotFoundError if the item is not in the database
        """
        if id in self.data_:
            self.data_[id]['status'] = 'delivered'
        else:
            raise ItemNotFoundError(f'Unknown order {id}')

    def get_contents(self, id:str):
        """
        Return the contents of a specific order
        :param id: The order's id
        :return: dict, the order's contents, keys are keys from the item database and values are counts of each item
        :raises ItemNotFoundError if the item is not in the database
        """
        if id in self.data_:
            return self.data_[id]['contents']
        else:
            raise ItemNotFoundError(f'Unknown order {id}')