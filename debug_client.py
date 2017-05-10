import requests, json, client, players



url = "http://127.0.0.1:4000/jsonrpc"
headers = {'content-type': 'application/json'}
command_args = {'login':['login', 'password'],
                'status':[],
                'action_map':[],
                'merge_wizard':['destination'],
                'player_data':['player_id'],
                'player_data': ['player_id'],
                'player_map': ['player_id'],
                'player_population': ['player_id'],
                'player_inventory': ['player_id'],
                'allocation': []}


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

def allocation(men_list,id):

    #responce = client.send_request('status',[],player.id)
    data = {}
    print('location X: ',end='')
    data['dest_x'] = int(input())
    print('location Y: ',end='')
    data['dest_y'] = int(input())
    print('dest_layer(private = 1, public=0): ',end='')
    data['dest_layer'] = int(input())
    for i in range(len(men_list)):
        if men_list[i]["is_allocated"]:
            continue
        print(i,' - ' ,men_list[i]["name"],men_list[i]["points"])
    print('name number to add: ',end='')
    inp = input()
    man = men_list[int(inp)]
    data['man'] = man["name"]
    return client.send_request('allocation', {'data': data},id)

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
            responce = client.send_request('player_population',args,player.id)
            men_list = responce['result']
            print(men_list)
            client.print_responce(allocation(men_list, player.id))
        else:
            client.print_responce(client.send_request(cmd,args,player.id))


if __name__ == "__main__":
    main()