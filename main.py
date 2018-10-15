from flask import Flask,request,redirect,render_template,session
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] =True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyNewPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body =db.Column(db.String(120))
   # exists=db.Column(db.Boolean)

    def __init__(self,title,body):
        self.title = title
        self.body = body
        #self.exists= True

    def __repr__(self):
        return '<Blog %r>' % self.title   

@app.route('/newpost')
def index():
    return render_template('Addblogentry.html')    

    
                   
@app.route('/newpost',methods= ['GET', 'POST'])
def newpost():
    t_error ='' 
    b_error =''   
    title =request.form['title']
    body =request.form['body']    
    if title == '':
        t_error ='please fill in the body'
    if body == '':
        b_error = 'please fill in the entry' 
    if title != '' and  body != '' :
        new_blog=Blog(title,body)  
        db.session.add(new_blog) 
        db.session.commit() 
        #print("$$"+str(new_blog.id))
        return redirect('/blog?id='+str(new_blog.id) )       
    else:        
        return render_template('Addblogentry.html',t_error=t_error,b_error=b_error)
@app.route('/blog')
def blogpost():
    if request.args.get('id') != None:
        indiv_id = request.args.get('id')
        #print("$$$$$"+indiv_id)
        blogs = Blog.query.get(indiv_id)
        return render_template('Individualentrypage.html',blogs=blogs)
    if request.args.get('id') == None:
        
        blogs = Blog.query.all()
        
        return render_template('Mainblogpage.html',blogs=blogs)


if __name__ == '__main__':
    app.run()

