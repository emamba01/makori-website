from flask import Flask, render_template,request,redirect

import psycopg2

app = Flask(__name__)

conn = psycopg2.connect("host='localhost' user='postgres'password='Emamba@39'dbname='my_shop'")


@app.route('/dashboard')
def dashboard():
    cur=conn.cursor()
    w="SELECT sum(products.selling_price * sales.quantity) as total, products.name from products join sales on products.id = sales.pid group by products.name;"
    cur.execute(w)
    v=cur.fetchall()
    labels=[]
    data=[]
    colours=[]
    for i in v:
        labels.append(i[1].split("-")[-1])
        data.append(i[0])
        colours.append("#3cba9f")
    return render_template('dashboard.html',colours=colours,label=labels,data=data)
    

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/sales')
def sales():
    cur=conn.cursor()
    o="SELECT *FROM sales;"
    cur.execute(o)
    t=cur.fetchall()
    q="select sales.sid,products.name,sales.quantity,(sales.created_at) from products join sales on products.id=sales.pid;"
    cur.execute(q)
    r =cur.fetchall()
    #print (r)
    
    s="select *from products;"
    cur.execute(s)
    p=cur.fetchall()
    return render_template('sales.html',rows=r,products=p,new=t)

@app.route('/products')
def products():
    cur=conn.cursor()
    q="SELECT *FROM products;"
    cur.execute(q)
    r =cur.fetchall()
    #print (r)
    return render_template('products.html',rows=r)

@app.route('/add_products',methods=['POST'])
def add_products():
    cur=conn.cursor()
    n=request.form['name']
    b=request.form['buying_price']
    c=request.form['selling_price']
    d=request.form['stock_quantity'] 
    
    data=(n,b,c,d)    
    q="insert into products(name,buying_price,selling_price,stock_quantity) values(%s,%s,%s,%s);"
    cur.execute(q,data)
    conn.commit()        
    return redirect('/products')

@app.route('/make_sale',methods=['POST'])
def add_sales():
    cur=conn.cursor()
    c=request.form('name')
    n=request.form['pid']
    b=request.form['quantity']
    sales=(c,n,b,'now()')    
    q="insert into sales(name,pid,quantity,created_at) values(%s,%s,%s,%s);"
    cur.execute(q,sales)
    conn.commit()        
    return redirect('/sales')


if __name__== "__main__":
    app.run(debug=True)

