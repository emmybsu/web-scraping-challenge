
#import necessary libraries
from flask import Flask, render_template

#create instance of Flask app
app = Flask(__name__)

#create route that renders index.html as template
@app.route('/')
def echo():
    return render_template('index.html', text = 'this is my initial flask file')


@app.route('/about')
def about():
    return render_template('index.html', text = 'something about me', another = "i'm a girl")


if __name__ == '__main__':
    app.run(debug=True)

