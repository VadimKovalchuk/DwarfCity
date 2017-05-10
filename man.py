class Man:
    '''
    Dwarf class.
    '''

    def __init__(self, player_id, name=''):

        self.player = player_id
        self.name = name
        self.is_allocated = False
        self.points = 5
        self.skills = {}
        self.weapon = None
        self.wear = None
        self.inventory = [None, None, None]

        return None

    def status(self):
        '''
        Detailed status.
        '''
        return self.__dict__

    def map_status(self):
        '''
        Brief status that is returned in case of map view
        '''
        return {'name':self.name,'player':self.player}