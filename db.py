import logging, sqlite3,location

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

    def _build_dict(self, raw_dict):
        '''
        (str) -> dict

        Converts string to dictionary.
        Returns parced dictionary
        '''
        if not (raw_dict.find(',') and raw_dict.find(':')):
            assert True, "Wrong string is passed to dictionary builder during DB interaction"
        result = {}
        pairs = raw_dict.split(',')
        for pair in pairs:
            key,value = pair.split(':')
            result[key] = value
        return result

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

    def locationDS(self, name):
        '''

        '''
        query = 'SELECT type,cost,storage,replace ' \
                'FROM locationsDS WHERE name is "' + name +'"'
        self.db_cursor.execute(query)
        row = self.db_cursor.fetchone()
        if not row:
            logging.error('Location ['+name+'] is missing in DB')
            return False
        # Build Storage dictionary
        if row[2]:
            if row[2].find(',') and row[2].find(':'):
                storage = self._build_dict(row[2])
            else:
                storage = {}
        else:
            storage = {}
        # Build Cost list
        if row[1]:
            cost = row[1].split()
        else:
            cost = []
        # Build Replace list
        if row[3]:
            replace = row[3].split()
        else:
            replace = []
        result_location = location.LocationDC(name=name, loc_type=row[0], cost=cost, storage=storage, replace=replace)
        result_location.recipes = self._recipes(name)

        return result_location

    def _recipes(self, name):
        '''
        (str) -> list of Recipe

        Returns list of recipes for inputed location name
        '''
        query = 'SELECT required,produced,stage,automatic ' \
                'FROM recipes WHERE location is "' + name + '"'
        self.db_cursor.execute(query)
        rows = self.db_cursor.fetchall()
        if not rows:
            return []
        recipes = []
        for row in rows:
            required = row[0].split()
            produced = row[1].split()
            automatic = True if row[3] == 'True' else False
            current_recipe = location.Recipe(required=required,produced=produced,stage=row[2],automatic=automatic)
            recipes.append(current_recipe)
        return recipes

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


