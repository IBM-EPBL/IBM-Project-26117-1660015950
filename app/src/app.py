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

#ADMIN

@app.route('/admin/login',methods=['GET','POST'])
def admin_login():
    form = AdminLoginForm()
    if is_admin_loggedin():
        return redirect('/admin/dashboard')
    elif request.method=='POST' and form.validate():
        admin = Admin.find_admin_by_email(conn,form.email.data)
        if admin:
            if password_verify(admin.password,form.password.data):
                session['loggedin'] = True
                session['ID'] = admin.id
                session['USER'] = 'ADMIN'
                return redirect('/admin/dashboard')
            else:
                flash('Login Failed ! Incorrect Password !','danger')   
        else:
            flash('Login Failed ! User does not exist !','danger')
    return render_template('admin/admin.login.html',form=form)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return admin_not_loggedin_redirect()

@app.route('/admin/signup',methods=['GET','POST'])
def admin_signup():
    form = AdminSignupForm()
    if is_admin_loggedin():
        return customer_loggedin_redirect()
    elif request.method=='POST' and form.validate():
        admin = Admin.construct_admin_from_form(form)
        admin.password = password_hash(admin.password)
        try:
            admin.create_admin(conn)
            flash('Signup Successful !','success')
        except Exception as e:
            flash('Already a admin exists with the same Email ID!','danger')
    return render_template('admin/admin.signup.html',form=form)    

@app.route('/admin/dashboard')
def admin_dashboard():
    if is_admin_loggedin():
        unassigned_complaints = Complaint.find_all_unassinged_complaints(conn)
        assigned_complaints = Complaint.find_all_assigned_complaints(conn)
        resolved_complaints = Complaint.find_all_resolved_complaints(conn)
        return render_template('admin/admin.dashboard.html',unassigned_complaints=unassigned_complaints,assigned_complaints= assigned_complaints,resolved_complaints=resolved_complaints)
    else:
        return admin_not_loggedin_redirect()





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

#AGENT

@app.route('/agent/signup',methods=['GET','POST'])
def agent_signup():
    form = AgentSignupForm()
    if is_agent_loggedin():
        return agent_loggedin_redirect()
    elif request.method=='POST' and form.validate():
        agent = Agent.construct_agent_from_form(form)
        agent.password = password_hash(agent.password)
        try:
            agent.create_agent(conn)
            flash('Agent created Successfully !','success')
        except Exception:
            flash('Email ID already exists !','danger')
    return render_template('agent/agent.signup.html',form=form)

@app.route('/agent/login',methods=['GET','POST'])
def agent_login():
    form = AgentLoginForm()
    if is_agent_loggedin():
        return agent_loggedin_redirect()
    elif request.method=='POST' and form.validate():
        agent = Agent.find_agent_by_email(conn,form.email.data)
        if agent:
            if password_verify(agent.password,form.password.data):
                session['loggedin'] = True
                session['ID'] = agent.id
                session['USER'] = 'AGENT'
                return redirect('/agent/dashboard')
            else:
                flash('Login Failed ! Incorrect Password !','danger')   
        else:
            flash('Login Failed ! User does not exist !','danger')
    return render_template('agent/agent.login.html',form=form)


@app.route('/agent/logout')
def agent_logout():
    session.clear()
    return agent_not_loggedin_redirect()



@app.route('/agent/dashboard')
def agent_dashboard():
    if is_agent_loggedin():
        assigned_complaints = Complaint.find_all_complaints_assigned_to_agent(conn,session['ID'])
        print(len(assigned_complaints))
        return render_template('agent/agent.dashboard.html',assigned_complaints=assigned_complaints)
    else:
        return agent_not_loggedin_redirect()


#CUSTOMER_COMPLAINT


@app.route('/complaint/create',methods=['GET','POST'])
def create_complaint():
    form = ComplaintCreateForm()
    if not is_customer_loggedin():
        return customer_not_loggedin_redirect()
    if request.method=='POST' and form.validate():
        complaint = Complaint.construct_complaint_from_create_form(form)
        complaint.customer_id = session['ID']
        complaint.create_complaint(conn)
        flash('Complaint Posted successfully !','success')
        AppHelper.send_complaint_opened_mail_to_customer(conn,mail,complaint)
        form = ComplaintCreateForm(formdata=None)
    return render_template('complaint/create.complaint.html',form=form)

