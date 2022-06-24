from DatabaseAdapter import DatabaseAdapter, ItemNotFoundError, ItemAlreadyExistsError

class RequestDatabase(DatabaseAdapter):
    allowed_keys = ['contents', 'status']

    def add_item(self, name:str, **kwargs):
        super(RequestDatabase, self).add_item(name, status='pending', **kwargs)

    def cancel_order(self, name):
        if name in self.data_:
            self.data_[name]['status'] = 'cancelled'
        else:
            raise ItemNotFoundError(f'Unknown order {name}')

    def fulfill_order(self, name):
        if name in self.data_:
            self.data_[name]['status'] = 'delivered'
        else:
            raise ItemNotFoundError(f'Unknown order {name}')