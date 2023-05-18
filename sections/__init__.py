import os
list = []
base_dir = os.path.abspath(os.path.dirname(__file__))

def init():
    global list
    for fname in os.listdir(base_dir):
        if os.path.isdir(os.path.join(base_dir,fname)):
            if os.path.isfile(os.path.join(base_dir,fname,"__init__.py")):
                list.append(fname)
    return
init()