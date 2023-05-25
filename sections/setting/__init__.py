from typing import Any, Dict
from nicegui import ui

class Setting_object():
    pass
    def update(self,data):
        print("update")
        return
class Setting_Model_Descriptor():
    def __init__(self):
        self.name = "AAAA"
        self.lists = []
        return
    def get_objects(self):
        print("get_objects")
        return self.lists
    def get_headers(self):
        print("get_headers")
        return []
    def create(self,data):
        print("create")
        self.lists.append(Setting_object())
        return
    def update(self,data):
        print("update")
        return
    def remove(self,obj):
        self.lists.remove(obj)
def model_factory(model):
    return Setting_Model_Descriptor()

def ui_factory(objects):
    ui.label("this page is for setting")
    dialog_object = {"value":{},"object":None}
    def create() -> None:
        open_dialog(None)
        display_list.refresh()

    ui.button(f'Add new {objects.name}', on_click=create)

    @ui.refreshable
    def display_list():
        for obj in objects.get_objects():
            print(obj)
            with ui.card():
                with ui.row().classes('justify-between w-full'):
                    for obj_desc in objects.get_headers():
                        ui.label(obj[obj_desc])
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
            ui.notify(f'Create new user {new_obj}')
        else:
            dialog_object["object"].update(dialog_object["value"])
            ui.notify(f'Updated user {dialog_object["object"]}')
        dialog.close()
        display_list.refresh()

    with ui.dialog() as dialog:
        with ui.card():
            for obj_desc in objects.get_headers():
                dialog_object["value"][obj_desc]=None
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
        ui.notify(f'Deleted user {obj}')
        display_list.refresh()

    def open_dialog(obj: Dict[str, Any]) -> None:
        print(obj)
        dialog_object["object"]=obj
        # if obj:
        #     for obj_desc in objects["items"]:
        #         dialog_object["value"][obj_desc] = None
        # else:
        #     for obj_desc in objects["items"]:
        #         dialog_object["value"][obj_desc] = None
        dialog.open()

    return





