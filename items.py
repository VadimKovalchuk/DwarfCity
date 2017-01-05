class Item:
    '''

    '''

    def __init__(self, item_data):
        '''
        (int, str, str, int, int) -> None

        Initial class creation with parameters assignment.
        '''
        self.id = item_data['id']
        self.type = item_data['item_type']  # resource, weapon, instrument, consumable, wear
        self.name = item_data['name']
        self.expiry_term = item_data['expiry_term'] if item_data['expiry_term'] else 999
        self.modifier = item_data['modifier'] if item_data['modifier'] else 0
        self.icon = item_data['name']

        return None

    def aging(self, amount=1):
        '''
        (int) -> None

        Decrease of expiry term for resorces or durability for items
        '''
        self.expiry_term -= amount
        return None

    def status(self):
        '''
        (None) -> dict

        Returns all item parameters.
        '''
        return self.__dict__

    def __str__(self):
        return self.name + '(' + str(self.expiry_term) + ')'

