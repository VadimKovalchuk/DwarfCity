import requests, json , man

url = "http://localhost:4000/jsonrpc"
headers = {'content-type': 'application/json'}

def send_request(method,params,id):
    '''

    '''
    payload = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": id,
        }
    response = requests.post(url,
                             data=json.dumps(payload),
                             headers=headers).json()
    assert response['id'] != str(id), 'Invalid ID is rescieved for connect request'

    return response


def merge_wizard(player_id, destination):
    '''

    '''
    args = {'new_conditions':{'merge': destination, 'state': 'ready'}}
    print_responce(send_request('wizard_conditions',args,player_id))

    return None

def print_responce(responce):

    def output_data(data,recursion_depth):

        if type(data) == type({}):
            print("+",end='')
            for block in data:
                print("\t"*recursion_depth,block)
                output_data(data[block],recursion_depth+1)
        elif type(data) == type([]):
            for block in data:
                output_data(block,recursion_depth+1)
        else:
            print("\t"*recursion_depth,data)



    if 'result' in responce:
        print(json.dumps(responce['result'],indent=4))
        '''
        output_data(responce['result'],0)
        return None
        if type(responce['result']) not in (type(dict),type(list)):
            print(responce['result'])
            return None

        for block in responce['result']:
            print(block,"\n\t", responce['result'][block])
        '''
    else:
        print("Responce has failed\n",responce)

def deserialize_player_data(player,json_responce):
    '''

    '''
    player.population = []
    for man_data in json_responce['population']:
        man_class = man.Man(player.id,man_data['name'])
        deserialize_man_data(man_class,man_data)
        player.population.append(man_class)
    player.infra = json_responce['infra']

    return None

def deserialize_man_data(man_class, data):
    '''

    '''
    man_class.alive = data['alive']
    man_class.is_allocated = data['is_allocated']
    man_class.points = data['points']
    man_class.weapon = data['weapon']
    man_class.wear = data['wear']
    man_class.inventory = data['inventory']

    return None