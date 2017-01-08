class Player:

    def __init__(self, id):
        '''
        (list) -> None

        Initial class creation.
        '''
        self.id = id
        self.session = None # Session/Wizard that player is connected to
        self.population = []
        self.stock = []
        self.skills = {}
        self.infra = []     # Locations inside tribe territory and their state
        self.idle_turns = 0 # Number of turns that player was idle
                            # during allocation phase

        return None

    def set_session(self, session):
        '''
        (Session) -> None

        Changes session/wizard that player belongs to.
        '''
        self.session = session

    def get_man_by_name(self, name):
        '''
        (str) -> Man

        Returns mans class that has passed name.
        (returns first instance! name should be unique!)
        '''
        for man in self.population:
            if name == man.name:
                return man
        return False

    def free_men(self):
        '''
        (None) -> int

        Returns amount of unallocated men.
        '''
        free_men = 0
        for man in self.population:
            if not man.is_allocated:
                free_men += 1
        return free_men

    def data(self):
        '''
        (None) -> dict

        Returns dictionary that should be passed to players client in order to
        represent all required information.
        '''
        stock_dict = {}
        for item in self.stock:
            if item.type not in stock_dict:
                stock_dict[item.type] = {}
            if item.name not in stock_dict[item.type]:
                stock_dict[item.type][item.name] = 1
            else:
                stock_dict[item.type][item.name] += 1

        return {'population': [man.status() for man in self.population],
                'stock': stock_dict,
                'skills': self.skills,
                'infra': [location.status() for location in self.infra]
                }

class PlayerDS:

    def __init__(self, id):
        '''
        (list) -> None

        Initial class creation.
        '''
        self.id = id
        self.session = None # Session/Wizard that player is connected to
        self.population = []
        self.stock = []
        self.map = None     # Locations inside tribe territory and their state
        self.idle_turns = 0 # Number of turns that player was idle
                            # during allocation phase

        return None

    def set_session(self, session):
        '''
        (Session) -> None

        Changes session/wizard that player belongs to.
        '''
        self.session = session

    def get_man_by_name(self, name):
        '''
        (str) -> Man

        Returns mans class that has passed name.
        (returns first instance! name should be unique!)
        '''
        for man in self.population:
            if name == man.name:
                return man
        return False

    def free_men(self):
        '''
        (None) -> int

        Returns amount of unallocated men.
        '''
        free_men = 0
        for man in self.population:
            if not man.is_allocated:
                free_men += 1
        return free_men

    def data(self):
        '''
        (None) -> dict

        Returns dictionary that should be passed to players client in order to
        represent all required information.
        '''
        stock_dict = {}
        for item in self.stock:
            if item.type not in stock_dict:
                stock_dict[item.type] = {}
            if item.name not in stock_dict[item.type]:
                stock_dict[item.type][item.name] = 1
            else:
                stock_dict[item.type][item.name] += 1

        return {'population': [man.status() for man in self.population],
                'stock': stock_dict,
                'map': self.map.status()
                }
