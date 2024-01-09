from flask import Flask, render_template,request,session,url_for,redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key= 'my_secret_key'
# MySQL connection configuration
db_config = {
    'host': 'ashishgupta291.mysql.pythonanywhere-services.com',
    'user': 'ashishgupta291',
    'password': 'Password@291',
    'database': 'ashishgupta291$ppm'
}

@app.route('/',methods=['POST','GET'])
def home():
  msg = ''
  try:
    user_name=session.get('user_id')
    if user_name:
       session['user_id']=user_name
       return render_template('index.html')
    if request.method == 'POST':
       user_name = request.form['user_name']
       password = request.form['password']

       connection = mysql.connector.connect(**db_config)
       cursor = connection.cursor(dictionary=True)
       cursor.execute('SELECT * FROM account WHERE user_name = %s AND password = %s', (user_name, password))
       account = cursor.fetchall()
       # Close the cursor and connection
       cursor.close()
       connection.close()
       if account:
           session['user_id']=user_name
           return render_template('index.html')
       else:
           if user_name=="Username":
               msg="Username cannot be Empty!!"
           elif password=="Password":
               msg="Password cannot be Empty!!"
           else:
               msg="Username or Password wrong !!"

    return render_template('login.html',msg=msg)
  except mysql.connector.Error as e:
    connection.rollback()
    return render_template('login.html',msg=f"Sorry !! Failed to login : {str(e)}" )
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/customers',methods=['POST','GET'])
def customers():
  user_name=session.get('user_id')
  if user_name:
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Execute a query to fetch count from the table
        cursor.execute("SELECT count(*) FROM Customer")
        Count = cursor.fetchall()

        # Execute a query to fetch all rows from the table
        cursor.execute("SELECT * FROM Customer order by CustomerID")
        # Fetch all rows as a list of dictionaries
        Cus = cursor.fetchall()

        formated_list=[]
        for cus in Cus:
           cursor.execute("SELECT Contact FROM Cust_contact where CustomerID = %s",(int(cus['CustomerID']),))
           temp_list = cursor.fetchall()
           formated_list.append([item['Contact'] for item in temp_list])

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return render_template('Customer.html', Cus=Cus,count=Count[0]['count(*)'], contact_list=formated_list)
    except mysql.connector.Error as e:
        connection.rollback()
        return f"Sorry !! Failed to show Due to : {str(e)}"
  else:
    return redirect(url_for('home'))
@app.route('/employees',methods=['POST','GET'])
def employees():
  user_name=session.get('user_id')
  if user_name:
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Execute a query to fetch count from the table
        cursor.execute("SELECT count(*) FROM Employee")
        Count = cursor.fetchall()

        # Execute a query to fetch all rows from the table
        cursor.execute("SELECT * FROM Employee join Positions ON Employee.Position_name = Positions.Position_name order by EmployeeID")
        # Fetch all rows as a list of dictionaries
        Emp = cursor.fetchall()

        formated_list=[]
        for emp in Emp:
           cursor.execute("SELECT Contact FROM Emp_contact where EmployeeID = %s",(int(emp['EmployeeID']),))
           temp_list = cursor.fetchall()
           formated_list.append([item['Contact'] for item in temp_list])

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return render_template('Employee.html', Emp=Emp,count=Count[0]['count(*)'],contact_list=formated_list)
    except mysql.connector.Error as e:
        connection.rollback()
        return f"Sorry !! Failed to show Due to : {str(e)}"
  else:
    return redirect(url_for('home'))

@app.route('/fuel_pumps',methods=['POST','GET'])
def pumps():
  user_name=session.get('user_id')
  if user_name:
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Execute a query to fetch count from the table
        cursor.execute("SELECT count(*) FROM FuelPump")
        Count = cursor.fetchall()

        # Execute a query to fetch all rows from the table
        cursor.execute("SELECT PumpID,FuelType,FuelPump.TankID as TankID,Capacity,CurrentVolume,Status as PumpStatus, TankStatus,PricePerLtr FROM FuelPump join (select FuelTank.FuelType as FuelType,TankID,Capacity,CurrentVolume,Status as TankStatus,PricePerLtr  from FuelTank join Fuel on Fuel.FuelType=FuelTank.FuelType ) as FuelTank on FuelPump.TankID = FuelTank.TankID order by PumpID")
        # Fetch all rows as a list of dictionaries
        Pump = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return render_template('Pump.html', Pump=Pump,count=Count[0]['count(*)'])
    except mysql.connector.Error as e:
        connection.rollback()
        return f"Sorry !! Failed to show Due to : {str(e)}"
  else:
    return redirect(url_for('home'))

