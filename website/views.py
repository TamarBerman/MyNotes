from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json
from . import db
from .models import Note
import pandas as pd

views = Blueprint('views', __name__)


@login_required
@views.route('/all-history', methods = ['GET', 'POST'])
def allhistory():
    csv_data = pd.read_csv('data.csv')
    sorted_df = csv_data.sort_values(by = ["Name"], ascending = True)
    sorted_df.to_csv('data.csv', index = False)
    print("============================")
    print(pd.read_csv("data.csv"))
    return render_template('history.html', user = current_user, pd = pd,manager=True)

@login_required
@views.route('/my-history', methods = ['GET', 'POST'])
def myhistory():
    csv_data = pd.read_csv('data.csv')
    sorted_df = csv_data.sort_values(by = ["Name"], ascending = True)
    sorted_df.to_csv('data.csv', index = False)
    print("============================")
    print(pd.read_csv("data.csv"))
    return render_template('history.html', user = current_user, pd = pd , manager=False)


'''home page - user sees his notes and can add notes'''


@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    print(current_user)
    if request.method == 'POST':
        note = request.form.get('note')
        add_note(note)
    return render_template('home.html', user = current_user)


'''adds a new note to the DB'''


def add_note(note):
    if len(note) < 1:
        flash("note is too shprt", category = "error")
    else:
        new_post = Note(data = note, user_id = current_user.id)
        db.session.add(new_post)
        db.session.commit()
        add_to_csv(new_post)
        flash("Note Added", category = "success")


def add_to_csv(new_post):
    data = {
        'Name': [new_post.user_id],
        'WriteDate': [new_post.date],
        'Data': [new_post.data],
    }
    df = pd.DataFrame(data)
    df.to_csv('data.csv', mode = 'a', index = False, header = False)
    df = pd.read_csv('data.csv')
    print(df)
    print("id: " + str(new_post.id))


@views.route('/delete-note', methods = ['POST'])
def delete_post():
    # this function expects a JSON from the INDEX.js file
    note = json.loads(request.data)
    # שומר את הסטרינג שקיבלנו כאוביקט
    postId = note['postId']
    note = Note.query.get(postId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
        return jsonify({})
