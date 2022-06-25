from DatabaseAdapter import DatabaseAdapter, ItemNotFoundError

class OrderDatabase(DatabaseAdapter):
    """
    A subclass of DatabaseAdapter with additional
    """
    allowed_keys = ['contents', 'status']

    def add_item(self, name:str, **kwargs):
        super(OrderDatabase, self).add_item(name, status='pending', **kwargs)

    def cancel_order(self, id:str):
        if id in self.data_:
            self.data_[id]['status'] = 'cancelled'
        else:
            raise ItemNotFoundError(f'Unknown order {id}')

    def fulfill_order(self, id:str):
        if id in self.data_:
            self.data_[id]['status'] = 'delivered'
        else:
            raise ItemNotFoundError(f'Unknown order {id}')

    def get_contents(self, id:str):
        if id in self.data_:
            return self.data_[id]['contents']
        else:
            raise ItemNotFoundError(f'Unknown order {id}')