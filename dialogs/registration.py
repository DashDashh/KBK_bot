# -*- coding: cp1251 -*-
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput

from dialogs.states import MainMenuDL, RegistrationDL

async def go_back_to_main(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuDL.main_menu, mode=StartMode.RESET_STACK)

async def go_to_fio(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(RegistrationDL.fio)

async def go_back_to_info(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(RegistrationDL.info)

async def go_to_confirm(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if dialog_manager.dialog_data.get('fio'):
        await dialog_manager.switch_to(RegistrationDL.confirm)

async def process_fio_input(message: Message, widget: TextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['fio'] = text
    await dialog_manager.switch_to(RegistrationDL.confirm)

async def confirm_and_send(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    fio = dialog_manager.dialog_data.get('fio', 'Не указано')
    
    await callback.message.answer(f"Регистрация завершена! Ваше ФИО: {fio}")
    
    dialog_manager.dialog_data.clear()
    await dialog_manager.start(MainMenuDL.main_menu, mode=StartMode.RESET_STACK)

async def edit_fio(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(RegistrationDL.fio)

async def get_fio_data(dialog_manager: DialogManager, **kwargs):
    fio = dialog_manager.dialog_data.get('fio', 'Не введено')
    return {
        'fio': fio
    }

fio_input = TextInput(
    id='fio_input',
    on_success=process_fio_input,
)

registration_dialog = Dialog(
    Window(
        Const('Сейчас мы пройдём небольшую регистрацию'),
        Row(
            Button(Const('Далее'), id='to_fio', on_click=go_to_fio),
            Button(Const('Отмена'), id='back_main_menu', on_click=go_back_to_main)
        ),
        state=RegistrationDL.info,
    ),
    Window(
        Const('Введите своё ФИО:'),
        fio_input,
        Row(
            Button(Const('Отмена'), id='back_info', on_click=go_back_to_info)
        ),
        state=RegistrationDL.fio,
    ),
    Window(
        Format('Ваше ФИО: {fio}\nВерно?'),
        Row(
            Button(Const('Подтвердить и отправить'), id='conf_fio', on_click=confirm_and_send),
            Button(Const('Изменить'), id='edit_fio', on_click=edit_fio),
            Button(Const('Отмена'), id='back_main', on_click=go_back_to_main)
        ),
        state=RegistrationDL.confirm,
        getter=get_fio_data 
    )
)