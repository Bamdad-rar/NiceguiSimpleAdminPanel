from typing import Any, Dict
from nicegui import ui



def ui_factory(objects):
    ui.label("this page is for setting")
    dialog_object = {"value":{}}
    def create() -> None:
        open_dialog(None)
        display_list.refresh()

    ui.button('Add new user', on_click=create)

    @ui.refreshable
    def display_list():
        for row in objects:
            user = {'id': row[0], 'name': row[1], 'age': row[2]}
            print(user)
            with ui.card():
                with ui.row().classes('justify-between w-full'):
                    ui.label(user['id'])
                    ui.label(user['name'])
                    ui.label(user['age'])
                with ui.row():
                    ui.button('edit', on_click=lambda _, user=user: open_dialog(user))
                    ui.button('delete', on_click=lambda _, user=user: delete(user), color='red')
    display_list()
    def update() -> None:
        max_id = objects[0][0] if len(objects) > 0 else 0
        print("H",objects,dialog_object["value"])
        dialog_id = dialog_object["value"]["id"]
        for itm in objects:
            print("V",itm)
            if itm[0] > max_id:
                max_id = itm[0]
            if  itm[0] == dialog_id:
                itm[1] = dialog_object["value"]["name"].value
                itm[2] = dialog_object["value"]["age"].value
        if dialog_id is None:
            objects.append([max_id + 1, dialog_object["value"]["name"].value, dialog_object["value"]["age"].value])
            ui.notify(f'Create new user {dialog_object["value"]["name"].value}')
        else:
            ui.notify(f'Updated user {dialog_object["value"]["name"].value}')
        dialog.close()
        display_list.refresh()

    with ui.dialog() as dialog:
        with ui.card():
            dialog_object["value"]["id"] = None
            dialog_object["value"]["name"] = ui.input('Name')
            dialog_object["value"]["age"] = ui.number('Age', format='%.0f')
            # dialog_name = ui.input('Name')
            # dialog_age = ui.number('Age', format='%.0f')
            with ui.row():
                ui.button('Save', on_click=update)
                ui.button('Close', on_click=dialog.close).props('outline')


    def delete(user: Dict[str, Any]) -> None:
        ind1 = False
        for itm in objects:
            if user['id'] == itm[0]:
                ind1 = itm
        objects.remove(ind1)
        ui.notify(f'Deleted user {user["name"]}')
        display_list.refresh()

    def open_dialog(user: Dict[str, Any]) -> None:
        print(user)
        if user:
            dialog_object["value"]["id"]=user["id"]
            dialog_object["value"]["name"].value=user["name"]
            dialog_object["value"]["age"].value=user["age"]
        else:
            dialog_object["value"]["id"]=None
            dialog_object["value"]["name"].value=""
            dialog_object["value"]["age"].value=0
        dialog.open()

    return





