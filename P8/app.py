from flask import Flask, render_template

# This project keeps its CSS and images beside the templates, so make that
# directory available at Flask's normal /static URL.
app = Flask(__name__, static_folder='templates', static_url_path='/static')

@app.route('/')
def home():
    skills = ['Python', 'HTML', 'CSS', 'Flask']
    return render_template('home.html', nama='Dewi Idda', skills=skills)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
