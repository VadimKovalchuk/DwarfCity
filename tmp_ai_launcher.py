from platform import system
import os, subprocess,time

python_path = 'C:\\Users\\vkovalchuk\\AppData\\Local\\Programs\\Python\\Python35-32\\python.exe'
bots = {1: {'login':'qwe','pass':'123'},
        2: {'login':'zxc','pass':'123'},
        3: {'login':'123','pass':'123'}
        }
wiz_id = 1000

def main():
    '''
    args = 'ls -lha'

    p = subprocess.Popen(args,shell=True)

    while True:
        p.poll()
    '''
    bot_processes = []

    for bot in bots:
        #args = ['python3', os.getcwd()+'/ai.py',new_ai['login'],new_ai['pass'],wiz.id]
        args = ''
        if system() == 'Windows':
            args = python_path +' C:\\tmp\\ai.py' + ' ' + bots[bot]['login'] + ' ' + bots[bot]['pass'] + ' ' + str(wiz_id)
        elif system() == 'Linux':
            args = 'python3 ai.py' + ' ' + bots[bot]['login'] + ' ' + bots[bot]['pass'] + ' ' + str(wiz_id)
        else:
            assert True, "Unsupported system detected"
        print(args)
        p = subprocess.Popen(args,shell=True)
        bot_processes.append(p)
        time.sleep(1)
    up = True
    while up:
        for bot in bot_processes:
            if bot.poll() != None:
                up = False
        time.sleep(10)

if __name__ == '__main__':
    main()