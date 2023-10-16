from flask import Flask, request
import requests
from flask_httpauth import HTTPBasicAuth
import os


app = Flask(__name__)
auth = HTTPBasicAuth()

USERNAME = os.environ.get('SSRF_USERNAME', 'admin')
PASSWORD = os.environ.get('SSRF_PASSWORD', 'hacktricks')

def ssrf_html(text=""):
    return '''
    <html>
        <head>
            <title>SSRF Demo</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    background-color: #f9f9f9;
                }
                form {
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                input[type="text"] {
                    width: 300px;
                    padding: 10px;
                    margin-bottom: 10px;
                    border-radius: 4px;
                    border: 1px solid #ccc;
                }
                input[type="submit"] {
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    background-color: #008CBA;
                    color: #fff;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <form action="/fetch" method="get">
                <input type="text" name="url" placeholder="Enter URL to fetch" required>
                <input type="submit" value="Fetch">
            </form>
            <br>
            <br>
            <h3>__TEXT__</h3>
        </body>
    </html>
    '''.replace('__TEXT__', text)

@auth.verify_password
def verify_password(username, password):
    global USERNAME, PASSWORD
    return username == USERNAME and password == PASSWORD

@app.route('/')
@auth.login_required
def index():
    return ssrf_html()

@app.route('/fetch', methods=['GET', 'POST'])
@auth.login_required
def fetch_url():
    url = ""
    if request.method == 'GET':
        url = request.args.get('url')
    elif request.method == 'POST':
        url = request.form.get('url')

    if not url:
        return ssrf_html('Please provide a URL')

    try:
        response = requests.get(url)
        return f'<pre>{response.text}</pre>'
    except:
        return ssrf_html('Unable to fetch URL')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=45380)
