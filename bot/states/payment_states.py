from aiogram.fsm.state import StatesGroup, State


class PaymentProcess(StatesGroup):
    amount = State()
    payment_type = State()
