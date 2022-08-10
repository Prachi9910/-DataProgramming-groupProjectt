from application import db, app
from datetime import datetime, date
from flask import render_template

class IncomeExpenses(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), default = 'income', nullable=False)
    category = db.Column(db.String(30), nullable=False, default='rent')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<IncomeExpenses: {self.id},{self.type},{self.category},{self.date},{self.amount}>'




