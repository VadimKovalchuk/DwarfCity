import requests, json, client, players



url = "http://127.0.0.1:4000/jsonrpc"
headers = {'content-type': 'application/json'}
command_args = {'login':['login', 'password'],
                'status':[],
                'merge_wizard':['destination'],
                'player_data':['player_id'],
                'allocation':[]}


def get_command_arguments(name):
    '''

    '''
    if name in command_args:
        params = {}
        if len(command_args[name]) == 0:
            return {}
        for argument in command_args[name]:
            print(argument,': ',end='')
            value = input()
            params[argument] = value
        return params
    else:
        return False

def login_flow():
    '''

    '''
    for attempt in range(1,4):
        args = get_command_arguments('login')
        response = client.send_request('connect',args,0)
        assert response['id'] != str(0), 'Invalid ID is rescieved for connect request'
        if('result' in response):
            id = response['result']['id']
            return id
        print('Attempt',attempt,'failed.')
    print('Login failed!')

    return None

def allocation(player):

    def free_slots(slots_lst):
        count = 0
        for i in range(len(slots_lst)):
            if slots_lst[i] is None:
                count += 1
        return count

    men = []
    responce = client.send_request('status',[],player.id)
    map_lst = responce['result']['map']
    map_lst.extend(player.infra)
    for i in range(len(map_lst)):
        free = free_slots(map_lst[i]['slots'])
        if free:
            print(i, ' - ', map_lst[i]['name'], ': ', free)

    print('location: ',end='')
    location_index = int(input())
    location_name = map_lst[location_index]['name']
    man_limit = free_slots(map_lst[location_index]['slots'])

    for a in range(man_limit):
        for i in range(len(player.population)):
            if player.population[i].is_allocated:
                continue
            print(i,' - ' ,player.population[i].name,player.population[i].points)
        print('Selected',men)
        print('name number to add: ',end='')
        inp = input()
        if inp == '':
            break
        else:
            man = player.population[int(inp)]
            men.append(man.name)
            man.is_allocated = True

    args = {'location': location_name, 'men': men}
    return client.send_request('allocation',args,player.id)

def main():

    player = players.Player(login_flow())

    command_list =[key for key in command_args]


    while True:
        print('\nCommand list')

        for i in range(0, len(command_list)):
            print(i,' - ', command_list[i])

        print('\n(',player.id,')Seclect command: ',end='')
        user_input = input()
        cmd_id = int(user_input)
        cmd = command_list[cmd_id]
        args = get_command_arguments(cmd)

        if cmd == 'login':
            client.print_responce(login_flow())
        elif cmd == 'merge_wizard':
            client.merge_wizard(player.id,args['destination'])
        elif cmd == 'allocation':
            args = {'player_id':player.id}
            responce = client.send_request('player_data',args,player.id)
            player_data = responce['result']
            client.deserialize_player_data(player,player_data)
            #print(player.data())
            client.print_responce(allocation(player))
        else:
            client.print_responce(client.send_request(cmd,args,player.id))


if __name__ == "__main__":
    main()