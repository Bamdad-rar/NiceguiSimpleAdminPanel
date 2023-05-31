from typing import Any, Dict
from nicegui import ui
import uuid


class Setting_object():
    def __init__(self,headers,data = None):
        self.headers = headers
        print("new object ",data)
        self._data = data
        pass
    def update(self,data):
        print("update",data)
        return
    def to_card(self,headers):
        print("to_card",headers)
        itr = iter(self._data)
        for h in headers:
            ui.label(h.get_name())
            ui.label(next(itr))

    def load_edit(self,edit_items):
        itr = iter(self._data)
        for h in self.headers:
            print(h)
            edit_items[h.id].value=next(itr)
        return

    def __str__(self):
        o1 = []
        itr = iter(self._data)
        for h in self.headers:
            print(h)
            o1.append("%s : %s"%(h.get_name(),next(itr)))
        return "[%s]"%",".join(o1)
class Setting_Header():
    def __init__(self,name,description):
        print(name,description)
        self._name = name
        self._desc = description
        self.id = uuid.uuid4().hex
    def to_edit_primary_key(self):
        i = ui.input()
        i.set_visibility(False)
        return i
    def to_edit_string(self):
        return ui.input(self._name)
    def to_edit_enum(self):
        s1 = ui.select(self._desc["values"])
        return s1
    def to_edit_number(self):
        return ui.number(self._name)
    def get_name(self):
        return self._name

    def to_edit_item(self):
        tmp_name = "to_edit_"+self._desc["type"]
        if hasattr(self,tmp_name):
            return getattr(self,tmp_name)()

        return ui.label(f"?{tmp_name}")
class Setting_Model_Descriptor():
    def __init__(self,name,headers):
        self.name = name
        self.headers = headers
        self.lists = []
        return
    def get_objects(self):
        print("get_objects")
        return self.lists
    def get_headers(self):
        print("get_headers")
        return self.headers
    def create(self,data):
        print("create",data)
        new_data = []
        for h in self.headers:
            print(h,h.id,data[h.id])
            new_data.append(data[h.id].value)
        new_obj = Setting_object(self.get_headers(),new_data)
        self.lists.append(new_obj)
        return new_obj

    def remove(self,obj):
        self.lists.remove(obj)
    def set_new(self,edit_items):
        for h in self.headers:
            edit_items[h.id].value= None
def model_factory(model):
    headers = []
    for h in model["items"]:
        print(h,model["items"][h])
        headers .append(Setting_Header(h,model["items"][h]))
    return Setting_Model_Descriptor(model["model_name"],headers)


def ui_factory(objects):
    ui.label("this page is for setting")
    factory_name = objects.name
    dialog_object = {"value":{},"object":None}

    def create() -> None:
        open_dialog(None)
        display_list.refresh()

    ui.button(f'Add new {factory_name}', on_click=create)

    @ui.refreshable
    def display_list():
        for obj in objects.get_objects():
            print(obj)
            with ui.card():
                with ui.row().classes('justify-between w-full'):
                    obj.to_card(objects.get_headers())
                with ui.row():
                    ui.button('edit', on_click=lambda _, obj=obj: open_dialog(obj))
                    ui.button('delete', on_click=lambda _, obj=obj: delete(obj), color='red')
    display_list()
    def update() -> None:
        # max_id = objects[0][0] if len(objects) > 0 else 0
        # print("H",objects,dialog_object["value"])
        # dialog_id = dialog_object["value"]["id"]
        # for itm in objects:
        #     print("V",itm)
        #     if itm[0] > max_id:
        #         max_id = itm[0]
        #     if  itm[0] == dialog_id:
        #         itm[1] = dialog_object["value"]["name"].value
        #         itm[2] = dialog_object["value"]["age"].value
        if dialog_object["object"] is None:
            new_obj = objects.create(dialog_object["value"])
            ui.notify(f'Create new {factory_name} {new_obj}')
        else:
            dialog_object["object"].update(dialog_object["value"])
            ui.notify(f'Updated {factory_name} {dialog_object["object"]}')
        dialog.close()
        display_list.refresh()

    with ui.dialog() as dialog:
        with ui.card():
            for obj_desc in objects.get_headers():
                dialog_object["value"][obj_desc.id]=obj_desc.to_edit_item()
            # dialog_object["value"]["id"] = None
            # dialog_object["value"]["name"] = ui.input('Name')
            # dialog_object["value"]["age"] = ui.number('Age', format='%.0f')
            # dialog_name = ui.input('Name')
            # dialog_age = ui.number('Age', format='%.0f')
            with ui.row():
                ui.button('Save', on_click=update)
                ui.button('Close', on_click=dialog.close).props('outline')


    def delete(obj: Dict[str, Any]) -> None:
        objects.remove(obj)
        ui.notify(f'Deleted {factory_name} {obj}')
        display_list.refresh()

    def open_dialog(obj: Dict[str, Any]) -> None:
        print(obj)
        dialog_object["object"]=obj
        if obj:
            obj.load_edit(dialog_object["value"])
        else:
            objects.set_new(dialog_object["value"])
        dialog.open()

    return





