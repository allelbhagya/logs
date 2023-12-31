@app.route('/home')
def index():
    return render_template('index.html',signals_data=sensor_data)

@app.route('/')
def auth():
    return render_template('auth.html')
