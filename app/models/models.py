from datetime import datetime
from typing import Annotated 

from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from ..config import sql_file_name, sql_url

connect_args = {"check_same_thread" : False} #Дает возможность использовать БД в нескольких потоках
engine = create_engine(sql_url,connect_args = connect_args)


class Server(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hostname: str = Field(index=True)
    username: str | None = Field(default=None)
    port: int = Field(default=22)
    added_at: datetime = Field(default=datetime.now())
    auth_mode: int = Field(default=0)
    private_key_path: str

def create_db_and_tables():
    '''create database using engine'''
    SQLModel.metadata.create_all(engine)

def get_session():
    '''create one session per request'''
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def get_servers(session: SessionDep) -> list[Server]:
    servers = session.exec(select(Server)).all()
    return servers

def add_server(server: Server, session: SessionDep):
    session.add(server)
    session.commit()
    session.refresh(server)
    return server
 

