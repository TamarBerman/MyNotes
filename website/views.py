from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json
from . import db
from .models import Note
import pandas as pd

views = Blueprint('views', __name__)


@login_required
@views.route('/all-history', methods = ['GET', 'POST'])
def all_history():
    """only manger has access to this page. this func reads csv, sorts its data by users name (id)"""
    csv_data = pd.read_csv('data.csv')
    sorted_df = csv_data.sort_values(by = ["Name"], ascending = True)
    sorted_df.to_csv('data.csv', index = False)
    '''send info to html (pd = pd), only manager has access (manager = True) '''
    return render_template('history.html', user = current_user, pd = pd, manager = True)


@login_required
@views.route('/my-history', methods = ['GET', 'POST'])
def my_history():
    """each user can watch his own notes history including deleted notes. they are read from the csv file and and
    they are displayed in html format  """
    csv_data = pd.read_csv('data.csv')
    sorted_df = csv_data.sort_values(by = ["Name"], ascending = True)
    sorted_df.to_csv('data.csv', index = False)
    '''send info to html (pd = pd), every one has access (manager = False) '''
    return render_template('history.html', user = current_user, pd = pd, manager = False)


@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    """home-page- user sees his notes and can add notes. this func retrieves info from the form and add to db,
    then render the page, and we will see the new note added and empty form """
    if request.method == 'POST':
        note = request.form.get('note')
        add_note(note)
    return render_template('home.html', user = current_user)


def add_note(note):
    """adds a new note to the DB and to our csv file"""
    if len(note) < 1:
        flash("note is too shprt", category = "error")
    else:
        new_post = Note(data = note, user_id = current_user.id)
        db.session.add(new_post)
        db.session.commit()
        add_to_csv(new_post)
        flash("Note Added", category = "success")


def add_to_csv(new_post):
    """creates a dataframe with the note info and add it to the csv file """
    data = {
        'Name': [new_post.user_id],
        'WriteDate': [new_post.date],
        'Data': [new_post.data],
    }
    df = pd.DataFrame(data)
    df.to_csv('data.csv', mode = 'a', index = False, header = False)
    df = pd.read_csv('data.csv')
    print(df)


@views.route('/delete-note', methods = ['POST'])
def delete_post():
    """this function will be called from a JS fetch, and will delete it from db """
    '''it expects a JSON from the INDEX.js file'''
    note = json.loads(request.data)
    # שומר את הסטרינג שקיבלנו כאוביקט
    '''saves the string we got as an object'''
    post_id = note['post_id']
    note = Note.query.get(post_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
        return jsonify({})
