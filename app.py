from flask import Flask, render_template, send_file, redirect, flash, url_for, request
from wtforms import Form, StringField, validators
from bs4 import BeautifulSoup
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
    #clean = "href=|\'|\""
    clean = "\'|\""
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
                flash('No se puede acceder al sitio', 'notify')
                flash(data, 'text')
                return redirect(url_for('front'))
        else:
            flash('Por favor, ingresa una URL válida', 'notify')
            if data:
                flash(data, 'text')
            return redirect(url_for('front'))
    return render_template('front.html')


def main():
    app.run(debug=True, port="5000", host="0.0.0.0")


if __name__ == "__main__":
    main()