@app.route('/fuel_tanks',methods=['POST','GET'])
def tanks():
  user_name=session.get('user_id')
  if user_name:
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Execute a query to fetch count from the table
        cursor.execute("SELECT count(*) FROM FuelTank")
        Count = cursor.fetchall()

        # Execute a query to fetch all rows from the table
        cursor.execute("SELECT * FROM FuelTank join Fuel ON Fuel.FuelType = FuelTank.FuelType order by TankID")
        # Fetch all rows as a list of dictionaries
        Tnk = cursor.fetchall()

        formated_list=[]
        for tnk in Tnk:
           cursor.execute("SELECT PumpID FROM FuelPump where TankID = %s",(int(tnk['TankID']),))
           temp_list = cursor.fetchall()
           formated_list.append([item['PumpID'] for item in temp_list])

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return render_template('Tank.html', Tnk=Tnk,count=Count[0]['count(*)'],pump_list=formated_list)
    except mysql.connector.Error as e:
        connection.rollback()
        return f"Sorry !! Failed to show Due to : {str(e)}"
  else:
    return redirect(url_for('home'))

@app.route('/add_fuel',methods=['POST','GET'])
def addf():
  user_name=session.get('user_id')
  if user_name:
    msg=''
    try:
     connection = mysql.connector.connect(**db_config)
     cursor = connection.cursor(dictionary=True)
     cursor.execute("select TankID, FuelType, CurrentVolume,Capacity from FuelTank")
     tanks = cursor.fetchall()
     cursor.close()
     connection.close()
     if request.method == 'POST':
       # Get form data
       tank = request.form['tank']
       quantity = float(request.form['quantity'])

       if float(tanks[0]['CurrentVolume']) + quantity > float(tanks[0]['Capacity']):
           msg=f"Sorry!! Maximum {tanks[0]['Capacity']-tanks[0]['CurrentVolume']} can be added to this Tank"
           return render_template('addFuel.html',tank=tanks,msg=msg)
       # Insert data into the MySQL database
       connection = mysql.connector.connect(**db_config)
       cursor = connection.cursor(dictionary=True)

       insert_query = "update  FuelTank set CurrentVolume=CurrentVolume + %s where TankID=%s"
       data = (quantity, tank,)
       cursor.execute(insert_query, data)
       connection.commit()

       cursor.close()
       connection.close()
       msg=f"Fuel Added Successfuly !!"
     return render_template('addFuel.html',tank=tanks,msg=msg)
    except mysql.connector.Error as e:
     connection.rollback()
     msg= f"Sorry !! Failed Due to : {str(e)}"
     return render_template('addFuel.html',tank=tanks,msg=msg)
  else:
    return redirect(url_for('home'))

@app.route('/addCustomer',methods=['POST','GET'])
def addC():
  user_name=session.get('user_id')
  if user_name:
    msg=''
    try:
     if request.method == 'POST':
       # Get form data
       first_name = request.form['first_name']
       last_name = request.form['last_name']
       email = request.form['email']
       contact_list = request.form.getlist('contact')
       address = request.form['address']

       # Insert data into the MySQL database
       connection = mysql.connector.connect(**db_config)
       cursor = connection.cursor(dictionary=True)

       insert_query = "INSERT INTO Customer (FirstName, LastName, Email, Address) VALUES (%s, %s, %s, %s)"
       data = (first_name, last_name, email, address)
       cursor.execute(insert_query, data)
       connection.commit()
       cursor.execute("select LAST_INSERT_ID()")
       cID=cursor.fetchall()
       for contact in contact_list:
         insert_query = "INSERT INTO Cust_contact (CustomerID, Contact) VALUES ( %s, %s)"
         data = (cID[0]['LAST_INSERT_ID()'],contact)
         cursor.execute(insert_query, data)
         connection.commit()

       cursor.close()
       connection.close()
       msg=f"{first_name} {last_name} Registered Successfuly!!! with ID: {cID[0]['LAST_INSERT_ID()']}"
     return render_template('addCustomer.html',msg=msg)
    except mysql.connector.Error as e:
     connection.rollback()
     msg= f"Sorry !! Failed Due to : {str(e)}"
     return render_template('addCustomer.html',msg=msg)
  else:
    return redirect(url_for('home'))
