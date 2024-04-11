import re
from datetime import date, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import MAX_LENGTH_BIRTH_DATE
from bot.db.crud.users_crud import user_crud
from bot.core.enums import UserRole


async def check_user_exists(
    tg_id: int,
    session: AsyncSession,
) -> None:
    user = await user_crud.get(
        tg_user_id=tg_id, session=session
    )
    if user is not None:
        return False
    return True


async def check_user_is_admin(
    tg_id: int,
    session: AsyncSession,
) -> None:
    user = await user_crud.get(
        user_id=tg_id, session=session
    )
    if user.role is UserRole.ADMIN:
        return True
    return False


async def validate_fio(msg: str):
    check = '^[А-ЯЁ]([а-я]*)\s[А-ЯЁ]([а-я]*)\s[А-ЯЁ]([а-я]*)'
    match = re.match(check, msg)
    if match is not None:
        return True
    return False


async def validate_birth_date(msg: str):
    check = '^(([1][0-9])|([2][0-9])|([3][0-1])|([1-9]))\.(([0][1-9])|([1][1-2])|[1-9])\.[1-2]([0-9]..)'
    current_date = date.today()
    match = re.match(check, msg)
    if match is not None and len(msg) < MAX_LENGTH_BIRTH_DATE:
        birth_date = datetime.strptime(msg, '%d.%m.%Y').date()
        if (
            (current_date > birth_date) and 
            (birth_date.year in range(current_date.year-100,current_date.year-16))
        ):
            return True
        return False
    return False


async def validate_phone_number(msg: str):
    check = '\+([0-9]*)'
    match = re.match(check, msg)
    if match is not None:
        return True
    return False



