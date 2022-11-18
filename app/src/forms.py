from flask_wtf import FlaskForm
from wtforms import EmailField,PasswordField,StringField,SelectField,TextAreaField,HiddenField,BooleanField
from wtforms.validators import DataRequired,EqualTo,Regexp

class AdminLoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired('Email is required !')])
    password = PasswordField(validators=[DataRequired('Password is required !')])

class AdminSignupForm(FlaskForm):
    email = EmailField(validators=[DataRequired('Email is required !')])
    password = PasswordField(validators=[DataRequired('Password is required !'),EqualTo('confirm_password','Passwords donot match !')])
    confirm_password = PasswordField(label='Confirm Password',validators=[DataRequired('Confirm Password is required !'),EqualTo('password','Passwords donot match !')])
    first_name = StringField('First Name',id='fname',validators=[DataRequired('First Name is required !')])
    last_name = StringField('Last Name',id='lname',validators=[DataRequired('Last Name is required !')])
    
class AgentLoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired('Email is required !')])
    password = PasswordField(validators=[DataRequired('Password is required !')])


class AgentSignupForm(FlaskForm):
    email = EmailField(validators=[DataRequired('Email is required !')])
    password = PasswordField(validators=[DataRequired('Password is required !'),EqualTo('confirm_password','Passwords donot match !')])
    confirm_password = PasswordField(label='Confirm Password',validators=[DataRequired('Confirm Password is required !'),EqualTo('password','Passwords donot match !')])
    first_name = StringField('First Name',id='fname',validators=[DataRequired('First Name is required !')])
    last_name = StringField('Last Name',id='lname',validators=[DataRequired('Last Name is required !')])
    category = SelectField('Category',choices=[['Hardware','HARDWARE'],['Software','SOFTWARE']],validators=[DataRequired('Category is required !')])

    
class CustomerLoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired('Email is required !')])
    password = PasswordField(validators=[DataRequired('Password is required !')])

class CustomerSignupForm(FlaskForm):
    email = EmailField(validators=[DataRequired('Email is required !')])
    password = PasswordField(validators=[DataRequired('Password is required !'),EqualTo('confirm_password','Passwords donot match !')])
    confirm_password = PasswordField(label='Confirm Password',validators=[DataRequired('Confirm Password is required !'),EqualTo('password','Passwords donot match !')])
    first_name = StringField('First Name',id='fname',validators=[DataRequired('First Name is required !')])
    last_name = StringField('Last Name',id='lname',validators=[DataRequired('Last Name is required !')])
    mobile = StringField(validators=[DataRequired('First Name is required !'),Regexp(regex="[0-9]{10}",message="Enter a valid mobile number")])
    gender = SelectField(choices=['Male','Female','Other'],validators=[DataRequired('Gender is required !')])
    address = TextAreaField('Address',validators=[DataRequired('Address is required !')])
    

class ComplaintCreateForm(FlaskForm):
    title = StringField('Title',id='title',validators=[DataRequired('Title is required !')])
    category = SelectField('Category',choices=[['Hardware','HARDWARE'],['Software','SOFTWARE']],validators=[DataRequired('Category is required !')])
    description = TextAreaField('Description',id='description',validators=[DataRequired('Description is required !')])

class ComplaintEditForm(ComplaintCreateForm):
    resolved = BooleanField('Resloved')
    

class ComplaintAssignForm(FlaskForm):
    agent = SelectField('Agent',choices=[],validators=[DataRequired('Agent is required !')])

class ComplaintReplyAndResolveForm(FlaskForm):
    message = TextAreaField('Message',validators=[DataRequired('Message is required !')])
    resolved = BooleanField('Resloved')
