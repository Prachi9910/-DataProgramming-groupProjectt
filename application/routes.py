from datetime import date

from application import app
from flask import render_template, url_for, redirect, flash, get_flashed_messages, request
from application.form import UserDataForm
from application.models import IncomeExpenses
from application import db
import json

@app.route('/')
def index():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template('index.html', entries = entries)

@app.route('/add', methods = ["POST", "GET"])
def add_expense():
    form = UserDataForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(type=form.type.data, category=form.category.data, amount=form.amount.data)
        db.session.add(entry)
        db.session.commit()
        flash(f"{form.type.data} has been added to {form.type.data}s", "success")
        return redirect(url_for('index'))
    return render_template('add.html', title="Add expenses", form=form)

@app.route('/query', methods = ["POST", "GET"])
def byid():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("querybyID.html")

@app.route("/<usr>")
def user(usr):
    entries = IncomeExpenses.query.filter(IncomeExpenses.id == int(usr)).all()
    return render_template('output.html', entries=entries)

@app.route('/querybyrange', methods = ["POST", "GET"])
def byrange():
    if request.method == "POST":
        mina = request.form["mina"]
        maxa = request.form["maxa"]
        return redirect(url_for("user2", mina=mina, maxa=maxa))
    else:
        return render_template("querybyrange.html")

@app.route("/<mina>/<maxa>")
def user2(mina,maxa):
    entries = IncomeExpenses.query.filter(IncomeExpenses.amount.between(int(mina),int(maxa))).all()
    return render_template('output.html', entries=entries)

@app.route('/delete-post/<int:entry_id>')
def delete(entry_id):
    entry = IncomeExpenses.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/dashboard')
def dashboard():
    income_vs_expense = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.type).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()

    category_comparison = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.category).group_by(IncomeExpenses.category).order_by(IncomeExpenses.category).all()

    dates = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.date).group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('dashboard.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label)
                        )