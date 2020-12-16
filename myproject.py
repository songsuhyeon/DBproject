from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_bootstrap import Bootstrap

app = Flask(__name__)

@app.route('/')
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/main/list')
def showlist():
    db = sqlite3.connect("DBlist.db")
    db.row_factory = sqlite3.Row
    items = db.execute(
        'select id, name, address, call, lecture, duration, total_price from Academy'
    ).fetchall()
    db.close()
    return render_template('list.html', items= items)

@app.route('/main/list/edit/<int:list_id>/', methods=['GET','POST'])
def editlist(list_id):
    if request.method=='POST':
        db = sqlite3.connect("DBlist.db")
        db.row_factory = sqlite3.Row
        db.execute(
            'update Academy'
            ' set name=?'
            ' where id=?',
            (request.form['list_name'],list_id),
        )
        db.commit()
        db.close()
        return redirect(url_for('showlist'))
    else:
        db = sqlite3.connect("DBlist.db")
        db.row_factory = sqlite3.Row
        item = db.execute(
            'select id, name, address, call, lecture, duration, total_price from Academy where id=?',(list_id,)
        ).fetchone()
        db.close()
        return render_template('editlist.html', item=item)
        

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)

    