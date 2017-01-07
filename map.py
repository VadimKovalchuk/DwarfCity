class Map:
    '''
    Generic map class that used as parent for clan and action maps.
    '''
    def __init__(self, player, width=6, hight=4):
        '''
        (list) -> None

        Initial class creation.
        '''
        self.player = player # Player ID. "0" in case if it is action map
        self.locations = [[None for i in range(hight)] for i in range(width)]

    def harvest(self):
        '''
        Updates all location in harvest phase by evoking corresponding method
        '''
        return None

    def switch_location(self, location, x, y):
        '''
        Updates all location in harvest phase by evoking corresponding method
        '''
        return None