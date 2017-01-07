class Location:
    '''
    Generic location class that used as general location and used as parent
    for all other location classes.
    '''
    def __init__(self, location_data):
        '''
        (list) -> None

        Initial class creation. .
        '''
        self.name = location_data['name']
        self.type = location_data['type'] #Production/Convertion/Modification/etc
        self.full_fill = True if location_data['full_fill'] == 1 else False
        self.infinite_slots = True if location_data['infinite_slots'] == 1 else False
        self.slots = [None for i in range(location_data['slots'])]
        self.stage = None
        self.points = None
        self.days = None

    def free_slots_amount(self):
        '''

        '''
        slots = 0
        for slot in self.slots:
            if slot is None:
                slots += 1
        return slots


    def allocate_man(self,man):
        '''

        '''
        if man.is_allocated:
            return False
        for i in range(len(self.slots)):
            if self.slots[i] is None:
                self.slots[i] = man
                return True
        return False

    def allocation(self):
        return None

    def day(self):
        return None

    def evening(self):
        return None

    def night(self):
        return None

    def status(self):
        status = self.__dict__.copy()
        status['slots'] = []
        for man in self.slots:
            if man:
                status['slots'].append(man.map_status())
            else:
                status['slots'].append(None)
        return status


class Campfire(Location):
    '''
    Basic Campfire class. Inherits from location class
    '''
    def __init__(self,location_data):
        '''

        '''
        Location.__init__(self,location_data)
        self.stage = 'fireless'
        self.days = 3

        return None

    def status(self):
        '''

        '''
        status = Location.status(self)
        status.update({'stage': self.stage,
                       'points': self.points,
                       'days': self.days})
        return status

class Farm(Location):
    '''
    Basic Farm class. Inherits from location class
    '''
    def __init__(self,location_data):
        '''

        '''
        Location.__init__(self,location_data)
        self.stage = 'unplowed'
        self.points = 25
        self.days = 0

        return None

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
        self.slots = location_data['slots']
        self.produce = None
        self.consume = []
        self.days = None

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
        status = self.__dict__.copy()
        status['slots'] = []
        for man in self.slots:
            if man:
                status['slots'].append(man.map_status())
            else:
                status['slots'].append(None)
        return status
