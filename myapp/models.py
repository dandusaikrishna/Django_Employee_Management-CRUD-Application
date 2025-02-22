# models.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from django.db import models



# Define the database URL
DATABASE_URL = "mysql+mysqlconnector://root:pass@localhost/newversion"

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(100), nullable=False)
    employees = relationship("Employee", back_populates="department")

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'))
    employee_salary = Column(Integer)
    department = relationship("Department", back_populates="employees")

Base.metadata.create_all(engine)

# Session function
def get_session():
    Session = sessionmaker(bind=engine)
    return Session()


class DjangoUser(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    age = models.IntegerField()



