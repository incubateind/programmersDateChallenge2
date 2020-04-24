import flask
from flask import Flask, render_template, url_for, redirect
from flask import request
import pymysql as mysql

app = Flask(__name__)


@app.route('/donate', methods=["POST", "GET"])
def donate():
    if flask.request.method == 'POST':
        id = request.form.get("Id")
        area = request.form.get("area")
        food_quantity = request.form.get("food_quantity")
        food_type = request.form.get("food_type")
        return render_template("donate.html", area=area, food_quantity=food_quantity, id=id, food_type=food_type)
    else:
        return "Good Job"


@app.route('/donate_details', methods=["POST", "GET"])
def donate_details():
    id = request.form.get("Id")
    name = request.form.get("name")
    area = request.form.get("area")
    number = request.form.get("number")
    food_quantity = int(request.form.get("food_quantity"))
    food_type = request.form.get("food_type")
    print(id, name, area, number, food_quantity)
    connection = mysql.connect(host='whatsapp-database.cwv08t8lmsdn.us-east-2.rds.amazonaws.com',
                               database='user_information',
                               user='sunnypranay',
                               password='pranay1999')
    cursor = connection.cursor()
    sql = ("SELECT * FROM food_request where ID = '%s';" % (id,))
    cursor.execute(sql)
    result = cursor.fetchall()
    if int(result[0][4]) - food_quantity > 0:
        sql = "update food_request set Food_Quantity = '%s' where ID = '%s';" % (
        (int(result[0][4]) - food_quantity), id)
        cursor.execute(sql)
        connection.commit()
        sql = "INSERT INTO Donar_details (name, area, quantity, number, food_type) VALUES (%s,%s,%s,%s,%s)"
        val = (name, area, food_quantity, number, food_type)
        cursor.execute(sql, val)
        connection.commit()
    else:
        sql = ("DELETE FROM food_request where ID = '%s';" % id)
        cursor.execute(sql)
        connection.commit()
        sql = "INSERT INTO Donar_details (name, area, quantity, number, food_type) VALUES (%s,%s,%s,%s,%s)"
        val = (name, area, food_quantity, number, food_type)
        cursor.execute(sql, val)
        connection.commit()
    connection.close()
    return redirect(url_for('food_pending'))


@app.route('/food_pending', methods=["POST", "GET"])
def food_pending():
    connection = mysql.connect(host='whatsapp-database.cwv08t8lmsdn.us-east-2.rds.amazonaws.com',
                               database='user_information',
                               user='sunnypranay',
                               password='pranay1999')
    cursor = connection.cursor()
    sql = "SELECT * FROM Donar_details"
    cursor.execute(sql)
    result = list(cursor.fetchall())
    print(result)
    connection.close()
    return render_template("food_pending.html", data=result)


