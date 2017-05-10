from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import session, wizard, logging,json

# @dispatcher.add_method
# def foobar(**kwargs):
#     return kwargs["foo"] + kwargs["bar"]

class Gate:

    def __init__(self):
        self.core = None
        self.db = None
        self.wizards = []
        self.players = {}
        self.request = None
        logging.debug('Gate is ready')

        return None

    def build_connections(self,infra):
        self.core = infra['core']
        self.db = infra['database']
        logging.debug('Gate connections are established')
        return None

    def update(self):
        if int(self.request["id"]) == 1:
            return self.core.update()
        else:
            return 'Error'

    def player_connect(self, login, password):
        player_id =self.db.player_login(login, password)
        if not player_id:
            return "Invalid credentials"
        current_session = self.core.get_instance_by_player(player_id)
        if not current_session :
            current_session = self.core.add_player(player_id)
        logging.info('Player [' + str(player_id) + '] is connected')
        return {'id':player_id,
                'session_type':str(type(current_session)),
                'session_id':current_session.id
                }

    def session_status(self):
        player_id = int(self.request["id"])
        current_inst = self.core.get_instance_by_player(player_id)
        #print('inst.status:',current_inst.status())
        if current_inst:
            return current_inst.status()
        else:
            return False

    def action_map(self):
        player_id = int(self.request["id"])
        current_inst = self.core.get_instance_by_player(player_id)
        #print('inst.status:',current_inst.status())
        if current_inst:
            return current_inst.map_status()
        else:
            return False

    def wizard_conditions(self,new_conditions):
        player_id = int(self.request["id"])
        current_inst = self.core.get_instance_by_player(player_id)
        if current_inst and 'Wizard' in str(type(current_inst)):
            return current_inst.change_conditions(new_conditions)
        else:
            logging.error(str(type(current_inst))+ " is returned when Wizard "
                                                  "instance expected")
            return False

    def player_status(self,player_id):
        for player in self.core.players:
            if player.id == int(player_id):
                return player.general_status()
        else:
            return False

    def player_map(self,player_id):
        for player in self.core.players:
            if player.id == int(player_id):
                return player.map_status()
        else:
            return False

    def player_population(self,player_id):
        for player in self.core.players:
            if player.id == int(player_id):
                return player.population_status()
        else:
            return False

    def player_inventory(self,player_id):
        for player in self.core.players:
            if player.id == int(player_id):
                return player.inventory_status()
        else:
            return False

    def allocation_command(self,data):
        player_id = int(self.request["id"])
        curent_session = self.core.get_instance_by_player(player_id)
        if 'Session' not in str(type(curent_session)):
            return False
        return curent_session.allocation(player_id, data)


    @Request.application
    def application(self,request):
        self.request = json.loads(request.data.decode("utf-8"))
        #print(request)
        # Dispatcher is dictionary {<method_name>: callable}
        dispatcher["update"] = self.update
        dispatcher["connect"] = self.player_connect
        dispatcher["status"] = self.session_status
        dispatcher["action_map"] = self.action_map
        dispatcher["wizard_conditions"] = self.wizard_conditions
        dispatcher["player_data"] = self.player_status
        dispatcher["player_map"] = self.player_map
        dispatcher["player_population"] = self.player_population
        dispatcher["player_inventory"] = self.player_inventory
        dispatcher["allocation"] = self.allocation_command


        response = JSONRPCResponseManager.handle(
            request.data, dispatcher)
        if response.data['id'] != 1 and 'result' not in response.data:
            print(request.data,'\n',response.data)
            logging.error('_______________________________________________' +
                          '\nRequiest is faulty or its handling was not successfull:\n'+
                          str(request.data) + '\nResponce:\n' + str(response.data) +
                          '\n---------------------------------------------')
        if response.data['id'] == 1000:
            print(request.data,'\n',response.data)

        return Response(response.json, mimetype='application/json')


    def start(self):
        run_simple('', '4000', self.application)