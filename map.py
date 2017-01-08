class Map:
    '''
    Generic map class that used as parent for clan and action maps.
    '''
    def __init__(self, player, width=6, height=4):
        '''
        (list) -> None

        Initial class creation.
        '''
        self.player = player # Player ID. "0" in case if it is action map
        self.locations = [[None for y in range(height)] for x in range(width)]

    def harvest(self):
        '''
        Updates all location in harvest phase by evoking corresponding method
        '''
        return None

    def switch_location(self, location, x, y):
        '''
        (Location, int, int) -> Location
        Replaces existing location with defined coordinates with the new one.
        Returns old one
        '''
        replaced, self.locations[x][y] = self.locations[x][y], location
        return replaced

    def status(self):
        '''
        Returns status for all locations on map
        '''
        result = [['' for i in range(self.locations[0])] for i in range(self.locations)]
        for x in range(self.locations):
            for y in range(self.locations[x]):
                result[x][y] = self.locations[x][y]
        return result