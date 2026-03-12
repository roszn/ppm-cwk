import json
import os
from flask import Flask, render_template, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'fdm_portal_2026'

def get_content():
    if not os.path.exists('data.json'):
        return []
    with open('data.json', 'r') as f:
        return json.load(f)

def update_content(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    if 'user' not in session:
        session['user'] = 'employee@fdmgroup.com'
    
    items = get_content()
    return render_template('home.html', content=items)

@app.route('/like/<int:item_id>', methods=['POST'])
def add_like(item_id):
    data = get_content()
    count = 0
    for item in data:
        if item['id'] == item_id:
            item['likes'] += 1
            count = item['likes']
    update_content(data)
    return jsonify({'new_count': count})

@app.route('/dislike/<int:item_id>', methods=['POST'])
def add_dislike(item_id):
    data = get_content()
    count = 0
    for item in data:
        if item['id'] == item_id:
            item['dislikes'] = item.get('dislikes', 0) + 1
            count = item['dislikes']
    update_content(data)
    return jsonify({'new_count': count})

@app.route('/profile')
def profile():
    return ""

@app.route('/holiday')
def holiday():
    return ""

@app.route('/structure')
def structure():
    return ""

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)