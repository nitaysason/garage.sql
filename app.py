import sqlite3
from flask import Flask, redirect, render_template, request, url_for

con = sqlite3.connect("garage.db", check_same_thread=False)
cur = con.cursor()

api = Flask(__name__)

try :
      cur.execute("CREATE TABLE garage(color, model, brand)")
except : pass

@api.route('/')
def home():
      cur.execute("SELECT * FROM garage")
      garage = cur.fetchall() 
      return render_template("home.html", garage=garage)
    

@api.route('/add_cars', methods=['GET', 'POST'])
def add_cars():
    if request.method == 'POST':
        color = request.form['color']
        model = request.form['model']
        brand = request.form['brand']
        cur.execute("INSERT INTO garage (color, model, brand) VALUES (?, ?, ?)", (color, model, brand))
        con.commit()
        return redirect(url_for('home'))
    return render_template("add_cars.html")

@api.route('/cars_list')
def cars_list():
    cur.execute("SELECT rowid,* FROM garage") #get all cars from DB
    garage = cur.fetchall() # cars - list of cars
  
    return render_template("cars_list.html", garage=garage)

@api.route('/delete_garage/<int:garage_id>', methods=['POST', 'DELETE'])
def delete_garage(garage_id):
    if request.method in ['POST', 'DELETE']:
        cur.execute("DELETE FROM garage WHERE rowid=?", (garage_id,))
        con.commit()
        return redirect('/cars_list')
    
@api.route('/update_car/<int:car_id>', methods=['GET', 'POST'])
def update_car(car_id):
    if request.method == 'POST':
        color = request.form['color']
        model = request.form['model']
        brand = request.form['brand']
        cur.execute("UPDATE garage SET color=?, model=?, brand=? WHERE rowid=?", (color, model, brand, car_id))
        con.commit()
        return redirect(url_for('cars_list'))
    
    cur.execute("SELECT rowid,* FROM garage WHERE rowid=?", (car_id,))
    car = cur.fetchone()
    return render_template("update_car.html", car=car)

if __name__ == '__main__':
    api.run(debug=True)