@app.route('/addEmployee',methods=['POST','GET'])
def addE():
  user_name=session.get('user_id')
  if user_name:
    msg=''
    try:
     connection = mysql.connector.connect(**db_config)
     cursor = connection.cursor(dictionary=True)
     cursor.execute("select Position_name from Positions")
     items = cursor.fetchall()
     cursor.close()
     connection.close()
     position_names = [item['Position_name'] for item in items]

     if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        position =request.form['position']
        email = request.form['email']
        contact_list = request.form.getlist('contact')
        address = request.form['address']

        # Insert data into the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        current_date = datetime.today().date()
        formatted_date = current_date.strftime('%Y-%m-%d')
        insert_query = "INSERT INTO Employee (FirstName, LastName,Position_name, Address, Email,JoiningDate) VALUES (%s,%s, %s, %s, %s,%s)"
        data = (first_name, last_name,position, address, email,formatted_date)

        cursor.execute(insert_query, data)
        connection.commit()

        cursor.execute("select LAST_INSERT_ID()")
        eID=cursor.fetchall()
        for contact in contact_list:
           insert_query = "INSERT INTO Emp_contact (EmployeeID, Contact) VALUES ( %s, %s)"
           data = (eID[0]['LAST_INSERT_ID()'],contact)
           cursor.execute(insert_query, data)
           connection.commit()
        cursor.close()
        connection.close()

        msg=f"{first_name} {last_name} Registered Successfuly!!! with ID: {eID[0]['LAST_INSERT_ID()']}"
     return render_template('addEmployee.html',items=position_names,msg=msg)
    except mysql.connector.Error as e:
     connection.rollback()
     msg= f"Sorry !! Failed Due to : {str(e)}"
     return render_template('addEmployee.html',items=position_names,msg=msg)
  else:
    return redirect(url_for('home'))

@app.route('/remove_customer',methods=['POST','GET'])
def rem_Cus():
  user_name=session.get('user_id')
  if user_name:
   msg=''
   try:
    if request.method == 'POST':
       # Get the ID to delete from the form
       customer_id = request.form['id']
       first_name = request.form['first_name']
       last_name = request.form['last_name']

       # Delete the row from the MySQL database
       connection = mysql.connector.connect(**db_config)
       cursor = connection.cursor(dictionary=True)
       cursor.execute("select * from Customer where CustomerID=%s",(int(customer_id),))
       check=cursor.fetchall()
       cursor.close()
       connection.close()
       if check[0]['CustomerID']== int(customer_id):
          connection = mysql.connector.connect(**db_config)
          cursor = connection.cursor(dictionary=True)
          delete_query = "DELETE FROM Cust_contact WHERE CustomerID = %s"
          data = (customer_id,)
          cursor.execute(delete_query, data)
          connection.commit()
          delete_query = "DELETE FROM Customer WHERE CustomerID = %s and FirstName = %s"
          data = (customer_id, first_name, )

          cursor.execute(delete_query, data)
          connection.commit()
          cursor.close()
          connection.close()

          msg= "Customer with ID {}, {} {} has been deleted.".format(customer_id, first_name, check[0]['LastName'])
       else:
          msg= "Customer with ID {}, {} {} not Found.".format(customer_id, first_name, last_name )
    return render_template('DeleteCustomer.html',msg=msg)
   except mysql.connector.Error as e:
    connection.rollback()
    msg= f"Sorry !! Failed Due to : {str(e)}"
    return render_template('DeleteCustomer.html',msg=msg)
  else:
   return redirect(url_for('home'))
@app.route('/remove_employee',methods=['POST','GET'])
def rem_Emp():
  user_name=session.get('user_id')
  if user_name:
   msg=''
   try:
    if request.method == 'POST':
       # Get the ID to delete from the form
       employee_id = request.form['id']
       first_name = request.form['first_name']
       last_name = request.form['last_name']

       # Delete the row from the MySQL database
       connection = mysql.connector.connect(**db_config)
       cursor = connection.cursor(dictionary=True)
       cursor.execute("select * from Employee where EmployeeID=%s",(int(employee_id),))
       check=cursor.fetchall()
       cursor.close()
       connection.close()
       if check[0]['EmployeeID']== int(employee_id):
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor(dictionary=True)
            delete_query = "DELETE FROM Emp_contact WHERE EmployeeID = %s"
            data = (employee_id,)
            cursor.execute(delete_query, data)
            connection.commit()

            delete_query = "DELETE FROM Employee WHERE EmployeeID = %s and FirstName = %s"
            data = (employee_id, first_name,)

            cursor.execute(delete_query, data)
            connection.commit()
            cursor.close()
            connection.close()

            msg= "Employee with ID {}, {} {} has been deleted.".format(employee_id, first_name, check[0]['LastName'])
       else:
            msg= "Employee with ID {}, {} {} not Found.".format(employee_id, first_name, last_name )
    return render_template('DeleteEmployee.html',msg=msg)
   except mysql.connector.Error as e:
    connection.rollback()
    msg= f"Sorry !! Failed Due to : {str(e)}"
    return render_template('DeleteEmployee.html',msg=msg)
  else:
   return redirect(url_for('home'))
