from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exitblogs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Blog(db.Model):
    sno= db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(500), nullable= False)
    author= db.Column(db.String(20), nullable= False)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} "

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "POST":
        title= request.form['title']
        content= request.form['content']
        author= request.form['author']
        blog=Blog(title=title, content=content, author=author)
        db.session.add(blog)
        db.session.commit()
    allBlogs= Blog.query.all()
    return render_template('index.html', allBlogs= allBlogs)
   
@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method== "POST":
        title= request.form['title']
        content= request.form['content']
        author= request.form['author']
        blog= Blog.query.filter_by(sno=sno).first()
        blog.title= title
        blog.desc= content
        blog.author= author
        db.session.add(blog)
        db.session.commit()
        return redirect("/")
    blog= Blog.query.filter_by(sno=sno).first()
    return render_template('update.html', blog= blog)

@app.route('/delete/<int:sno>', methods=['GET','POST'])
def delete(sno):
    blog= Blog.query.filter_by(sno=sno).first()
    db.session.delete(blog)
    db.session.commit()
    return redirect("/")

    



if __name__ == "__main__":
    app.run(debug=True, port=8000)
    