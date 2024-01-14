from sqlalchemy import create_engine, MetaData, Table, Column, Integer, ForeignKey, String, Date
from sqlalchemy.sql import select
import faker
from random import randint, choice
import datetime


STUDENTS_COUNT = 32
GROUPS = ["601-TT", "601-ME", "602-MM"]
DISCIPLINES = [
    "ІВНБ",
    "Теорія електричних і магнітних кіл",
    "Волоконно - оптичні лінії зв'язку",
    "Комп'ютерні мережі",
    "Технічна електродинаміка",
    "Схемотехніка"
]
TEACHERS_COUNT = 4
COUNTER = 20
fake_data = faker.Faker("uk-UA")



engine = create_engine("sqlite:///university.db", echo=True)

metadata = MetaData()

disciplines = Table("disciplines", metadata,
                    Column("id", Integer, primary_key=True, autoincrement=True),
                    Column("name", String, unique=True),
                    Column("teacher_id", Integer, ForeignKey("teachers.id")),
                    )

grades = Table("grades", metadata,
               Column("id", Integer, primary_key=True, autoincrement=True),
               Column("student_id", Integer, ForeignKey("students.id")),
               Column("disciplines_id", Integer, ForeignKey("disciplines.id")),
               Column("date_of", Date),
               Column("grade", Integer))

groups = Table("groups", metadata,
               Column("id", Integer, primary_key=True, autoincrement=True),
               Column("name", String, unique=True))

students = Table("students", metadata,
                Column("id", Integer, primary_key=True, autoincrement=True),
                Column("fullname", String, unique=True),
                Column("group_id", Integer, ForeignKey("groups.id")))

teachers = Table("teachers", metadata,
                Column("id", Integer, primary_key=True, autoincrement=True),
                Column("fullname", String, unique=True, nullable=False))

metadata.create_all(engine)

with engine.connect() as connection:
    for i in GROUPS:
        connection.execute(groups.insert().values(name = i))
    s = select(groups)
    res = connection.execute(s)
    # for i in res:
    #     print(i)

    for i in range(STUDENTS_COUNT):
        connection.execute(students.insert().values(fullname = fake_data.name(), group_id = randint(1, len(GROUPS))))
        s = select(students)
        res = connection.execute(s)
        # for i in res:
        #     print(i)
    for i in range(TEACHERS_COUNT):
        connection.execute(teachers.insert().values(fullname = fake_data.name()))
        s = select(teachers)
        res = connection.execute(s)

    for i in DISCIPLINES:
        connection.execute(disciplines.insert().values(name = i, teacher_id = randint(1, TEACHERS_COUNT)))
        

    for i in range(STUDENTS_COUNT * len(DISCIPLINES)):
        connection.execute(grades.insert().values(student_id = randint(1, STUDENTS_COUNT), 
                                                  disciplines_id = randint(1, len(DISCIPLINES)), 
                                                  date_of = datetime.date.today(),
                                                  grade = randint(1, 100)))
        s = select(grades)
        res = connection.execute(s)
        for i in res:
            print(i)
    
    connection.commit()