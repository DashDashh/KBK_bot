# -*- coding: cp1251 -*-
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import State, StatesGroup
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.media import StaticMedia
from dialogs.registration import RegistrationDL

from dialogs.states import MainMenuDL
from dialogs.states import RegistrationDL

rt = Router()

async def go_to_support(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainMenuDL.support)

async def go_back_to_main(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainMenuDL.main_menu)

async def go_to_registration(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(RegistrationDL.info, mode=StartMode.RESET_STACK)

main_menu_dialog = Dialog(
    Window(
        StaticMedia(path="igraushii-kotenok_1920x1200.jpg", type='photo'),
        Const('Главное меню'),
        Row(
            Button(Const('Регистрация'), id='reg', on_click=go_to_registration),
            Button(Const('Поддержка'), id='support', on_click=go_to_support)
        ),
        state=MainMenuDL.main_menu,
    ),
    Window(
        Const('Наша служба поддержки: example@mail.com'), 
        Button(Const('Назад'), id='back_main_menu', on_click=go_back_to_main),
        state=MainMenuDL.support
    )
)

@rt.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuDL.main_menu, mode=StartMode.RESET_STACK)