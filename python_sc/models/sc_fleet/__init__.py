import sqlalchemy

from sqlalchemy import Column,Integer,VARCHAR,ForeignKey,TIMESTAMP
from database.main import session, Base
from sqlalchemy.orm import relationship

class SC_FLEET(Base):

    __tablename__ = 'sc_fleet'

    sc_guid = Column(Integer,ForeignKey('sc_global.sc_guid'),primary_key=True)  
    sc_global = relationship('SC_GLOBAL', back_populates = 'sc_global_fleet')

    sc_type = Column(VARCHAR(45))
    sc_name = Column(VARCHAR(45))
    sc_start_time = Column(TIMESTAMP)
    sc_end_time = Column(TIMESTAMP)

    sc_source = Column(VARCHAR(45))
    sc_destination = Column(VARCHAR(45))