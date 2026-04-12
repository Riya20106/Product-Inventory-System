from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:Riya2006!@localhost:5432/project1" ; 
engine = create_engine(db_url) 
sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine) 