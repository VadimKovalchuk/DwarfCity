import time, logging, scenario, rules

class Session:

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
        self.scenario = scenario.Scenario(wzrd.conditions['scenario'],self,self.db)
        self.phase = 'allocation'  # Allocation/Day/Evening/Night
        self.log = {}  # Game events that will be show to player
        self.round = 1
        self.points = {}
        self.first_turn = self.players[0]
        self.player_turn = self.players[0]
        self.turn_start_time = time.time()

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

    def _get_location(self,location_name,player_id):
        '''
        (str,int) -> Location

        Returns Location instance that corresponds to location name.
        Location is looked for in Session map list. If not found than in
        Player infra locations. Pleayer is defined by passed player ID.
        '''
        for location in self.map:
            if location.name == location_name:
                return location
        player = self._get_player(player_id)

        if not player:
            return False

        for location in player.infra:
            if location.name == location_name:
                return location
        # for location in player.farm:
        #     if location.name == location_name:
        #         return location
        return False

    def _next_player_turn(self):
        '''
        (None) -> None

        Switches active player to next player in session players list.
        Increases amount of free slots in locations with endless allocation
        possibilities(e.g. Hunting grounds)
        '''
        player_index = self.players.index(self.player_turn)
        player_index += 1
        if player_index == len(self.players):
            self.player_turn = self.players[0]
        else:
            self.player_turn = self.players[player_index]

        for location in self.map:
            if location.infinite_slots:
                free_men = self.player_turn.free_men()
                free_slots = location.free_slots_amount()
                if free_men > free_slots:
                    location.slots.extend([None for i in range(free_men - free_slots)])
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


    def allocation(self, player_id, location_name, men):
        '''
        (int, str, list of str) -> Bool


        '''
        location = self._get_location(location_name, player_id)
        if not location:
            return False

        # Allocation within other players turn is allowed only
        # to internal locations
        if location.type == 'standard' and \
           player_id != self.player_turn.id:
            return False

        # Input validation to Game Logic Rules
        if location.free_slots_amount() < len(men):
            return False
        if location.full_fill is True and \
            location.free_slots_amount() != len(men):
            return False

        # Allocating men to passed location
        player = self._get_player(player_id)
        for name in men:
            man = player.get_man_by_name(name)
            if not man:
                return False
            if location.allocate_man(man):
                man.is_allocated = True
            else:
                return False

        # Switch turn to next player in case if current move where belong
        # passed player.
        if player_id == self.player_turn.id:
            self._next_player_turn()
        logging.debug('Session [' + str(self.id) + ']: Player [' +
                      str(player_id) + '] allocates ' + str(men) +
                      ' to location [' + location_name + ']')
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

        Full session data that includes: instance type, game phase,
        active player, all location with their parameters, TBD
        '''
        status = {'type': 'session',
                  'phase': self.phase,
                  'player_turn': self.player_turn.id,
                  'map':[]}
        for location in self.map:
            status['map'].append(location.status())
        return status