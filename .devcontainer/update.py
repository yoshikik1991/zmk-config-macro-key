import os, shutil, subprocess

#ENV Variable
WORKDIR = '/workspaces'
ZMK_CONFG_PATH = '/workspaces/zmk-config'


def run_shell_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    while True:
        output = process.stdout.readline().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

def mkdir(dir):
    if not os.path.exists(dir): 
        os.makedirs(dir)

def rm(dir):
    if os.path.exists(dir): 
        shutil.rmtree(dir)   

def main():
    #change current dir
    os.chdir(WORKDIR)
    print(os.getcwd())

    #west update
    mkdir('/workspaces/app/')
    shutil.copy(ZMK_CONFG_PATH + '/config/west.yml', '/workspaces/app/')
    run_shell_command('west update')   
    run_shell_command('west zephyr-export')   

if __name__ == '__main__':
    main()
