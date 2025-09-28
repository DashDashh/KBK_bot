from aiogram.filters.state import State, StatesGroup
class MainMenuDL(StatesGroup):
    main_menu = State()
    support = State()

class RegistrationDL(StatesGroup):
    info = State()
    fio = State()
    confirm = State()
