import sys, time, client, players

def login_flow():
    '''

    '''
    args = {"login": sys.argv[1], "password": sys.argv[2]}
    response = client.send_request('connect',args,0)
    assert response['id'] != str(0), 'Invalid ID is rescieved for connect request'
    if('result' in response):
        id = response['result']['id']
        return id

def update_wizard(player_id):
    '''

    '''
    args = {'new_conditions':{'merge': sys.argv[3], 'state': 'ready'}}
    print(client.send_request('wizard_conditions',args,player_id))

def get_free_man(player):
    '''

    '''
    for man in player.population:
        if man.is_allocated:
            continue
        else:
            return man
    return False

command_flows = {'connect': login_flow,
                 'wizard_conditions':update_wizard}

def main():

    player = players.PlayerDC(login_flow())

    print('AI '+ str(player.id) + '(' + sys.argv[1] + '/'+ sys.argv[2] +') is created. merging it to wizard '+ sys.argv[3])
    update_wizard(player.id)

    while True:
        time.sleep(10)
        responce = client.send_request('status',[],player.id)
        print(responce)
        status = responce['result']
        if status['type'] == "wizard":
            continue
        if status['phase'] == 'allocation' and status['player_turn'] == player.id:
            args = {'player_id':player.id}
            responce = client.send_request('player_data',args,player.id)
            player_data = responce['result']
            client.deserialize_player_data(player,player_data)
            free_man = get_free_man(player)
            if free_man:
                args = {'location': 'hunting_grounds', 'men': [free_man.name]}
                if client.send_request('allocation',args,player.id)['result']:
                    print('AI '+ str(player.id) + '(' + sys.argv[1] + '/'+ sys.argv[2] +'): sending ' + free_man.name + ' to hunting grounds')
        #print('AI '+ str(player.id) + '(' + sys.argv[1] + '/'+ sys.argv[2] +'):'+ str(client.send_request('status',[],player.id)))


if __name__ == "__main__":
    main()