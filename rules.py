from random import randint

class Rules:

    def __init__(self, session):
        '''
        (Sesssion) -> None

        Initial class creation.
        '''
        self.session = session

        return None

    def process_day_phase(self):
        '''
        (None) -> TBD

        Performs day phase actions.
        '''
        actions = {player.id: {} for player in self.session.players}
        locations = []
        locations.extend(self.session.map)
        for player in self.session.players:
            locations.extend(player.infra)
            #locations.extend(player.farm)

        for location in locations:
            for man in location.slots:
                if not man:
                    continue
                if location.name not in actions[man.player]:
                    actions[man.player][location.name] = {'men':{}}
                dice_result = randint(1, man.points)
                actions[man.player][location.name]['men'][man.name] = dice_result
                if man.weapon:
                    pass

                man.is_allocated = False
            location.slots = [None for i in range(len(location.slots))]

        for player in self.session.players:
            for action in actions[player.id]:
                points = 0
                for man in actions[player.id][action]['men']:
                    points += actions[player.id][action]['men'][man]
                actions[player.id][action]['created'] = self._location_production(action, points)


        return actions

    def _location_production(self,action, points):

        return {}
