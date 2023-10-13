import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


class ApiClient:
    apiKey = '20A19C979F42771B4FB5BD52E86ACAFBAD706A9B721B69648907D0FFAA5CA079B211B25B1A81F9726D6498A2D926D74F'
    apiUri = 'https://api.elasticemail.com/v2'

    def Request(method, url, data):
        data['apiKey'] = ApiClient.apiKey
        if method == 'POST':
            result = requests.post(ApiClient.apiUri + url, data=data)
        elif method == 'PUT':
            result = requests.put(ApiClient.apiUri + url, data=data)
        elif method == 'GET':
            attach = ''
            for key in data:
                attach = attach + key + '=' + data[key] + '&'
            url = url + '?' + attach[:-1]
            result = requests.get(ApiClient.apiUri + url)

        jsonMy = result.json()

        if jsonMy['success'] is False:
            return jsonMy['error']

        return 'Correo enviado con exito :D'


def Send(request):
    body_html = request.form.get('bodyHtml') or request.form.get('bodyHtml')

    return ApiClient.Request('POST', '/email/send', {
        'subject': request.form.get('subject'),
        'from': 'sponkurtus098@gmail.com',
        'fromName': 'Carlitos API',
        'to': request.form.get('to'),
        'bodyHtml': f'<h1>{body_html}</h1>',
        'bodyText': '',
        'isTransactional': False
    })


@app.route('/send-email', methods=['POST'])
def SendEmail():
    return Send(request)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
