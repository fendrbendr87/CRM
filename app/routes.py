from app import app

@app.route('/')
@app.route('/index')
@login_required
def index():
    return "Hello, World!"
