import ibm_db
from flask import Flask,session,redirect,render_template,request,flash,url_for
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_mail import Mail

from sqlstmts import CREATE_CUSTOMERS_SQL,CREATE_ADMINS_SQL,CREATE_AGENTS_SQL,CREATE_STATUS_SQL,CREATE_COMPLAINTS_SQL,CREATE_COMPLAINT_STATUS_ASSIGN

from forms import AdminLoginForm,CustomerSignupForm,CustomerLoginForm,AgentSignupForm,AgentLoginForm,ComplaintCreateForm,ComplaintEditForm,AdminSignupForm,ComplaintAssignForm,ComplaintReplyAndResolveForm

from dbactions import Customer,Agent,Complaint,Admin,AgentAssign

from helpers import AgentHelper,AppHelper

import appsecrets


def create_tables(conn):
    create_stmts = [CREATE_CUSTOMERS_SQL]
    for create_stmt in create_stmts:
        ibm_db.exec_immediate(conn,create_stmt)


conn = None

try:
    conn = ibm_db.connect(f"DATABASE={appsecrets.DB_NAME};HOSTNAME={appsecrets.DB_HOSTNAME};PORT={appsecrets.DB_PORT};SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID={appsecrets.DB_USERNAME};PWD={appsecrets.DB_PASSWORD}",'','')
    print(ibm_db.server_info(conn))
except Exception as e:
    print(ibm_db.conn_errormsg())
    print(e)
    exit()


app = Flask(__name__)

app.secret_key = appsecrets.FLASK_APP_SECRET

#START MAIL CONFIG




app.config['MAIL_SERVER'] = appsecrets.MAIL_SERVER
app.config['MAIL_PORT'] = appsecrets.MAIL_PORT
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME']  = appsecrets.MAIL_USERNAME
app.config['MAIL_PASSWORD']  = appsecrets.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = appsecrets.MAIL_DEFAULT_SENDER

mail = Mail(app)

# END MAIL CONFIG


print('MAIL INIT COMPLETE ')

csrf = CSRFProtect(app)

bcrypt = Bcrypt(app)

#APP HELPER FUNCTIONS

def password_hash(password:str):
    return bcrypt.generate_password_hash(password).decode("utf-8") 

def password_verify(hash:str,password:str):
    return bcrypt.check_password_hash(hash,password)


def is_customer_loggedin():
    return 'loggedin' in session and session['USER']=='CUSTOMER'

def customer_loggedin_redirect():
    return redirect(url_for('customer_dashboard'))


def customer_not_loggedin_redirect():
    return redirect(url_for('customer_login'))

def is_admin_loggedin():
    return 'loggedin' in session and session['USER']=='ADMIN'

def admin_logged_in_redirect():
    return redirect(url_for('admin_dashboard'))

def admin_not_loggedin_redirect():
    return redirect(url_for('admin_login'))


def is_agent_loggedin():
    return 'loggedin' in session and session['USER']=='AGENT'

def agent_not_loggedin_redirect():
    return redirect(url_for('agent_login'))

def agent_loggedin_redirect():
    return redirect(url_for('agent_dashboard'))


@app.route("/")
def home():
    return render_template('home.html')



#CUSTOMER
@app.route('/customer/signup',methods=['GET','POST'])
def customer_signup():
    form = CustomerSignupForm()
    if is_customer_loggedin():
        return customer_loggedin_redirect()
    elif request.method=='POST' and form.validate():
        customer = Customer.construct_customer_from_form(form)
        customer.password = password_hash(customer.password)
        try:
            customer.create_customer(conn)
            flash('Signup Successful !','success')
        except Exception as e:
            print(e)
            flash('Already a customer exists with the same Email ID!','danger')
    return render_template('customer/customer.signup.html',form=form)        

@app.route('/customer/login',methods=['GET','POST'])
def customer_login():
    form = CustomerLoginForm()
    if is_customer_loggedin():
        return customer_loggedin_redirect()
    elif request.method=='POST' and form.validate():
        customer = Customer.find_user_by_email(conn,form.email.data)
        if customer:
            if password_verify(customer.password,form.password.data):
                session['loggedin'] = True
                session['ID'] = customer.id
                session['USER'] = 'CUSTOMER'
                return redirect('/customer/dashboard')
            else:
                flash('Login Failed ! Incorrect Password !','danger')   
        else:
            flash('Login Failed ! User does not exist !','danger')
    return render_template('customer/customer.login.html',form=form)

@app.route('/customer/logout')
def customer_logout():
    session.clear()
    return customer_not_loggedin_redirect()



@app.route('/customer/dashboard')
def customer_dashboard():
    if is_customer_loggedin():
        complaints = Complaint.find_all_complaint_by_customer_id(conn,session['ID'])
        print(complaints)
        return render_template('customer/customer.dashboard.html',complaints=complaints)
    return customer_not_loggedin_redirect()



    
if __name__ == "__main__":
    app.run('0.0.0.0',port=5000,debug=True)
