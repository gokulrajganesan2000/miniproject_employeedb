from sqlalchemy import create_engine, Column, Integer, String, DATE, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update
import datetime

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employee'

    emp_id = Column('id', Integer(), primary_key=True)
    emp_name = Column('name', String())
    emp_dob = Column('dob', DATE())
    gender = Column('gender', String())
    join_date = Column('join_date', DATE())
    emp_dept = Column('deportment', String())
    designation = Column('designation', String())


engine = create_engine('sqlite:///employee.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()
def check_date_format(dates):
    if int(dates[0])>0 and int(dates[0])<32 and int(dates[1])>0 and int(dates[1])<13 and int(dates[2])>0:
        return True
    return False

def check_dob_eligibility(dates):
    dates=dates.split('/')
    if check_date_format(dates):
        dates=datetime.date(int(dates[2]), int(dates[1]), int(dates[0]))
        today = datetime.date.today()
        age= today.year - dates.year - ((today.month, today.day) < (dates.month, dates.day))
        if age>=18 and age<=60:
            return True
        else:
            return False
    else:
        return False

def check_join_date(ijoin_date):
    ijoin_date=ijoin_date.split('/')
    if not(int(ijoin_date[0])>0 and int(ijoin_date[0])<32 and int(ijoin_date[1])>0 and int(ijoin_date[1])<13 and int(ijoin_date[2])>0):
        return False
    else:
        ijoin_date=datetime.date(int(ijoin_date[2]), int(ijoin_date[1]), int(ijoin_date[0]))
        if not ijoin_date<=datetime.date.today():
            return False
    return True


def name_condition(iemp_name):
    for i in range(len(iemp_name)-3):
        if(iemp_name[i] == iemp_name[i+1]):
            if(iemp_name[i] == iemp_name[i+2]):
                return False
    return True
print('Select Option 1-> Update,2->view,3-> insert')
opp=int(input())
if opp==1:
    ###########update#####################
    emp=session.query(Employee).filter(Employee.emp_id==input('enter a employee id :')).one()
    print('1 -> change name ,2 -> change DOB,3 -> change gender,4 -> change joindate,5 -> change department,6 -> change designation')
    option=int(input('Enter option'))

    if option==1:
        name=input()
        if name_condition(name):
            emp.emp_name=name
        else:
            print('error')
    elif option==2:
        dob=input()
        if check_dob_eligibility(dob):
            emp.emp_dob=dob
        else:
            print('Invalid Date Formate')
    elif option==3:
        emp.gender=input()
    elif option==4:
        jdate=input()
        if check_join_date(jdate):
            emp.join_date=jdate
    elif option==5:
        emp.emp_dept=input()
    elif option==6:
        emp.designation=input()

    session.commit()
elif opp==2:
    ##############retrive#####################
    employee=session.query(Employee).all()
    for i in employee:
        print('Employee ID :',i.emp_id)
        print('Employee Name :',i.emp_name)
        print('Employee DOB :',i.emp_dob)
        print('Employee Gender :',i.gender)
        print('Employee Join Date :',i.join_date)
        print('Employee Department :',i.emp_dept)
        print('Employee Designation :',i.designation)

        for j in range(50):
            print('-',end='')
        print()
elif opp==3:
    ###########create##################
    #input
    iemp_id = input('Enter Employee Id : ')
    iemp_name = input('Enter Employee Name : ')
    iemp_dob = input('Enter Employee DOB : ')
    igender = input('Enter Employee Gender : ')
    ijoin_date = input('Enter Employee JoinDate : ')
    iemp_dept = input('Enter Employee Department : ')
    idesignation = input('Enter Employee Designation : ') 

    error = 0
    # id condition
    if len(iemp_id) == 4 and iemp_id.isnumeric():
        iemp_id = int(iemp_id)
    else:
        error = 1
        print('invalid id ')

    #name condition
    if name_condition(iemp_name):
        # emp.emp_name=iemp_name
        pass
    else:
        error = 1
        print('error')

    #dob condition
    if check_dob_eligibility(iemp_dob):
        iemp_dob=iemp_dob.split('/')
        iemp_dob=datetime.date(int(iemp_dob[2]),int(iemp_dob[1]),int(iemp_dob[0]))
    else:
        error = 1
        print('Invalid Date Formate')

    #join date condition
    if check_join_date(ijoin_date):
        ijoin_date=ijoin_date.split('/')
        ijoin_date=datetime.date(int(ijoin_date[2]),int(ijoin_date[1]),int(ijoin_date[0]))
        #emp.join_date=ijoin_date
    else:
        error = 1
        print('wrong date format')

    if error==0:
        emp=Employee()
        emp.emp_id=iemp_id
        emp.emp_name=iemp_name
        emp.emp_dob=iemp_dob
        emp.gender=igender
        emp.join_date=ijoin_date
        emp.emp_dept=iemp_dept
        emp.designation=idesignation
        try:
            session.add(emp)
            session.commit()
        except SQLAlchemyError as e:
            print(e)

        # employee=session.query(Employee).all()
        #for i in employee:
        #   print(i.emp_dob) 

        session.close()
    else:
        print('please retry')
