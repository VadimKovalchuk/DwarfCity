import logging, players, wizard,session

class Core:
    '''
    Main class that serves as the transition platform and exchange point between
    all others.
    '''

    def __init__(self):
        '''
        (None) -> None

        Initial class creation. Without connection to infrastructure.
        '''
        self.gate = None
        self.db = None
        self.sessions = []  # active sessions
        self.wizards = []   # wizards of active players
        self.players = []   # Active players
        self.elder_tasks = []#Requests that sent to Elder
        logging.debug('Core is ready')

        return None

    def build_connections(self, infra):
        '''
        (list) -> None

        Creates connection to all infrastructure classes.
        '''
        self.gate = infra['gate']
        self.db = infra['database']
        logging.debug('Core connections are established')
        return None

    def start_session(self,wiz):
        '''
        (Wizard, Database) -> None

        Creates session upon passed wizard parameters.
        '''
        logging.info('Creating new Session [' + str(wiz.id) + ']')
        new_session = session.SessionDC(wiz, self.db)
        print('session:'+ str(type(new_session)))
        self.sessions.append(new_session)
        self.wizards.remove(wiz)
        logging.debug('Session [' + str(new_session.id) + '] is created. '
                     'Corresponding Wizard is deleted')
        return None

    def add_player(self, id):
        '''
        (int) -> Wizard

        Creates player in core list with passed id. Creates Wizard for
        this player and returns this wizard instance.
        '''
        new_player = players.PlayerDC(id)
        self.players.append(new_player)
        new_wiz = wizard.Wizard(new_player)
        self.wizards.append(new_wiz)
        return new_wiz

    def get_instance_by_player(self,id):
        '''
        (int) -> Session

        Returns session/wizard that player with passed ID bind to.
        In case if player does not exists - returns false.
        '''
        for player in self.players:
            if player.id == id:
                return player.session
        else:
            False

    def update_wizard(self, wiz):
        '''
        (Wizard) -> None

        Updates passed wizard instance according to condition parameters.
        '''
        def find_bot_in_task_list(id):
            '''
            (int) -> bool

            Validates if bot is already exists in Elder task list.
            '''
            for task in self.elder_tasks:
                if 'id' in task and task['id'] == id:
                    return True
            else:
                False

        # Players are merging to one wizard. Redundant wizard is deleted.
        if int(wiz.conditions['merge']) != wiz.id:
            logging.debug('Wizard ['+ str(wiz.id) +'] is marked for marging to [' +
                          str(wiz.conditions['merge']) + ']')
            master_wiz_id = int(wiz.conditions['merge'])
            master_wiz = self.get_instance_by_player(master_wiz_id)
            if 'Wizard' not in str(type(master_wiz)):
                logging.error("Wrong class is detected when Wizard expected")
            master_wiz.add_player(wiz.players[0])
            self.wizards.remove(wiz)

        # When player(s) ready to start session - remaining player slots are
        # filled with bots.
        elif wiz.conditions['players'] > len(wiz.players):
            for i in range(0,int(wiz.conditions['players']) > len(wiz.players)):
                new_ai = self.db.get_free_ai()
                if new_ai and not find_bot_in_task_list(new_ai['id']):
                    new_ai['type'] = 'add_bot'
                    new_ai['merge'] = wiz.id
                    self.elder_tasks.append(new_ai)
                    logging.debug('Requesting bot player ['+ str(new_ai['id'])+
                                  '] creation')

        #
        else:
            self.start_session(wiz)

        return None


    def update(self):
        '''
        (None) -> None

        Updates all session and wizard instances.
        '''
        for wiz in self.wizards:
            if wiz.conditions['state'] == 'ready':
                self.update_wizard(wiz)

        for session in self.sessions:
            session.update()

        for request in self.elder_tasks:
            if request['type'] == 'add_bot' and self.get_instance_by_player(request['id']):
                self.elder_tasks.remove(request)

        return self.elder_tasks
