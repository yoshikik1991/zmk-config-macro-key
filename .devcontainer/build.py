import yaml, json, os, shutil, subprocess, glob
from datetime import datetime, timezone, timedelta
import argparse

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

def uf2_backup_and_clean(dir):
    timedelta
    tz_offset = os.popen('date +%z').read().strip() 
    hours_offset = int(tz_offset[:3]) 
    minutes_offset = int(tz_offset[0] + tz_offset[3:]) 
    local_tz = timezone(timedelta(hours=hours_offset, minutes=minutes_offset)) 
    now_local = datetime.now(local_tz)
    timestamp = now_local.strftime('%Y%m%d%H%M%S')

    backup_dir = dir + '/backup/' + timestamp

    for p in glob.glob(dir + '/*.uf2', recursive=True):
        mkdir(backup_dir)
        if os.path.isfile(p):
            shutil.move(p, backup_dir)
    


def zmk_build(board, shield, buildOption, releaseDir, zmkConfigPath=None):
    print(board)
    print(shield)
    
    #set variable
    destDir = WORKDIR + '/build/' + board  + '/' + shield

    zmkConfigCommand = ""
    if not zmkConfigPath==None:
        zmkConfigCommand = '-DZMK_CONFIG=' + zmkConfigPath

    if buildOption == None:
        buildOption = ""

    command = 'west build  -d "' + destDir + '" -s zmk/app -b "' + board + '" ' + buildOption + ' -- ' + zmkConfigCommand + ' -DSHIELD="' + shield + '"' 
        
    print(destDir)
    print(releaseDir)
    print(command)

    #prepare dir
    mkdir(destDir)
    mkdir(releaseDir)

    #build
    run_shell_command(command)   

    #copy release dir
    shutil.copy(destDir + '/zephyr/zmk.uf2', releaseDir + '/' + shield + '_' + board + '.uf2')

def main():
    #change current dir
    os.chdir(WORKDIR)
    print(os.getcwd())

    #get args
    parser = argparse.ArgumentParser(description="ZMK Build Script")
    parser.add_argument("--update", action="store_true", help="enable west update")
    args = parser.parse_args()

    #set build mode
    init = not os.path.exists('/workspaces/app/')
    update = args.update

    #west update
    if init or update:
        mkdir('/workspaces/app/')
        shutil.copy(ZMK_CONFG_PATH + '/config/west.yml', '/workspaces/app/')
        if init:
            run_shell_command('west init -l app/')  
        run_shell_command('west update')   
        run_shell_command('west zephyr-export')   
    
    uf2_backup_and_clean(ZMK_CONFG_PATH + '/release')

    #build keyboard by build.yaml
    with open(ZMK_CONFG_PATH + '/build.yaml') as file:
        obj = yaml.safe_load(file)
        #js = json.dumps(obj, indent=2)
        
        for shield in obj["include"]:
            print(shield)
            build_option = None
            if 'snippet' in shield:
                if shield['snippet'] == 'studio-rpc-usb-uart':
                    build_option = '-S studio-rpc-usb-uart'
            zmk_build(shield["board"], shield["shield"], build_option, ZMK_CONFG_PATH + '/release', ZMK_CONFG_PATH + '/config')

if __name__ == '__main__':
    main()
