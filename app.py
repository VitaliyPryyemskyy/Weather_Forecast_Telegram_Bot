from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/classic")
def classic():
    return render_template('classic.html')


@app.route("/for_kids")
def for_kids():
    return render_template('for_kids.html')


@app.route("/non_alcohol")
def non_alcohol():
    return render_template('non_alcohol.html')


@app.route("/shots")
def shots():
    return render_template('shots.html')


@app.route("/handle_form", methods=['GET', 'POST'])
def handle_form():

    if request.method == 'POST':
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        with open('database.txt', 'r') as file:
            for line in file:
                if first_name in line and last_name in line:
                    return f"This name already taken {render_template('form.html')}"
        with open('database.txt', 'a') as file:
            file.write(f'\n{first_name} {last_name}\n')
        return f"{first_name}, {render_template('complete_registration.html')} "
    else:
        return render_template('form.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')

        with open('database.txt', 'r') as file:

            for line in file:

                if first_name in line and last_name in line:

                    return render_template('login.html', first_name=first_name)

            return render_template('login.html', error_message='wrong name')

    else:

        return render_template('login.html')
