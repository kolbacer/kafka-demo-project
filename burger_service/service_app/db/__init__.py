import logging
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "sqlite:////code/dbpath/burger_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
import service_app.db.models as models
Base.metadata.create_all(engine)

session = SessionLocal()
log.debug('Database session started')

Burger = models.Burger
Order = models.Order


async def get_burgers() -> List[Burger]:
    return session.query(Burger).all()


async def get_burger_by_name(name: str) -> Burger:
    return session.query(Burger).filter_by(name=name).first()


async def add_burger(burger_name: str, burger_price: float) -> bool:
    if await get_burger_by_name(burger_name) is not None:
        log.info(f'Burger "{burger_name}" already exists')
        return False

    burger = Burger(
        name=burger_name,
        price=burger_price,
        owner=None
    )
    session.add(burger)
    session.commit()
    log.info(f'Burger "{burger_name}" was added')
    return True


async def set_burger_owner(burger_name: str, customer_name: str):
    session.query(Burger).filter_by(name=burger_name).update({'owner': customer_name})
    session.commit()
    log.info(f'{customer_name} now owns "{burger_name}" burger')


async def get_orders() -> List[Order]:
    return session.query(Order).all()


async def add_order(burger_name: str, customer_name: str):
    burger = await get_burger_by_name(burger_name)
    order = Order(
        burger_id=burger.id,
        burger_name=burger_name,
        customer_name=customer_name
    )
    session.add(order)
    session.commit()
    log.info(f'{customer_name}\'s order for "{burger_name}" burger was added')
