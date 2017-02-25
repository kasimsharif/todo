from flask import Flask , render_template , request , url_for , redirect
import sqlite3

def init_db():
    try:
        conn = sqlite3.connect('todo.db')
        print "Opened database successfully";
        conn.execute('CREATE TABLE lists (id INTEGER PRIMARY KEY autoincrement , name TEXT NOT NULL )')
        print "Table created successfully";
        conn.close()
    except:
        print "Table already exist"

app = Flask(__name__)

@app.route('/')
def listall():
    init_db()
    con = sqlite3.connect("todo.db")
    print "Open connection"
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from lists")

    result = cur.fetchall();
    print "result"+str(result);
    return  render_template('listall.html', list=result)

@app.route('/newitem')
def newitem():
    return render_template('newitem.html')

@app.route('/additem',methods= ['POST','GET'])
def additem():
    if request.method == 'POST':
        try:
            item = request.form['item']
            print "item : "+item;
            with sqlite3.connect("todo.db") as con:
                print "Inside con :  "
                cur = con.cursor()
                print "Inside cursor :  "
                cur.execute("INSERT INTO lists(name) VALUES ('%s')" % (item))
                print "Inserted row"
                con.commit()
        except:
            print "Rollback"
            con.rollback()
        finally:
            return redirect('/')

@app.route('/deleteitem',methods=['POST','GET'])
def deleteitem():
    if request.method == 'POST':
        try:
            itemid = request.form['listid']
            print itemid
            print "item : "+itemid;
            with sqlite3.connect("todo.db") as con:
                print "Inside con :  "
                cur = con.cursor()
                print "Inside delete cursor :  "
                print "DELETE from lists where id = %s" % (itemid)
                cur.execute("DELETE from lists where id = %s" % (itemid))
                print "deleted row"
                con.commit()
        except:
            print "Rollback"
            con.rollback()
        finally:
            return redirect('/')

@app.route('/showitem/<id>')
def showitem(id):
    try:
        with sqlite3.connect("todo.db") as con:

            print "Inside select cursor :  "
            print "SELECT NAME from lists where id = %s" % (id)
            cur = con.execute("SELECT NAME from lists where id = %s" % (id))
            print "Execute select query %s " %(cur)
            for row in cur:
                print "Item Name : %s " % row[0]
                name = row[0]
    except:
        print "Rollback"
        con.rollback()
    finally:
        return render_template('showitem.html',itemid=id,itemname=name)

@app.route('/updateitem',methods=['POST','GET'])
def updateitem():
    if request.method == 'POST':
        try:
            itemid = request.form['itemid']
            itemname = request.form['itemname']
            print itemid
            print "item : "+itemid;
            with sqlite3.connect("todo.db") as con:
                print "Inside con :  "
                cur = con.cursor()
                print "Inside update cursor :  "
                print "UPDATE lists SET name = \"%s\" where id = %s" % (itemname,itemid)
                cur.execute("UPDATE lists SET name = \"%s\" where id = %s" % (itemname,itemid))
                print "update row"
                con.commit()
        except:
            print "Rollback"
            con.rollback()
        finally:
            return redirect('/')

if __name__ == '__main__':
    app.run()
