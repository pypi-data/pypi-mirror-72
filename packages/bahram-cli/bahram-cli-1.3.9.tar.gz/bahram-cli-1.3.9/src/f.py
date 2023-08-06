#!/usr/bin/env python3
from __future__ import print_function, unicode_literals
import requests
from PyInquirer import prompt, print_json, Separator
import fire
import time
from random import randint
from yaspin import yaspin
from yaspin.spinners import Spinners

import filecmp
import glob
import os
import shutil
import zipfile
import requests
current_path = os.getcwd()
def recursive_copy_files(source_path, destination_path, override=False):
    """
    Recursive copies files from source  to destination directory.
    :param source_path: source directory
    :param destination_path: destination directory
    :param override if True all files will be overridden otherwise skip if file exist
    :return: count of copied files
    """
    files_count = 0
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
    items = glob.glob(source_path + '/*')
    for item in items:
        if os.path.isdir(item):
            path = os.path.join(destination_path, item.split('/')[-1])
            files_count += recursive_copy_files(source_path=item, destination_path=path, override=override)
        else:
            file = os.path.join(destination_path, item.split('/')[-1])
            if not os.path.exists(file) or override:
                shutil.copyfile(item, file)
                files_count += 1
    return files_count


def fix_git_ignore():
    flag = False
    if os.path.exists(current_path + '/.git'):
        try:
            with open(current_path + '.gitignore', "a") as my_file:
                my_file.write("/.cloud")
                my_file.write("/.cloud/")
            flag = True

        except IOError:
            flag = False
            raise Exception("permission denied")
    return flag
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
def init():
    flag = False
    if os.path.exists(current_path+'/.cloud'):
        flag = True
    else:
        try:
            os.makedirs(current_path+'/.cloud')
            os.makedirs(current_path+'/.cloud/prev')
            with open(current_path+'/.cloud/commit', 'w') as commit:
                commit.write('0')
            flag = True
            recursive_copy_files(current_path, current_path + '/.cloud/prev')

            fix_git_ignore()
        except Exception:
            flag = False
            raise Exception("Permission denied")
    return flag

def comparison(current_path, prev_path):
    comparison = filecmp.dircmp(current_path, prev_path)
    common_files = ', '.join(comparison.common)
    right_files = ', '.join(comparison.right_only)
    left_files = ', '.join(comparison.left_only)
    data = {
        'common_files': common_files,
        'right_files': right_files,
        'left_files': left_files,
    }
    return data

def copy_from_left(left_files):
    ignored_files = ['.idea', '.cloud', '.gitignore', '.pws']
    # print(left_files)
    left_files = left_files.replace(".idea,", "")
    left_files = left_files.replace(".pws,", "")
    left_files = left_files.replace(".cloud,", "")
    left_files = left_files.replace(".gitignore,", "")
    # left_files = left_files
    # print(left_files)
    left_files = left_files.split(', ')
    for i in left_files:
        # print(i == '.idea')
        # print(i in ignored_files)
        # print(i)
        if i in ignored_files:
            # print(i.__key__)
            left_files.remove(i)

    # print(left_files)
    for i in left_files:
       # print(i)
       if os.path.isdir(i) and '.pws' not in i:
            shutil.copytree(current_path + '/' + i, current_path + '/.cloud/prev/' + i)
       else:
            if '.pws' not in i:
                # print("iiiiiiii")
                shutil.copy(current_path+'/'+i, current_path+'/.cloud/prev/'+i)
    pass
def check_internet_work():
    with yaspin(Spinners.earth, text="Checking Internet Connection...", color="cyan") as sp:
        try:
            r = requests.get('http://49.12.101.190/')
            if r.status_code == 200:
                result = True
            else:
                result = False
        except:
            result = False

    return result


class ParsPaas(object):
    """cutest cli ever!."""

    def deploy(self):
        if check_internet_work() is not True:
            print("you are not connected to internet yet")
            exit()
        with yaspin(Spinners.earth, text="Fetching Your Apps List", color="cyan") as sp:
            with open(current_path + '/.cloud/a4e1daa4f02f756b865ce2f9a9f9b689', 'r') as commit:
                tokenx= commit.read()
            headers = {"Authorization": "Bearer "+tokenx}

            r = requests.get('http://49.12.101.190/api/apps/',headers=headers)
            print(r.text)
            rr = r.status_code
        # liste= ['MyNodeApp1','MyDjangoApp1','MyNodeApp2']
        liste= r.json()
        liste= liste['apps']
        apps = [
            {
                'type': 'list',
                'name': 'app',
                'message': 'Please Choose the App You want to deploy on it ',
                'choices': [
                    *liste,
                    Separator(),
                    'Contact support',


                ]
            }
        ]
        apps = prompt(apps)





        with yaspin(text="Deploying the "+apps['app']+' ...', color="cyan") as sp:
            # task 1
            time.sleep(1)
            sp.write("> Compressing Files")
            init()
            x = comparison(current_path, current_path + '/.cloud/prev')

            # print(x)
            copy_from_left(x['left_files'])
            x = comparison(current_path, current_path + '/.cloud/prev')
            if os.path.isfile(current_path + '/.cloud/Python.zip'):
                os.remove(current_path + '/.cloud/Python.zip')
            shutil.make_archive(current_path + '/.cloud/Python', 'zip', current_path + '/.cloud/prev')
            headersx = {"Authorization": "Bearer "+tokenx}

            url = 'http://49.12.101.190/api/deploy/'

            files = {'file': open(current_path + '/.cloud/Python.zip', 'rb')}
            values = {'user_id': '1', 'user_token': 'x', 'app_id': '2'}

            r = requests.post(url, files=files, data=values,headers=headersx)
            print(r.text)
            # task 2
            time.sleep(2)
            sp.write("> Compressing Files")

            # finalize
            sp.ok("✔")

        # return apps['app']
        return apps['app']+ "successfully Deployed "

    def login(self):
        if check_internet_work() is not True:
            print("you are not connected to internet yet")
            exit()

        credentials = [
            {
                'type': 'input',
                'name': 'username',
                'message': 'Please enter your username > ',

            },
            {
                'type': 'password',
                'name': 'password',
                'message': 'Please enter your password > ',

            },

        ]
        credentials = prompt(credentials)
        username = credentials['username']
        password = credentials['password']
        data = { 'username': username, 'password': password}
        r = requests.post('http://49.12.101.190/api/auth/login/', data=data)
        x=r.json()
        try:
            if x['access'] is not None:
                init()
                with open(current_path + '/.cloud/a4e1daa4f02f756b865ce2f9a9f9b689', 'w') as commit:
                    commit.write(x['access'])
                result = "successfully logged in"
            else:
                result =  "access denied"
        except:
            result =   "access denied"
        # print(x['access'])

        # print(r.status_code)
        # print(r.encoding)
        # print(r.headers)
        # print(r.headers['content-type'])

        return result
    def logout(self):
        if check_internet_work() is not True:
            print("you are not connected to internet yet")
            exit()

        try:
            myf = current_path + '/.cloud/a4e1daa4f02f756b865ce2f9a9f9b689'
            os.remove(myf)
            result = "successfully logged out"
        except:
            result = "access denied"

        return result
    def help(self):

        return "result"


if __name__ == '__main__':
    fire.Fire(ParsPaas)
