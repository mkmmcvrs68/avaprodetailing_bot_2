from datetime import datetime

from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.utils.deep_linking import create_start_link
from sqlalchemy.ext.asyncio import AsyncSession

# from bot.db.crud.users_crud import user_crud
from bot.core.constants import (
    PROFILE_MESSAGE_WITH_INLINE, STATE_BIRTH_DATE,
    STATE_FIO, STATE_PHONE_NUMBER, THX_REG,
)
from bot.db.crud.users import users_crud
from bot.db.models.users import User
from bot.keyboards.users_keyboards import (
    add_car_kb, agree_refuse_kb,
    back_menu_kb, profile_kb,
)
from bot.states.user_states import RegUser
from bot.utils.qr_code import generate_qrcode
from bot.utils.validators import (
    validate_birth_date, validate_fio,
    validate_phone_number,
)

router = Router(name=__name__)

profile_message = (
    'ФИО: {last_name} {first_name}\n'
    'Дата рождения: {birth_date}\n'
    'Номер телефона: {phone_number}\n'
    'Бонусы: {bonus}\n'
    '\nДля внесения изменений в информацию - обратитесь к администратору.'
)


# FIXME
@router.callback_query(F.data == 'profile')
async def get_profile(
    callback: CallbackQuery,
    session: AsyncSession,
):
    await callback.message.delete()
    tg_id = callback.from_user.id
    db_obj = await users_crud.get_by_attribute(
        attr_name='tg_user_id',
        attr_value=tg_id,
        session=session
    )
    birth_date = datetime.strftime(db_obj.birth_date, '%d.%m.%Y')
    # car = await
    if db_obj.is_active:
        await callback.message.answer(
            profile_message.format(
                last_name=db_obj.last_name,
                first_name=db_obj.first_name,
                birth_date=birth_date,
                phone_number=db_obj.phone_number,
                bonus=1,
            ),
            reply_markup=back_menu_kb
        )


@router.callback_query(F.data == 'menu')
async def main_user_menu(
    callback: CallbackQuery,
):
    await callback.message.delete()
    await callback.message.answer(
        PROFILE_MESSAGE_WITH_INLINE,
        reply_markup=profile_kb
    )


@router.callback_query(F.data == 'generate_qr_code')
async def generate_qr_code(callback: CallbackQuery, bot: Bot):
    link = await create_start_link(
        bot, str(callback.from_user.id), encode=True
    )

    qrcode = generate_qrcode(link)
    if qrcode is None:
        await callback.message.answer('Произошла ошибка.\nПопробуйте позже')
        return
    await callback.message.answer_photo(
        photo=BufferedInputFile(qrcode, 'qrcode.png'),
    )
