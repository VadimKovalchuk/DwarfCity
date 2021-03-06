import location, man, map, items
import logging

start_pop_amount = 2

names = ["Rubrour", "Kildruk", "Lokkomri", "Lughoick", "Thastreath", "Hofoud", "Janmen",
                 "Oldrug", "Heddeat", "Dourdrami", "Yurharlig", "Dolonlir", "Rumruc", "Jalik"]

class ScenarioDC:

    def __init__(self, name, session, db):
        '''
        (str, Database) -> None

        Initial class creation. Gets parameters and players from wizard.
        Makes self as the players session.
        '''
        self.name = name
        self.session = session
        self.db = db

        return None



    def _create_player_map(self, player):
        '''
        (Player) -> None

        Creates map for passed player according to Scenario rules.
        '''
        player.map = map.Map(player.id)

        for x in range(len(player.map.locations)):
            for y in range(len(player.map.locations[0])):
                if x < 3:
                    location_class = self.db.locationDS("forest")
                else:
                    location_class = self.db.locationDS("rock")
                player.map.switch_location(location_class, x,y)

        location_class = self.db.locationDS("root cavern")
        player.map.switch_location(location_class, 3, 0)

        location_class = self.db.locationDS("cavern")
        player.map.switch_location(location_class, 3, 1)
        return None

    def _create_action_map(self):
        '''
        (None) -> None

        Creates action map according to Scenario rules.
        '''
        distribution = [["excavation","tunnel", "ore mining",   "ruby mining", "tunnel",   "ore stockpile"],
                        ["furnishing","tunnel","mine construction","tunnel",    "tunnel",   "blacksmith"],
                        ["tunnel",  "tunnel",   "tunnel",       "tunnel",   "pasture building","tunnel"],
                        ["logging", "barn",     "farming",      "tunnel",   "sheep farming","donkey farming"]]
        self.session.map = map.Map(self.session.id)
        s_map = self.session.map
        for x in range(len(s_map.locations)):
            for y in range(len(s_map.locations[0])):
                location_class = self.db.locationDS(distribution[y][x])
                s_map.switch_location(location_class, x,y)
        return None

    def _create_map(self):
        '''
        Creates action and players maps
        '''
        for player in self.session.players:
            self._create_player_map(player)
        self._create_action_map()
        return None


    def _starting_population(self):
        '''

        '''
        for player in self.session.players:
            player.population = [man.Man(player.id,names[i]) \
                                 for i in range(start_pop_amount)]
        return None

    def _starting_infra(self):
        '''

        '''

        return None

    def _starting_inventory(self):
        '''
        (None) -> None

        Defines amount of items and resources that players should start with
        '''
        for player in self.session.players:
            for i in range(12):
                player.stock.append(items.Item(self.db.item(name='food')))

        return None

    def initial_setup(self):
        '''

        '''
        logging.debug('Session [' + str(self.session.id) + '] is applied with '
                                'Scenario [' + self.name + ']')
        self._create_map()
        self._starting_population()
        self._starting_infra()
        self._starting_inventory()

        return None

    def update_map(self):
        '''

        '''
        pass