import time, logging, scenario, rules

class SessionDC:

    def __init__(self, wzrd, db):
        '''
        (Wizard, Database) -> None

        Initial class creation:
            - Creates supporting Scenario class with initial session parameters
            - Gets parameters and players from wizard.
            - Makes self as the players session.
        '''
        self.id = wzrd.id
        self.db = db
        self.players = wzrd.players
        self.rules = rules.Rules(self)
        self.map = []
        self.phase = 'allocation'  # Allocation/Journeys/Evening/Night
        self.log = []  # Game events that will be show to player
        self.round = 1
        self.points = {}
        self.turn_order = self.players[:]
        self.player_turn = self.turn_order[0]
        self.turn_start_time = time.time()
        self.scenario = scenario.ScenarioDC(wzrd.conditions['scenario'], self, self.db)

        for player in self.players:
            player.set_session(self)

        self.scenario.initial_setup()

        return None

    def _get_player(self,player_id):
        '''
        (int) -> Player

        Returns Player class from session players list
        that corresponds to passed ID.
        '''
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    def _get_location(self,player_id,x,y,private):
        '''
        (str,int) -> Location

        Returns Location instance that corresponds to location name.
        Location is looked for in Session map matrix. If not found - than on
        Player map. Player is distinguished by passed player ID.
        '''
        if private == 1:
            player = self._get_player(player_id)
            _map = player.map
        else:
            _map = self.map
        location = _map.locations[x][y]
        return location

    def _next_player_turn(self):
        '''
        (None) -> None

        Switches active player to next player in session players list.
        '''
        player_index = self.players.index(self.player_turn)
        player_index += 1
        if player_index == len(self.players):
            self.player_turn = self.players[0]
        else:
            self.player_turn = self.players[player_index]
        return None

    def _all_players_done(self):
        '''
        (None) -> Bool

        Verifies if all players that belongs to this session does not have
        unallocated men.
        '''
        for player in self.players:
            if player.free_men():
                return False
        return True


    def allocation(self, player_id, data):
        '''
        (int, str, list of str) -> Bool


        '''
        #Validating mandatory parameters
        logging.debug('Allocation command is received from player ['+str(player_id)+']')
        for key in ['dest_x','dest_y','dest_layer','man']:
            if key in data.keys():
                logging.debug('Parameter [' + key + '] is found')
            else:
                logging.error('Parameter [' + key + '] is MISSING')
                return False
        # Allocation within other players turn is allowed only
        # to internal locations
        location = self._get_location(player_id,data['dest_x'],data['dest_y'],data['dest_layer'])
        if not location:
            return False
        if location.type == 'public' and \
           player_id != self.player_turn.id:
            return False
        # Input validation to Game Logic Rules


        # Allocating men to passed location
        player = self._get_player(player_id)
        man_class = player.get_man_by_name(data['man'])
        if not man_class:
            return False
        if location.allocation(man_class):
            man_class.is_allocated = True
        else:
            return False
        # Switch turn to next player in case if current move where belong
        # passed player.
        if player_id == self.player_turn.id:
            self._next_player_turn()
        logging.debug('Allocation flow is successfully finished')
        return True

    def update(self):
        '''
        (None) -> None

        Activates session events that cannot be triggered by user input events.
        (e.g. Player turn timeout)
        '''
        if self.phase == 'allocation':
            if self._all_players_done():
                self.phase = 'day'
                logging.info('Session [' + str(self.id) + ']: Day phase is started')
                self.log = self.rules.process_day_phase()
            elif not self.player_turn.free_men():
                self._next_player_turn()
        return None


    def status(self):
        '''
        (None) -> Dict

        Session data that includes: instance type, game phase,
        active player, TBD
        '''
        status = {'type': 'session',
                  'phase': self.phase,
                  'player_turn': self.player_turn.id}
        '''
        for location in self.map:
            status['map'].append(location.status())'''
        return status

    def map_status(self):
        '''
        (None) -> Dict

        Action map locations status.
        '''
        return self.map.status()