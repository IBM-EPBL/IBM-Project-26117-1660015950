from __future__ import annotations

import json
import ibm_db

from forms import CustomerSignupForm,AgentSignupForm,ComplaintCreateForm,ComplaintEditForm


class AppModel:
    pass


class Customer(AppModel):
    def __init__(self,id,email:str,password:str,first_name:str,last_name:str,mobile:str,gender:str,address:str,created_at=None):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.mobile = mobile
        self.gender = gender
        self.address = address
        self.created_at = created_at
        
    
    def create_customer(self,conn):
        sql = "INSERT INTO CUSTOMERS (EMAIL,PASSWORD,FIRST_NAME,LAST_NAME,MOBILE,GENDER,ADDRESS) VALUES(?,?,?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt, 1, self.email)
        ibm_db.bind_param(prep_stmt, 2, self.password)
        ibm_db.bind_param(prep_stmt, 3, self.first_name)
        ibm_db.bind_param(prep_stmt, 4, self.last_name)
        ibm_db.bind_param(prep_stmt, 5, self.mobile)
        ibm_db.bind_param(prep_stmt, 6, self.gender)
        ibm_db.bind_param(prep_stmt, 7, self.address)
        result = ibm_db.execute(prep_stmt)
    

    def to_dict(self,remove_password=True):
        return {'id':self.id,'email':self.email,'password': '' if remove_password else self.password,'first_name':self.first_name,'last_name':self.last_name,'mobile':self.mobile,'gender':self.gender,'address':self.address}
    
    def json(self):
        return json.dumps(self.to_dict())
    
    @staticmethod
    def find_user_by_email(conn,email:str):
        sql = "SELECT * FROM CUSTOMERS WHERE EMAIL = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        return Customer.construct_customer_from_assoc(assoc)
    
    @staticmethod
    def find_customer_by_id(conn,customer_id):
        sql = "SELECT * FROM CUSTOMERS WHERE ID = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,customer_id)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        return Customer.construct_customer_from_assoc(assoc)
    
    @staticmethod
    def construct_customer_from_assoc(assoc):
        if assoc:
            return Customer(assoc['ID'],assoc['EMAIL'],assoc['PASSWORD'],assoc['FIRST_NAME'],assoc['LAST_NAME'],assoc['MOBILE'],assoc['GENDER'],assoc['ADDRESS'],assoc['CREATED_AT'])
        return False

    @staticmethod
    def construct_customer_from_form(form: CustomerSignupForm):
        return Customer(-1,form.email.data,form.password.data,form.first_name.data,form.last_name.data,form.mobile.data,form.gender.data,form.address.data)



