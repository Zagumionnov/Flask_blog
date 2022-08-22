from wtforms import Form, StringField, PasswordField


class LoginForm(Form):
    email = StringField('Email')
    password = PasswordField('Password')


class SignupForm(Form):
    name = StringField('Name')
    email = StringField('Email')
    password = PasswordField('Password')
    # repeat_password = PasswordField('Repeat password')
