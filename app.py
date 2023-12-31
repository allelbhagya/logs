from flask import Flask, render_template, request, jsonify, redirect, url_for, json
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

import pickle
import pandas as pd

with open('regionwise_columns.pickle', 'rb') as f:
    sensor_data = pickle.load(f)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_type = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(255), nullable=False)
    datetime = db.Column(db.String(50), nullable=False)
    signals = db.Column(db.String(255), nullable=False)
    affected_region = db.Column(db.String(255), nullable=False)
    correctness_measures = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    return render_template('index.html',signals_data=sensor_data)

@app.route('/add_log', methods=['POST'])
def add_log():
    data = request.form
    log_type = data.get('log_type')

    new_log = Log(
        log_type=log_type,
        details=data['log_details'],
        datetime=data['datetime'],
        signals=data['signals'],
        affected_region=data['affected_region'],
        correctness_measures=data['correctness_measures']
    )

    db.session.add(new_log)
    db.session.commit()

    return jsonify({'message': f'{log_type.capitalize()} added successfully'}), 200

@app.route('/logs/<log_type>')
def logs(log_type):
    logs = Log.query.filter_by(log_type=log_type).all()
    return render_template('logs.html', logs=logs, log_type=log_type)

@app.route('/edit/<log_type>/<int:id>', methods=['GET', 'POST'])
def edit_log(log_type, id):
    log = Log.query.get(id)

    if request.method == 'POST':
        log.details = request.form['log_details']
        log.datetime = request.form['datetime']
        log.signals = request.form['signals']
        log.affected_region = request.form['affected_region']
        log.correctness_measures = request.form['correctness_measures']
        db.session.commit()
        return redirect(url_for('logs', log_type=log_type))

    return render_template('edit_log.html', log=log, log_type=log_type)

@app.route('/delete/<log_type>/<int:id>')
def delete_log(log_type, id):
    log = Log.query.get(id)
    db.session.delete(log)
    db.session.commit()
    return redirect(url_for('logs', log_type=log_type))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
