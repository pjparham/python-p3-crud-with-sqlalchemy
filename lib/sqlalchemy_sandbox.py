#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"


if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    # use our engine to configure a 'Session' class
    Session = sessionmaker(bind=engine)
    # use 'Session' class to create 'session' object
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()
    #query to show all students
    students = session.query(Student).all()
    #query to show all student's names
    names = session.query(Student.name).all()
    #query to show all student's name in alphabetical order
    students_by_name = session.query(
        Student.name).order_by(
        Student.name).all()
    #query to show limits
    oldest_student = session.query(
        Student.name, Student.birthday).order_by(
        desc(Student.grade)).limit(1).all()
    #other query to show limits
    other_oldest_student = session.query(
        Student.name, Student.birthday).order_by(
        desc(Student.grade)).first()
    #func gives us acccess to commong SQL operations that act upon columns
    #we call these with the syntax fun.operatiion(). this keeps it from confusing python
    student_count = session.query(func.count(Student.id)).first()
    #example of filter()
    query = session.query(Student).filter(Student.name.like('%Alan%'),
        Student.grade == 11).all()
    
    # for record in query:
    #     print(record.name)

    #updating data###############
    # for student in session.query(Student):
    #     student.grade += 1

    # session.commit()
    #OR
    session.query(Student).update({
        Student.grade: Student.grade + 1
    })
    # print([(student.name, student.grade) for student in session.query(Student)])
    #####################
    #deleting data
    delete_query = session.query(
        Student).filter(Student.name == "Albert Einstein")
    albert_einstein = delete_query.first()
    session.delete(albert_einstein)
    session.commit()
    albert_einstein = delete_query.first()
    print(albert_einstein)
    #another way to delete
    #delete_query.delete()
    #this deletes all objects returned by query so be careful

    

