import root,json_handle,db, logging

def main():
    logging.basicConfig(filename='log/core.log', level=logging.DEBUG)
    logging.info('Init base classes')

    core = root.Core()
    gate = json_handle.Gate()
    database = db.Database()

    logging.info('Build infrastructure connections')
    infra = {'core':core,'gate':gate,'database':database}
    for module in infra:
        infra[module].build_connections(infra)

    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    gate.start()

if __name__ == '__main__':
    main()