from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import time




# Create a engine to our database
engine = create_engine('sqlite:///test.db')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()

# Define a class that inherits from Base and represents our table
class Runner(Base):
    __tablename__ = 'runners'
    
    id = Column(Integer, primary_key=True)
    pool = Column(String)
    updated = Column(DateTime)

    def __repr__(self):
        return f"Runner(id={self.id}, pool='{self.pool}', updated='{self.updated}')"
    

def create_runner(pool):
    session = Session()
    try:
        runner = Runner(pool=pool, updated=datetime.now())
        session.add(runner)
        session.commit()
        print(f"Created runner with pool {pool}")
        return runner
    finally:
        session.close()

def get_runner(pool):
    session = Session()
    try:
        runner = session.query(Runner).filter_by(pool=pool).first()
        return runner
    finally:
        session.close()

def get_main_runner():
    session = Session()
    try:
        runner = session.query(Runner).filter_by(id=1).first()
        if runner is None:
            runner = create_runner("A") # use pool A as default
        return runner
    finally:
        session.close()

def update_runner(runner, pool):
    session = Session()
    try:
        runner.pool = pool
        runner.updated = datetime.now()
        session.add(runner)
        session.commit()
    finally:
        session.close()

def check_or_change_runner(pool_instance, pool_time_limit):
    runner = get_main_runner()

    current_pool = runner.pool
    runner_updated = runner.updated
    now = datetime.now()
    delta = now - runner_updated

    if current_pool != pool_instance and delta.total_seconds() > pool_time_limit:
        update_runner(runner, pool_instance)
        print(f"Changed runner to {pool_instance}")
        return True
    if current_pool != pool_instance and delta.total_seconds() <= pool_time_limit:
        print(f"Other runner is still alive")
        return False
    if current_pool == pool_instance:
        print(f"Runner is already {pool_instance}")
        update_runner(runner, pool_instance)
        return True

# Create all tables in the engine
Base.metadata.create_all(engine)