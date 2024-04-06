"""initial

Revision ID: dd09c59ef9d6
Revises: 
Create Date: 2024-04-04 19:58:19.658228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd09c59ef9d6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('payment_type_online', sa.Boolean(), nullable=False),
    sa.Column('payment_state', sa.Enum('WAITING', 'PAID', 'NOT_PAID', name='paymentstate'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('user_agreement', sa.Boolean(), nullable=False),
    sa.Column('role', sa.Enum('USER', 'ADMIN', 'SUPERADMIN', name='userrole'), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(length=120), nullable=False),
    sa.Column('first_name', sa.String(length=120), nullable=False),
    sa.Column('middle_name', sa.String(length=120), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('note', sa.String(length=120), nullable=False),
    sa.Column('tg_user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(length=20), nullable=False),
    sa.Column('model', sa.String(length=20), nullable=False),
    sa.Column('number', sa.String(length=20), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('car_body_type', sa.Enum('SEDAN', 'COUPE', 'HATCHBACK', 'LIFTBACK', 'FASTBACK', 'STATION_WAGON', 'CROSSOVER', 'OFFROAD', 'PICKUP', 'VAN', 'MINIVAN', 'COMPACT_VAN', 'MICROVAN', 'CONVERTIBLE', 'ROADSTER', 'TARGA', 'LANDAU', 'LIMOUSINE', name='carbodytype'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    op.create_table('visit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('summ', sa.Integer(), nullable=False),
    sa.Column('bonus_payment', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('admin_user_id', sa.Integer(), nullable=False),
    sa.Column('car_number', sa.String(length=20), nullable=False),
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['admin_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['car_number'], ['car.number'], ),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('visit')
    op.drop_table('car')
    op.drop_table('user')
    op.drop_table('payment')
    # ### end Alembic commands ###
