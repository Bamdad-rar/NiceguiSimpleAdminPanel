#!/usr/bin/env python3
'''This is only a very simple authentication example which stores session IDs in memory and does not do any password hashing.

Please see the `OAuth2 example at FastAPI <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>`_  or
use the great `Authlib package <https://docs.authlib.org/en/v0.13/client/starlette.html#using-fastapi>`_ to implement a real authentication system.

Here we just demonstrate the NiceGUI integration.
'''

import os
import uuid
from typing import Dict

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from nicegui import app, ui

# put your your own secret key in an environment variable MY_SECRET_KEY
app.add_middleware(SessionMiddleware, secret_key=os.environ.get('MY_SECRET_KEY', ''))

# in reality users and session_info would be persistent (e.g. database, file, ...) and passwords obviously hashed
users = [('system', 'sys'), ('user2', 'pass2')]
session_info: Dict[str, Dict] = {}


def is_authenticated(request: Request) -> bool:
    return session_info.get(request.session.get('id'), {}).get('authenticated', False)

tab_names = ['A', 'B', 'C']
@ui.page('/')
def main_page(request: Request) -> None:
    if not is_authenticated(request):
        return RedirectResponse('/login')
    session = session_info[request.session['id']]

    def switch_tab(msg: Dict) -> None:
        name = msg['args']
        tabs.props(f'model-value={name}')
        panels.props(f'model-value={name}')
    with ui.header().classes(replace='row items-center') as header:
        ui.button(on_click=lambda: left_drawer.toggle()).props('flat color=white icon=menu')

    # with ui.column().classes('absolute-center items-center'):
        ui.label(f'Hello {session["username"]}!').classes('text-2xl')
        # NOTE we navigate to a new page here to be able to modify the session cookie (it is only editable while a request is en-route)
        # see https://github.com/zauberzeug/nicegui/issues/527 for more details
        ui.button('', on_click=lambda: ui.open('/logout')).props('outline round color=red icon=logout')


    with ui.footer(value=False) as footer:
        ui.label('Footer')

    with ui.left_drawer().classes('bg-blue-100') as left_drawer:
        ui.label('Side menu')

        with ui.element('q-tabs').on('update:model-value', switch_tab) as tabs:
            for name in tab_names:
                # ui.button(f'Tab {name}', on_click=lambda: switch_tab({"args":name}))
                with ui.element('div').classes('p-2 bg-green-100'):
                    ui.element('q-tab').props(f'name={name} div label={name}')
    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        ui.button(on_click=footer.toggle).props('fab icon=contact_support')

    # the page content consists of multiple tab panels
    with ui.element('q-tab-panels').props('model-value=A animated').classes('w-full') as panels:
        for name in tab_names:
            with ui.element('q-tab-panel').props(f'name={name}').classes('w-full'):
                ui.label(f'Content of {name}')









@ui.page('/login')
def login(request: Request) -> None:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if (username.value, password.value) in users:
            session_info[request.session['id']] = {'username': username.value, 'authenticated': True}
            ui.open('/')
        else:
            ui.notify('Wrong username or password', color='negative')

    if is_authenticated(request):
        return RedirectResponse('/')
    request.session['id'] = str(uuid.uuid4())  # NOTE this stores a new session ID in the cookie of the client
    with ui.card().classes('absolute-center'):
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password').props('type=password').on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)


@ui.page('/logout')
def logout(request: Request) -> None:
    if is_authenticated(request):
        session_info.pop(request.session['id'])
        request.session['id'] = None
        return RedirectResponse('/login')
    return RedirectResponse('/')


ui.run()