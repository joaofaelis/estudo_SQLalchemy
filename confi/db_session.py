import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker

from pathlib import Path  # Usado no SQLite
from  typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.future.engine import Engine

from models.model_base import ModelBase

__engine: Optional[Engine] = None # ENgine necessario para criar conexão e definir qual banco.

def create_engine(sqlite: bool = False):
    """FUnção  para configurar a conexão com o banco de daddos"""
    global __engine

    if __engine:
        return
    if sqlite:
        arquivo_db = 'db/exemplo.sqlite'
        folder = Path(arquivo_db).parent
        folder.mkdir(parents=True, exist_ok=True)

        conn_str = f'sqlite:///{arquivo_db}'
        __engine = sa.create_engine(url=conn_str, echo=False, connect_args={'check_same_thread': False})

    else:
        conn_str = 'postgresql://user:password@localhost:5432/exemplo'
                    # BD instanciado, após é usuario, senha, local de conexão, porta padrão do postgres, nome do BD.
        __engine = sa.create_engine(url=conn_str, echo=False)

        return __engine

def create_session() -> Session:
    """função criada para criar a sessão com o banco de dados"""
    global __engine
    if not __engine:
        create_engine() #Caso não utilizar o postgress utilizar create_engine(sqlite=True)

    __session = sessionmaker(__engine, expire_on_commit=False, class_=Session)

    session: Session = __session()

    return session