@app.route('/transactions',methods=['POST','GET'])
def transaction():
   user_name=session.get('user_id')
   if user_name:
      msg=''
      try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Execute a query to fetch all rows from the table
        cursor.execute("select TransactionID, Date,Time,Quantity,TotalPrice,FuelType, EFN,  ELN,Customer.FirstName as CFN, Customer.LastName as CLN,Customer.CustomerID as CustID,EmpID,PumpID,PricePerLtr from Customer join (select TransactionID, Date,Time,CustomerID,Quantity,TotalPrice,FuelType,Employee.FirstName as EFN, Employee.LastName as ELN,Employee.EmployeeID as EmpID,PumpID, PricePerLtr from Employee join (SELECT TransactionID,Transaction.PumpID as PumpID, Date,Time,CustomerID,EmployeeID,Quantity,Quantity*PricePerLtr as TotalPrice,PricePerLtr,FuelType FROM Transaction join (select PumpID, FuelType,PricePerLtr from FuelPump join (select FuelTank.FuelType as FuelType,TankID,PricePerLtr  from FuelTank join Fuel on Fuel.FuelType=FuelTank.FuelType) as FuelTank on FuelPump.TankID=FuelTank.TankID) as A ON Transaction.PumpID = A.PumpID) as B on B.EmployeeID=Employee.EmployeeID) as C on C.CustomerID=Customer.CustomerID order by TransactionID DESC")

        # Fetch all rows as a list of dictionaries
        TR = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return render_template('Transaction.html', TR=TR, msg=msg)
      except mysql.connector.Error as e:
        connection.rollback()
        msg= f"Sorry !! Failed Due to: {str(e)}"
        return render_template('Transaction.html',msg=msg)
   else:
      return redirect(url_for('home'))
@app.route('/addTransaction',methods=['POST','GET'])
def addT():
  user_name=session.get('user_id')
  if user_name:
   msg=''
   try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select PumpID,FuelType from FuelPump join FuelTank on FuelPump.TankID=FuelTank.TankID order by PumpID")
    pumps = cursor.fetchall()
    cursor.close()
    connection.close()

    if request.method == 'POST':
        # Get form data
        customer_id = request.form['customer_id']
        employee_id = request.form['employee_id']
        PumpID =request.form['pump_id']
        quantity = request.form['quantity']

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        #check whether pump is active
        cursor.execute("select FuelTank.TankID as TID,FuelPump.Status as PumpStatus, FuelTank.Status as TankStatus,FuelTank.CurrentVolume as cv from FuelPump join FuelTank on FuelPump.TankID= FuelTank.TankID where PumpID = %s",(int(PumpID),))
        statuss = cursor.fetchall()
        if statuss[0]['PumpStatus']=='inactive' or statuss[0]['TankStatus']=='inactive':
            cursor.close()
            connection.close()
            msg="sorry! this Pump can not serve Temporarily. Try another..."
            return render_template('addTransaction.html',pumps=pumps,msg=msg)
        if statuss[0]['cv']<float(quantity):
            cursor.close()
            connection.close()
            msg=f"sorry! this Pump can serve Maximum {statuss[0]['cv']} Ltr"
            return render_template('addTransaction.html',pumps=pumps,msg=msg)
        cursor.execute("update FuelTank set CurrentVolume= CurrentVolume-%s where TankID=%s",(float(quantity),int(statuss[0]['TID'])))
        connection.commit()
        # Insert data into the MySQL database
        current_time = datetime.now()
        current_date = datetime.today().date()
        formatted_date = current_date.strftime('%Y-%m-%d')
        formatted_time = current_time.strftime('%H:%M:%S')
    #insert_query = "INSERT INTO Transaction( Date,Time,CustomerID, EmployeeID,PumpID,Quantity, TotalPrice) VALUES (%s,%s,%d,%d, %s, %s, %s)"
    #data = (formatted_date,formatted_time, customer_id, employee_id,PumpID, quantity, total_amount)
        insert_query = f"INSERT INTO Transaction (Date, Time, CustomerID, EmployeeID, PumpID, Quantity) VALUES ('{formatted_date}', '{formatted_time}', {customer_id}, {employee_id}, {PumpID}, {quantity})"

        cursor.execute(insert_query)
        connection.commit()
        cursor.execute("select LAST_INSERT_ID()")
        tID=cursor.fetchall()
        cursor.close()
        connection.close()

        msg=f"Transaction added Successfuly!!! with ID: {tID[0]['LAST_INSERT_ID()']}"
    return render_template('addTransaction.html',pumps=pumps,msg=msg)
   except mysql.connector.Error as e:
    connection.rollback()
    msg= f"Sorry !! Failed Due to : {str(e)}"
    return render_template('addTransaction.html',pumps=pumps,msg=msg)
  else:
   return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)
