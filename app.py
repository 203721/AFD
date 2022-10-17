from flask import Flask, render_template, send_file, redirect, flash, url_for, request
from wtforms import Form, StringField, validators
from bs4 import BeautifulSoup
from os import remove, listdir
import urllib.request
import re
import automaton

app = Flask(__name__)

app.secret_key = 'llave_secreta'


class UrlForm(Form):
    url = StringField('url', [validators.URL(
        require_tld=True, message=None)])


def generateFile(link):
    urls = []
    clean = "href=|\'|\""
    page = urllib.request.urlopen(link)
    html = page.read().decode('UTF-8')
    soup = BeautifulSoup(html, "html.parser")
    text = soup.title.string
    string = text.get_text()
    title = re.sub(r"[^a-zA-Z0-9 ]", "", string)
    found = automaton.executeAutomaton(html)
    for url in found:
        url = re.sub(clean, "", url)
        urls.append(url)
    with open(f"files/{title}.txt", "w") as file:
        file.write(f"ENLACES EXTERNOS ENCONTRADOS EN \"{title}\"\n\n")
        for line in urls:
            file.write(f"{line}\n")
    return file


def clean():
    path = ""
    files = "files/"
    dir = listdir(files)
    if dir:
        for file in dir:
            path = files + file
            remove(path)


@app.route('/', methods=['GET', 'POST'])
def front():
    data = ""
    form = UrlForm(request.form)
    if request.method == 'POST':
        data = form.url.data
        if form.validate():
            try:
                path = generateFile(data).name
                return send_file(path, as_attachment=True)
            except:
                flash('ERROR : Fallo de conexión o codificación', 'notify')
                flash(data, 'text')
                return redirect(url_for('front'))
        else:
            flash('ERROR : Por favor, ingresa una URL válida', 'notify')
            if data:
                flash(data, 'text')
            return redirect(url_for('front'))
    clean()
    return render_template('front.html')


def main():
    app.run(debug=True, port="5000", host="0.0.0.0")


if __name__ == "__main__":
    main()
