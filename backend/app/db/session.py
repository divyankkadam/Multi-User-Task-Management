from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker , AsyncSession
from sqlalchemy.orm import DeclarativeBase 

DATABASE_URL = "postgresql+asyncpg://divyank:divyank123@127.0.0.1:5432/todo_db"

# Create Async Engine 
engine = create_async_engine(
    DATABASE_URL,
    echo=False,              # Set to True to print raw SQL statements during debug
    pool_pre_ping=True,      # Tests connections before handing them out
    pool_size=10,            # Max persistent connections (Postgres only)
    max_overflow=20          # Extra surge connections allowed
)

# Async Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevents lazy-loading errors after commit
    autoflush=False
)


class Base(DeclarativeBase):
    pass

