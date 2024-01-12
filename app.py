from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def show_logs():
    logs = []
    with open('log.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if "Success" in line:
                logs.append(f'{line}')
            elif "Failed" in line:
                logs.append(f'{line}')
            elif "In progress" in line:
                logs.append(f'{line}')
            else:
                logs.append(f'{line}')
    return render_template('index.html', logs=logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)