import logging

class Wizard:

    def __init__(self, initial_player):
        '''
        (list) -> None

        Initial class creation.
        '''
        self.id = initial_player.id
        self.players = [initial_player]
        self.conditions = {'type': 'wizard',
                           'scenario': 'free',
                           'players': 4,
                           'map': 'classic',
                           'state': 'decision',
                           'merge': self.id
                           }

        self.players[0].set_session(self)
        logging.debug('Wizard [' + str(self.id) + '] is created')

        return None

    def change_conditions(self,new_values):
        '''
        (dict) -> bool

        Changes conditions for session creation.
        '''
        logging.debug('Wizard [' + str(self.id) + '] is updated with parameters:'+
                      str(new_values))

        for parameter in new_values:
            if parameter in self.conditions:
                self.conditions[parameter]= new_values[parameter]
            else:
                logging.error("Wizard ["+ str(self.id)
                              +"] Wrong parameter is sent to conditions")
                return False
        return True

    def status(self):
        '''
        (None) -> Dict
        '''
        result = self.conditions.copy()
        result['wizard_id']= self.id
        result['current_players'] = [ player.id for player in self.players]
        return result

    def add_player(self, new_player):
        '''
        (Player) -> None

        Adds passed player to curent players list and replaces his
        active session to self.
        '''
        logging.debug('Wizard [' + str(self.id) + '] got new player [' +
                      str(new_player.id) + ']')

        self.players.append(new_player)
        new_player.set_session(self)

        return None
