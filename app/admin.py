from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from wtforms import SelectMultipleField, StringField, SelectField  # Import StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

from app import app, db
from app.models import User, Group, UserGroupAssociation, Post

# Create Flask-Admin instance
admin = Admin(app, name='microblog', template_mode='bootstrap3')

# Define a form for UserGroupAssociation model which created many-to-many relationship with User and Group
class UserGroupForm(FlaskForm):
    user_id = SelectField('User', validators=[DataRequired()])
    group_id = SelectField('Group', validators=[DataRequired()])

    # Initialize the user choices in the constructor
    def __init__(self, *args, **kwargs):
        super(UserGroupForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(str(user.id), user.username) for user in User.query.all()]  # Fetch user choices
        self.group_id.choices = [(str(group.id), group.name) for group in Group.query.all()]  # Fetch user choices
    

# Creating a custom view for the  UserGroupAssociation model 
class UserGroupFormView(ModelView):
    column_list = ['user_id', 'group_id']

    #Changing column names to appropriate ones
    column_labels = {
        'user_id': 'Username',
        'group_id': 'Group Name',
    }

    #Displaying username and group name instead of their id's
    column_formatters = {
        'user_id': lambda view, context, model, name: model.users.username,
        'group_id': lambda view, context, model, name: model.groups.name,
    }

    #Method for creating or updating UserGroupFormView 
    def on_model_change(self, form, model, is_created):
        selected_user = User.query.get(form.user_id.data)
        selected_group = Group.query.get(form.group_id.data)

        if not model.user_id or not model.group_id:
            raise ValueError("Both user and group must be selected.")
        
        model.user = selected_user
        model.group = selected_group
        super(UserGroupFormView, self).on_model_change(form, model, is_created)
    form = UserGroupForm

#Adding GroupView to the admin instance
admin.add_view(ModelView(model=Group, session=db.session))

# Adding UserGroupFormView to the admin instance
admin.add_view(UserGroupFormView(model=UserGroupAssociation, session=db.session))


