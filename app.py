from flask import Flask,render_template,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class records(db.Model):

    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(500),nullable=False)
    birthday=db.Column(db.String(500),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"{self.name}-{self.birthday}"


    
@app.route('/', methods=['GET','POST'])
def entries():
    
    if request.method=='POST':
        
        name=request.form['person_name'] 
        birthday=request.form['person_birthday']
        collection=records(name=name, birthday=birthday)
        db.session.add(collection)
        db.session.commit()
    all_records=records.query.all()
    return render_template('index.html',all_records=all_records)



@app.route('/delete/<int:sno>')
def delete(sno):
    abc=records.query.filter_by(sno=sno).first()
    db.session.delete(abc)
    db.session.commit()
    return  redirect("/")



@app.route('/update/<int:sno>', methods=['get','post'])
def update(sno):
    if request.method=='POST':
        name=request.form['person_name'] 
        birthday=request.form['person_birthday'] 
        abc=records.query.filter_by(sno=sno).first()
        abc.name=name 
        abc.birthday=birthday 
        db.session.add(abc)
        db.session.commit()
        return redirect('/') 
    abc=records.query.filter_by(sno=sno).first()
    return render_template('update.html',abc=abc)

#rest api for this crud application

@app.route('/records')
def api_data():
    all_data=records.query.all()
    output=[]
    for data in all_data:
        my_api_data={"name":data.name, "birthday":data.birthday}
        output.append(my_api_data)
    return {"data":output}

@app.route('/records/<sno>')
def api_data_with_id(sno):
    all_data=records.query.get(sno)
    return {"name":all_data.name, "birthday":all_data.birthday}

        


if __name__== "__main__":
    app.run(debug=True)