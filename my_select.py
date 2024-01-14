from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from main import students, grades


engine = create_engine("sqlite:///university.db", echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()


print(session.query(students.fullname, func.round(func.avg(grades.grade), 2).label('avg_grade')).select_from(grades).join(students).group_by(students.id)).order_by(desc('avg_grade')).limit(5).all