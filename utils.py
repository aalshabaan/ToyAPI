class CommaSeparatedList:
    """
    A simple class to parse a string of values separated by ',' as a list of strings
    """
    def __init__(self, parser_string:str):
        self.values = parser_string.strip().split(',')

    def __getitem__(self, item):
        return self.values[item]

    def __iter__(self):
        return self.values.__iter__()

    def __len__(self):
        return len(self.values)

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return repr(self.values)

class IntCommaSeparatedList(CommaSeparatedList):
    """
    Like CommaSeparatedList, only all values are cast to integers
    """
    def __init__(self, parser_string):
        super().__init__(parser_string)
        self.values = [int(x) for x in self.values]