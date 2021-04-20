import os
from shutil import rmtree

def ensure_dir(path):
    if(not os.path.exists(path)):
        os.makedirs(path)


def label_save(path, data):
    with open(path, 'w') as f:
        for i in data:
            f.write(str(i) + '\n')


def edge_save(path, data):
    with open(path, 'w') as f:
        for i in data:
            f.write(str(i[0]) + ', ' + str(i[1]) + '\n')


def rmdir(path):
    try:
        rmtree(path)
    except:
        pass


def rmfile(path):
    try:
        remove(path)
    except:
        pass


def find_file(dir):
    files = listdir(dir)
    for file in files:
        if(file[:3] == 'out'):
            file = dir + file
            return file
    print('not found datas!')
    return 'None'


def listdir(path):
    return os.listdir(path)


def makedirs(path):
    os.makedirs(path)


def exists(path):
    return os.path.exists(path)
