class LocationDC:
    '''
    Generic location class that used as general location and used as parent
    for all other location classes.
    '''
    def __init__(self, location_data):
        '''
        (list) -> None

        Initial class creation.
        '''
        self.name = location_data['name']
        self.type = location_data['type'] #Production/Convertion/Modification/etc
        self.cost = location_data['cost'] #List of required items
        self.consumption = location_data['consumption'] #List of items required for action
        self.production = location_data['production'] # List of items that are going to be produced
        self.storage = location_data['storage'] #Dictionary where key is item and value is extra amout of items for store
        self.replace = location_data['replace'] #List of location that current location can replace
        self.slots = []

    def allocation(self,man):
        '''
        (Man) -> Bool

        Assigns a man to self as target location.
        '''
        if man.is_allocated:
            return False
        for i in range(len(self.slots)):
            if self.slots[i] is None:
                self.slots[i] = man
                return True
        return False

    def harvest(self):
        return None

    def night(self):
        return None

    def status(self):
        status = {}
        status['name'] = self.name
        if not self.slots:
            return status
        status['slots'] = []
        for man in self.slots:
            if man:
                status['slots'].append(man.map_status())
            else:
                status['slots'].append(None)
        return status

class Slot:
    '''
    Slots alow to allocate man on specific location.
    '''
    def __init__(self, cost):
        '''
        (list) -> None

        Initial class creation. Cost defines list of Items required for man allocation on this slot
        '''
        self.man = None
        self.cost = [None]

    def status(self):
        '''

        '''
        return self.__dict__.copy()