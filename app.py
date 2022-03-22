from flask import Flask,render_template,url_for,request,session,redirect,send_file
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from sqlalchemy.sql.base import NO_ARG

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qvnrfnffgkatty:010e049a28d3e09951be0a387320b77acf3c1f3add6f99d3de5383f9bfb0c8c6@ec2-52-207-74-100.compute-1.amazonaws.com:5432/da7amva7esqbme"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'kreya22'
db = SQLAlchemy(app)


#------------------working function-------------------------------

def rollsort(lis):
    return lis[0]




#-----------------------------------------------------------------
class Sample(db.Model):

    __tablename__ = "festdata"
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50))
    rollno = db.Column(db.String(50))
    email = db.Column(db.String(50))
    refname = db.Column(db.String(50))
    refrollno = db.Column(db.String(50))
    


@app.route('/',methods = ["POST","GET"])
def index():

    if request.method == "POST":
        name = request.form["name"]
        rollno = request.form["rollno"]
        email = request.form["email"]
        refname = request.form["refname"]
        refrollno = request.form["refrollno"]
        a=str(refrollno).lower()
        b=str(a).upper()

        count=Sample.query.filter_by(refrollno=b).all()
        print(len(count))

        if len(count)==1 or len(count)==0 :

            details = Sample(name = name ,rollno=rollno, email=email, refname= refname,refrollno=b)

            db.session.add(details)
            db.session.commit()

            return redirect('https://docs.google.com/forms/d/e/1FAIpQLSeyhghgHwBK_rTVY2yI0xUIChPrgCoaxaQHgidf5t42iGg5Zw/viewform?usp=pp_url&entry.559352220='+str(name)+'&entry.721085583='+str(rollno)+'&entry.437505012='+str(refrollno)+'&entry.822335319='+str(refname))
        return render_template('index.html',msg="Reference is not available for "+str(b)+" .")


    

    #     return render_template('data_entry.html',message='record submitted',color='success')
    #https://docs.google.com/forms/d/e/1FAIpQLScbRRFySGjz2KPTfHtQQVnPmUP5tNSdhClWCJ6U6umUNJJu7g/viewform?usp=sf_link&entry.553411993=+str(name)+'&entry.1125976599='+str(rollno)+'&entry.801581831'+str(refrollno)+'&entry.822335319'+str(refname))

    # return render_template('data_entry.html')
    return render_template('index.html')


@app.route('/delete',methods =['GET','POST'])
def delete():
    db.session.query(Sample).delete()
    db.session.commit()
    return redirect('/')


@app.route('/details',methods =['GET'])
def details():
    data=Sample.query.all()
    l=list()
    for i in data:
        d=dict()
        lis=[str(i.refrollno),i]
        l.append(lis)
    # print(l)
    l.sort(key=lambda x: x[0])
    # print(l)
    # for i in l :
    #     print(i[1].refname)
        # print(i.refrollno)
    return render_template("details.html",data=l)


@app.route('/del/<val>',methods =['GET','POST'])
def delid(val):
    Sample.query.filter_by(id=val).delete()
    db.session.commit()
    return redirect('/details')

# @app.errorhandler(404) 
# def not_found(e):
#     return render_template("404.html") 
  




if __name__ == "__main__":
    db.create_all()
    
    app.run(debug=True)
