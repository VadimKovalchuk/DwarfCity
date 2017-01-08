import logging, sqlite3

ai_creation_timeout = 1

class Database:
    '''
    .
    '''

    def __init__(self):
        '''
        (list) -> None

        Initial class creation. Without connection to infrastructure.
        '''
        self.core = None
        self.gate = None
        self.db = sqlite3.connect('database/general.db')
        self.db_cursor = self.db.cursor()

        logging.debug('Database is ready')
        return None

    def build_connections(self, infra):
        self.core = infra['core']
        self.gate = infra['gate']
        logging.debug('Database connections are established')
        return None

    def player_login(self, login, password):
        '''
        (None) -> bool

        Validates player credentials.
        '''
        query = 'SELECT id, pass FROM players WHERE login is "' + login +'"'
        self.db_cursor.execute(query)
        row = self.db_cursor.fetchone()
        player_id,db_pass = row
        if db_pass == password:
            return player_id

    def get_free_ai(self):
        '''

        '''
        query = 'SELECT id, login, pass FROM players WHERE ai is "1"'
        self.db_cursor.execute(query)
        rows = self.db_cursor.fetchall()
        for row in rows:
            bot_id = row[0]
            if not self.core.get_instance_by_player(bot_id):
                return {'id':bot_id,'login': row[1], 'pass': row[2]}

        return False

    def location(self, name):
        '''

        '''
        query = 'SELECT type,slots,full_fill,infinite_slots ' \
                'FROM locations WHERE name is "' + name +'"'
        self.db_cursor.execute(query)
        row = self.db_cursor.fetchone()
        return {'type': row[0], 'slots':row[1], 'full_fill':row[2],
                'infinite_slots':row[3]}

    def locationDS(self, name):
        '''

        '''
        query = 'SELECT type,cost,consumption,production,storage,replace ' \
                'FROM locationsDS WHERE name is "' + name +'"'
        self.db_cursor.execute(query)
        row = self.db_cursor.fetchone()
        return {'name': name, 'type': row[0], 'cost':row[1], 'consumption':row[2],
                'production':row[3], 'storage':row[4], 'replace':row[5]}

    def item(self, item_id=None, name=None):
        '''
        (int,str) -> dict

        Returns item data by passed id or name.
        '''
        if not (item_id or name):
            return False
        search_param = 'id' if item_id else 'name'
        search_value = item_id if item_id else name
        param_names = ['id', 'item_type', 'name', 'expiry_term', 'modifier']

        query = 'SELECT ' + ', '.join(param_names) + ' FROM items WHERE ' + search_param + ' is "' + str(search_value) +'"'
        #print(query)
        self.db_cursor.execute(query)
        param_values = self.db_cursor.fetchone()

        result = {}
        for i in range(len(param_names)):
            result[param_names[i]] = param_values[i]
        return result


if __name__ == '__main__':
    db = Database()
    print(db.item(1))
    print(db.item(item_id=2))
    print(db.item(name='bone'))


