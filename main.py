from flask import Flask, request, redirect, render_template  #, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:pass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    story = db.Column(db.String(500))

    def __init__(self, title, story):
        self.title = title
        self.story = story


@app.route('/')
def index():
    #return render_template('blog.html')
    return redirect ('/blog')


@app.route('/blog')
def blog():

    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)


@app.route('/add-blog', methods=['POST', 'GET'])
def add_blog():

    if request.method == 'POST':

        name = request.form['blog_name']
        storys = request.form['add_blog']

        error_blog_name = ''
        error_blog_story = ''
        error = 0

        if len(name) == 0:
            error_blog_name = 'invaled title'
            error = error + 1
        else:
            error_blog_name = ''

        if len(storys) == 0:
            error_blog_story = 'invaled blog'
            error = error + 1
        else:
            error_blog_story = ''

        if error > 0:
            return render_template('add-blog.html', 
            error_blog_name=error_blog_name, 
            error_blog_story=error_blog_story, blog_name=name, add_blog=storys)

        else:
            new_blog = Blog(name, storys)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('blog-temo.html')

    return render_template('add-blog.html')


@app.route('/blog-temo')
def blog_temo():

    #blog_id = int(request.form['blog-id'])
    #blog = Blog.query.get(blog_id)
    #db.session.add(blog)
    #db.session.commit()

    return render_template('blog-temo.html')

if __name__ == '__main__':
    app.run()