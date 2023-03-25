# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from decouple import config
# from sqlalchemy.ext.declarative import declarative_base


# """ Setting up datebase using sqlachemy
# """


# DEVELOPMENT = config("DEVELOPMENT")
# SQLALCHEMY_DATABASE_URL = ""
# engine = ""

# Base = declarative_base()
# if (DEVELOPMENT == 'production'):
#     SQLALCHEMY_DATABASE_URL = 'mysql+mysqldb://{}:{}@{}/{}'.format(config("ADMIN_MYSQL_USER"),
#                                                                    config("ADMIN_MYSQL_PWD"),
#                                                                    config("ADMIN_MYSQL_HOST"),
#                                                                    config("ADMIN_MYSQL_DB"))

#     engine = create_engine(SQLALCHEMY_DATABASE_URL)
# else:
#     SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
#     engine = create_engine(SQLALCHEMY_DATABASE_URL,
#                            connect_args={"check_same_thread": False})


# Base.metadata.create_all(bind=engine)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




# db = SessionLocal()
