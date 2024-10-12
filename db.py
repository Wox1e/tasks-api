from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from hashing import sha256
from jwt_tokens import decode_jwt
from config import DB_URI



#for DB_URI
#postgresql:// - correct 
#postgres:// - not correct



Base = declarative_base()
db = DB_URI
engine = create_engine(db)



Session = sessionmaker(bind=engine)
session = Session()



class AbstractClass():
    def addToDB(self):
        """
        Adds object instance into DB
        """
        session.add(self)
        session.commit()



class User(Base, AbstractClass):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    def __repr__(self):
        return f"User {self.id}"


    def __init__(self, username, password):
        self.username = username
        self.password = sha256(password)

    @staticmethod
    def check_credentials(username:str, password:str) -> bool:
        """
        Returns true if credentials are correct \n
        Returns false if not
        """
        user = session.query(User).filter_by(username = username).first()
        
        if not user: return False
        
        return user.password == sha256(password)
    
    @staticmethod
    def check_token(token:str) -> int:
        ''' Returns id if correct \n
            Returns -1 if not
        '''
        
        body = decode_jwt(token)
        username = body["username"]
        password = body["password"]

        if not User.check_credentials(username, password):
            return -1
        
        user = session.query(User).filter_by(username = username).first()
        return user.id

    
    def addToDB(self):
        session.add(self)
        session.commit()


class Task(Base, AbstractClass):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(128))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Task {self.id} | User {self.user_id}"

    def __init__(self, user_id:int, description:str):
        self.user_id = user_id
        self.description = description





if not inspect(engine).has_table("user"):
    Base.metadata.create_all(engine)

