import os
import sections

list= {}
total_list = []
base_dir = os.path.abspath(os.path.dirname(__file__))
def init():
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
init()