@app.route('/request', methods=["POST", "GET"])
def food_request():
    connection = mysql.connect(host='whatsapp-database.cwv08t8lmsdn.us-east-2.rds.amazonaws.com',
                               database='user_information',
                               user='sunnypranay',
                               password='pranay1999')
    cursor = connection.cursor()
    area_list = ['75 Feet Service Road', 'Adarsa Nagar Road', 'Aganampudi', 'Akkayyapalem', 'Akkayyapalem Main Road',
                 'Akkireddypalem', 'Allipuram', 'Allipuram Road', 'Anandapuram', 'Arilova', 'Asilmetta', 'Auto Nagar',
                 'Balaji Nagar', 'Balayya Sastri Layout', 'Beach Road', 'Bowdra Ring Road', 'Butchirajupalem',
                 'CBM Compound', 'Chengal Rao Peta', 'Chinna Waltair', 'China Mushidiwada', 'Collector Office Junction',
                 'Daba Garden Road', 'Daba Gardens', 'Daspalla Hills', 'Dayal Nagar', 'Diamond Park Road',
                 'Doctors Colony', 'Dondaparthy', 'Duvada', 'Dwaraka Nagar', 'Dwaraka Nagar Road', 'East Point Colony',
                 'Fishing Harbour', 'Gajuwaka', 'Gnanapuram', 'Gopalapatnam', 'H B Colony', 'Hanumantha Road',
                 'Industral Estate', 'Isakathota', 'Jagadamba Junction', 'Jaill Road', 'KGH Down Road', 'Kailasapuram',
                 'Kancharapalem', 'Kanithi Junction', 'Kirlampudi Layout', 'Krantinagar', 'Krishna Nagar',
                 'Kurmannapalem', 'Lalitha Nagar', 'Lawsons Bay Colony', 'MVP Double Road', 'MVP Main Road',
                 'Maddilapalem', 'Madhavadhara', 'Madhuranagar', 'Madhurawada', 'Maharani Peta', 'Malkapuram',
                 'Marripalem', 'Mudasarlova Road', 'Mindi', 'Murlinagar', 'MVP Colony', 'NAD', 'Naidu Thota',
                 'Narasimhanagar', 'Nathayyapalem', 'New Gajuwaka', 'Nowroji Road', 'Old Bus Stop', 'Old Gajuwaka',
                 'Old Post Office Road', 'P&T Colony Park', 'Panduranga Layout', 'Paravada', 'Pedda Waltair',
                 'Pedagantyada', 'Pendurthi', 'Pithapuram Colony', 'Purna Market', 'Port Area', 'Pothinamallayya Palem',
                 'Prahaladapuram', 'Railway New Colony', 'Rajaram Mohanrai Road', 'Rajendra Nagar', 'Ram Nagar',
                 'Rama Talkies Junction', 'Rednam Gardens', 'Resapuvanipalem', 'RK Beach', 'RTC Complex', 'Rushikonda',
                 'Sagar Nagar', 'Salagramapuram', 'Shankara Matam', 'Santhipuram', 'Saraswathi Junction', 'SBI Colony',
                 'Seethammadhara', 'Seethammadhara Road', 'Seetamma Peta', 'Santhi Puram', 'Sheela Nagar',
                 'Simhachalam Road', 'Simhachalam', 'Simhachalam Road', 'Siripuram', 'Sivajipalem Road', 'Sriharipuram',
                 'Stadium Road', 'Railway Station Road', 'Steel Plant Road', 'Super Bazar', 'Suryabagh', 'TPT Colony',
                 'Thatichetlapalem', 'Town Kotha Road', 'Town Main Road', 'Ukkunagaram', 'Vadlapudi Junction',
                 'Venkojipalem', 'Vepagunta', 'Vidhya Nagar', 'Visakha Dairy', 'Visalakshi Nagar ', 'Vuda Colony',
                 'Waltair Main Road']
    if flask.request.method == 'GET':
        return render_template("register.html", area_list=area_list)
    else:
        name = str(request.form.get("name"))
        number = int(request.form.get("number"))
        email = str(request.form.get("email"))
        area = str(request.form.get("area"))
        food_quantity = int(request.form.get("food_quantity"))
        food_type = request.form.get("food")
        print(name, number, email, area, food_quantity)
        sql = "INSERT INTO food_request (name, phone_number,Area,Food_Quantity,food_type) VALUES (%s,%s,%s,%s,%s)"
        val = (name, number, area, food_quantity, food_type)
        cursor.execute(sql, val)
        connection.commit()
        connection.close()
        return redirect(url_for('home'))


@app.route('/')
def home():
    connection = mysql.connect(host='whatsapp-database.cwv08t8lmsdn.us-east-2.rds.amazonaws.com',
                               database='user_information',
                               user='sunnypranay',
                               password='pranay1999')
    cursor = connection.cursor()
    cursor = connection.cursor()
    sql = "SELECT * FROM food_request"
    cursor.execute(sql)
    result = list(cursor.fetchall())
    print(result)
    connection.close()
    return render_template("home.html", data=result)


if __name__ == '__main__':
    app.run(debug=True)
