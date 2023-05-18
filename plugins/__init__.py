import os
import sections

list= {}
total_list = []
base_dir = os.path.abspath(os.path.dirname(__file__))
def init():
    global  list
    global total_list
    for fname in os.listdir(base_dir):
        print(fname)
        if os.path.isdir(os.path.join(base_dir,fname)):
            print(fname , "is directory")
            if os.path.isfile(os.path.join(base_dir,fname,"__init__.py")):
                total_list.append(fname)
                for sname in sections.list:
                    print("check section", sname)
                    if os.path.isfile(os.path.join(base_dir,fname,sname.lower()+".py")):
                        if sname.lower() not in list:
                            list[sname.lower()]=[]
                        list[sname.lower()].append(fname)
                print(fname)
    return
def get_section_plugins(section_name):
    return list[section_name.lower()] if section_name.lower() in list else []

from importlib import import_module

def load_module(module_name):
    module = import_module(module_name)
    return module
def get_content(section_name,plugin_name):
    if os.path.isdir(os.path.join(base_dir, plugin_name)):
        if os.path.isfile(os.path.join(base_dir, plugin_name, "__init__.py")):
            if os.path.isfile(os.path.join(base_dir, plugin_name, section_name.lower() + ".py")):
                load_module(f"plugins.{plugin_name}.{section_name}")
                pass
init()