from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlmodel import Session, SQLModel, create_engine

DB_URL = "sqlite:///./test.db"
ASYNC_DB_URL = "sqlite+aiosqlite:///./test.db"

engine = create_engine(DB_URL, echo=True)
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)

def get_session():
    """Get synchronous DB session."""
    with Session(engine) as session:
        yield session


async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    """Get asynchronous DB session."""
    async with async_session() as session:
        yield session


def init_database():
    """Initialize DB schema and tables."""
    SQLModel.metadata.create_all(engine)