@app.route('/complaint/<int:complaint_id>/edit',methods=['GET','POST'])
def edit_complaint(complaint_id):
    if is_customer_loggedin():
        complaint: Complaint = Complaint.find_complaint_by_id(conn,complaint_id)
        form = ComplaintEditForm()
        if complaint:
            if complaint.customer_id ==session['ID']:
                if complaint.status == 'RESOLVED':
                    flash('Complaint has been REOLSVED !','warning')
                elif complaint.status == 'ASSIGNED':
                    flash('Agent has been assigned ! Complaint under review !','warning')
                elif request.method == 'POST' and form.validate():
                    complaint.title = form.title.data
                    complaint.description = form.description.data
                    complaint.category = form.category.data
                    if form.resolved.data == True:
                        complaint.status = "RESOLVED"
                    Complaint.update_complaint(conn,complaint)
                    flash('Complaint updated successfully !','success');
                if complaint.status == 'OPENED':
                    form = ComplaintEditForm(data={'title':complaint.title,'description':complaint.description,'category':complaint.category,'resolved':False})
                else:
                    complaint = None
                    form = ComplaintEditForm(formdata=None)
            else:
                flash('Unatuhorized Action !','danger')
        else:
            flash('Complaint not found !','warning')
        return render_template('complaint/edit.complaint.html',complaint=complaint,form = form)
    else:
        return customer_not_loggedin_redirect()

@app.route('/complaint/<int:complaint_id>/assign',methods=['GET','POST'])
def complaint_assign(complaint_id):
    if is_admin_loggedin():
        form = ComplaintAssignForm()
        form.agent.choices = AgentHelper.get_agent_select_field_list(Agent.find_all_agents(conn))
        complaint:Complaint = Complaint.find_complaint_by_id(conn,complaint_id)
        if complaint:
            if complaint.status=='RESOLVED':
                flash('Complaint Resolved !','danger')
            
            elif request.method=='POST' and form.validate():
                if complaint.status=='OPENED':
                    AgentAssign.assign_agent_to_opened_complaint(conn,complaint.id,form.agent.data)
                else:
                    AgentAssign.assign_agent_to_assigned_complaint(conn,complaint.id,form.agent.data)
                complaint.status='ASSIGNED'
                AppHelper.send_complaint_assigned_mail_to_agent(conn,mail,complaint,form.agent.data)
                AppHelper.send_complaint_assigned_mail_to_customer(conn,mail,complaint,form.agent.data)
                flash('Agent Assigned successfully !','success')
        else:
            flash('Complaint does not exist !','danger')
        return render_template('complaint/assign.complaint.html',complaint=complaint,form=form)
    else:
        return admin_not_loggedin_redirect()

@app.route('/complaint/<int:complaint_id>/resolve',methods=['GET','POST'])
def complaint_resolve(complaint_id):
    if is_agent_loggedin():
        complaint = Complaint.find_complaint_by_id(conn,complaint_id)
        agent_assign = AgentAssign.find_agent_assign_by_complaint_id(conn,complaint_id)
        form = ComplaintReplyAndResolveForm(data={'message':'','resolved':False})
        if complaint:
            if complaint.status=='RESOLVED':
                flash('Complaint Already Resolved !','danger')
            elif complaint.status == 'OPENED':
                flash('Complaint not assigned yet !')
            elif agent_assign.agent_id != session['ID']:
                flash('Unauthorized Action !','warning')
            elif request.method=='POST' and form.validate():
                agent_message = form.message.data
                if form.resolved.data:
                    AgentAssign.change_status_to_resolved_complaint(conn,complaint.id,session['ID'])
                    complaint.status='RESOLVED'      
                    flash('Complaint Resolved Successfully !','success')
                AppHelper.send_complaint_resolved_mail_to_customer(conn,mail,complaint,session['ID'],agent_message)
                flash('Customer has been notified !','success')
            return render_template('complaint/resolve.complaint.html',form=form,complaint= complaint)
        else:
            flash('Complaint does not exist !','danger')
    else:
        return agent_not_loggedin_redirect()

@app.route('/play')
def play():
    opts = AgentHelper.get_agent_select_field_list(Agent.find_all_agents(conn))
    print(opts)
    return 'PLAY'

    
if __name__ == "__main__":
    app.run('0.0.0.0',port=5000,debug=True)
