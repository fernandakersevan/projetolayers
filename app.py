from flask import Flask, request, redirect, render_template_string
import re, json, os, random, string
import requests

# Para criar a aplicação da web
app = Flask(__name__)

# Variável para a URL base
BASE_URL = "http://localhost:5000"

# Arquivo para armazenar URLs encurtadas
URL_FILE = "urls.json"

# Função para gerar um ID aleatório
def generate_random_id(length=6):
    characters = string.ascii_letters + string.digits + '_-'
    return ''.join(random.choice(characters) for _ in range(length))

# Função para carregar URLs do arquivo
def load_urls():
    if os.path.exists(URL_FILE):  # Verifica se o arquivo de URLs existe
        with open(URL_FILE, 'r') as file:  # Abre o arquivo em modo de leitura
            return json.load(file)  # Carrega e retorna o conteúdo do arquivo como uma lista de URLs
    return []  # Retorna uma lista vazia se o arquivo não existir

# Função para salvar URLs no arquivo
def save_urls(url_list):
    with open(URL_FILE, 'w') as file:  # Abre o arquivo em modo de escrita
        json.dump(url_list, file)  # Converte a lista de URLs para JSON e salva no arquivo

# Carregar URLs do arquivo
url_list = load_urls()

# Função para validar a string do link encurtado
def is_valid_short_id(short_id):
    return re.match("^[a-zA-Z0-9_-]+$", short_id) is not None  # Verifica se o ID encurtado contém apenas caracteres permitidos

# Função para verificar se a URL é válida
def is_url_valid(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

@app.route('/', methods=['GET', 'POST'])  # Define a rota principal que aceita métodos GET e POST
def home():
    if request.method == 'POST':  # Se o método da requisição for POST
        original_url = request.form['url']  # Obtém a URL original do formulário
        short_id = request.form['short_id'].strip()  # Obtém o ID encurtado do formulário e remove espaços em branco

        if not short_id:  # Se o ID encurtado estiver vazio, gera um ID aleatório
            short_id = generate_random_id()

        # Verifica se a URL é válida
        if not is_url_valid(original_url):
            return render_template_string('''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Encurtador de Links</title>
                    <style> 
                        body { font-family: Helvetica, sans-serif; margin: 0; padding: 0; background-color: #000000; color: #009bb5; } 
                        .container { width: 50%; margin: auto; overflow: hidden; padding: 20px; background: #ffffff; margin-top: 50px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
                        h1 { text-align: center; color: #009bb5; }
                        form { display: flex; flex-direction: column; }
                        input[type="text"] { padding: 10px; margin-bottom: 10px; border: 1px solid #009bb5; border-radius: 4px; background-color: #ffffff; color: #009bb5; }
                        input[type="submit"] { padding: 10px; background: #009bb5; color: #ffffff; border: none; border-radius: 4px; cursor: pointer; }
                        input[type="submit"]:hover { background: #007b8f; }
                        .result { margin-top: 20px; }
                        .button { display: inline-block; padding: 10px 20px; background-color: #009bb5; color: #ffffff; border: none; border-radius: 4px; text-align: center; cursor: pointer; }
                        .button:hover { background-color: #007b8f; }
                        .error { color: #ff0000; font-size: 16px; text-align: center; margin-top: 20px; }
                    </style> 
                </head>
                <body>
                    <div class="container"> 
                        <h1>Encurtador de Links</h1> 
                        <form method="post"> 
                            URL: <input type="text" name="url" required> 
                            ID Encurtado: <input type="text" name="short_id" placeholder="Opcional" value="{{ short_id }}"> 
                            <input type="submit" value="Encurtar"> 
                        </form> 
                        <div class="result"> 
                            <p class="error">URL não encontrada. Tente novamente.</p>
                            <p><a href="/list" class="button">Ver todas as URLs</a></p>
                        </div>
                    </div>
                </body>
                </html>
            ''', base_url=BASE_URL, short_id=short_id)

        if not is_valid_short_id(short_id):  # Verifica se o ID encurtado é válido
            return render_template_string('''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Encurtador de Links</title>
                    <style> 
                        body { font-family: Helvetica, sans-serif; margin: 0; padding: 0; background-color: #000000; color: #009bb5; } 
                        .container { width: 50%; margin: auto; overflow: hidden; padding: 20px; background: #ffffff; margin-top: 50px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
                        h1 { text-align: center; color: #009bb5; }
                        form { display: flex; flex-direction: column; }
                        input[type="text"] { padding: 10px; margin-bottom: 10px; border: 1px solid #009bb5; border-radius: 4px; background-color: #ffffff; color: #009bb5; }
                        input[type="submit"] { padding: 10px; background: #009bb5; color: #ffffff; border: none; border-radius: 4px; cursor: pointer; }
                        input[type="submit"]:hover { background: #007b8f; }
                        .result { margin-top: 20px; }
                        a { color: #009bb5; text-decoration: none; }
                        a:hover { text-decoration: underline; }
                        .button { display: inline-block; padding: 10px 20px; background-color: #009bb5; color: #ffffff; border: none; border-radius: 4px; text-align: center; cursor: pointer; }
                        .button:hover { background-color: #007b8f; }
                        .copy-button { display: inline-block; padding: 10px 20px; background-color: #009bb5; color: #ffffff; border: none; border-radius: 4px; text-align: center; cursor: pointer; }
                        .copy-button:hover { background-color: #007b8f; }
                        .error { color: #ff0000; font-size: 16px; text-align: center; margin-top: 20px; }
                    </style> 
                </head>
                <body>
                    <div class="container"> 
                        <h1>Encurtador de Links</h1> 
                        <form method="post"> 
                            URL: <input type="text" name="url" required> 
                            ID Encurtado: <input type="text" name="short_id" placeholder="Opcional" value="{{ short_id }}"> 
                            <input type="submit" value="Encurtar"> 
                        </form> 
                        <div class="result"> 
                            <p class="error">ID inválido. Use apenas letras, números, hífens e underscores.</p>
                            <p><a href="/list" class="button">Ver todas as URLs</a></p>
                        </div>
                    </div>
                </body>
                </html>
            ''', base_url=BASE_URL, short_id=short_id)

        for url in url_list:  # Verifica se o ID encurtado já existe
            if url['short_id'] == short_id:
                return render_template_string('''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Encurtador de Links</title>
                        <style> 
                            body { font-family: Helvetica, sans-serif; margin: 0; padding: 0; background-color: #000000; color: #009bb5; } 
                            .container { width: 50%; margin: auto; overflow: hidden; padding: 20px; background: #ffffff; margin-top: 50px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
                            h1 { text-align: center; color: #009bb5; }
                            form { display: flex; flex-direction: column; }
                            input[type="text"] { padding: 10px; margin-bottom: 10px; border: 1px solid #009bb5; border-radius: 4px; background-color: #ffffff; color: #009bb5; }
                            input[type="submit"] { padding: 10px; background: #009bb5; color: #ffffff; border: none; border-radius: 4px; cursor: pointer; }
                            input[type="submit"]:hover { background: #007b8f; }
                            .result { margin-top: 20px; }
                            a { color: #009bb5; text-decoration: none; }
                            a:hover { text-decoration: underline; }
                            .button { display: inline-block; padding: 10px 20px; background-color: #009bb5; color: #ffffff; border: none; border-radius: 4px; text-align: center; cursor: pointer; }
                            .button:hover { background-color: #007b8f; }
                            .copy-button { display: inline-block; padding: 10px 20px; background-color: #009bb5; color: #ffffff; border: none; border-radius: 4px; text-align: center; cursor: pointer; }
                            .copy-button:hover { background-color: #007b8f; }
                            .error { color: #ff0000; font-size: 16px; text-align: center; margin-top: 20px; }
                        </style> 
                    </head>
                    <body>
                        <div class="container"> 
                            <h1>Encurtador de Links</h1> 
                            <form method="post"> 
                                URL: <input type="text" name="url" required> 
                                ID Encurtado: <input type="text" name="short_id" placeholder="Opcional" value="{{ short_id }}"> 
                                <input type="submit" value="Encurtar"> 
                            </form> 
                            <div class="result"> 
                                <p class="error">O ID encurtado já existe. Escolha outro.</p>
                                <p><a href="/list" class="button">Ver todas as URLs</a></p>
                            </div>
                        </div>
                    </body>
                    </html>
                ''', base_url=BASE_URL, short_id=short_id)

        url_list.append({'original_url': original_url, 'short_id': short_id, 'access_count': 0})
        save_urls(url_list)

        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Encurtador de Links</title>
                <style> 
                    body { font-family: Helvetica, sans-serif; margin: 0; padding: 0; background-color: #000000; color: #009bb5; } 
                    .container { width: 50%; margin: auto; overflow: hidden; padding: 20px; background: #ffffff; margin-top: 50px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
                    h1 { text-align: center; color: #009bb5; }
                    form { display: flex; flex-direction: column; }
                    input[type="text"] { padding: 10px; margin-bottom: 10px; border: 1px solid #009bb5; border-radius: 4px; background-color: #ffffff; color: #009bb5; }
                    input[type="submit"] { padding: 10px; background: #009bb5; color: #ffffff; border: none; border-radius: 4px; cursor: pointer; }
                    input[type="submit"]:hover { background: #007b8f; }
                    .result { margin-top: 20px; }
                    a { color: #009bb5; text-decoration: none; }
                    a:hover { text-decoration: underline; }
                    .button { display: inline-block; padding: 10px 20px; background-color: #009bb5; color: #ffffff; border: none; border-radius: 4px; text-align: center; cursor: pointer; }
                    .button:hover { background-color: #007b8f; }
                    .copy-button { display: inline-block; padding: 10px 20px; background-color: #009bb5; color: #ffffff; border: none; border-radius: 4px; text-align: center; cursor: pointer; }
                    .copy-button:hover { background-color: #007b8f; }
                </style> 
            </head>
            <body>
                <div class="container"> 
                    <h1>Encurtador de Links</h1> 
                    <div class="result" align="center"> 
                        <p>URL encurtada: <a href="{{ base_url }}/{{ short_id }}" target="_blank">{{ base_url }}/{{ short_id }}</a></p>
                        <button class="copy-button" onclick="copyToClipboard('{{ base_url }}/{{ short_id }}')">Copiar</button>
                        <p><a href="/list" class="button">Ver todas as URLs</a></p>
                        <p><a href="/" class="button">Voltar à página inicial</a></p>
                        <script>
                            function copyToClipboard(text) {
                                navigator.clipboard.writeText(text).then(function() {
                                    alert('Link copiado para a área de transferência!');
                                }, function(err) {
                                    console.error('Erro ao copiar para a área de transferência: ', err);
                                });
                            }
                        </script>
                    </div>
                </div>
            </body>
            </html>
        ''', base_url=BASE_URL, short_id=short_id)

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Encurtador de Links</title>
            <style> 
                body { font-family: Helvetica, sans-serif; margin: 0; padding: 0; background-color: #000000; color: #009bb5; } 
                .container { width: 50%; margin: auto; overflow: hidden; padding: 20px; background: #ffffff; margin-top: 50px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
                h1 { text-align: center; color: #009bb5; }
                form { display: flex; flex-direction: column; }
                input[type="text"] { padding: 10px; margin-bottom: 10px; border: 1px solid #009bb5; border-radius: 4px; background-color: #ffffff; color: #009bb5; }
                input[type="submit"] { padding: 10px; background: #009bb5; color: #ffffff; border: none; border-radius: 4px; cursor: pointer; }
                input[type="submit"]:hover { background: #007b8f; }
                .result { margin-top: 20px; }
                a { color: #009bb5; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .button { display: inline-block; padding: 10px 20px; background-color: #009bb5; color: #ffffff; border: none; border-radius: 4px; text-align: center; cursor: pointer; }
                .button:hover { background-color: #007b8f; }
                .copy-button { display: inline-block; padding: 10px 20px; background-color: #009bb5; color: #ffffff; border: none; border-radius: 4px; text-align: center; cursor: pointer; }
                .copy-button:hover { background-color: #007b8f; }
            </style> 
        </head>
        <body>
            <div class="container"> 
                <h1>Encurtador de Links</h1> 
                <form method="post"> 
                    URL: <input type="text" name="url" required> 
                    ID Encurtado: <input type="text" name="short_id" placeholder="Opcional"> 
                    <input type="submit" value="Encurtar"> 
                </form> 
                <div class="result"> 
                    <p><a href="/list" class="button">Ver todas as URLs</a></p>
                </div>
            </div>
        </body>
        </html>
    ''')

@app.route('/<short_id>', methods=['GET'])
def redirect_to_url(short_id):
    for url in url_list:
        if url['short_id'] == short_id:
            url['access_count'] += 1
            save_urls(url_list)
            return redirect(url['original_url'])

    return "URL não encontrada"

@app.route('/list', methods=['GET'])
def list_urls():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lista de URLs Encurtadas</title>
            <style> 
                body { font-family: Helvetica, sans-serif; margin: 0; padding: 0; background-color: #000000; color: #009bb5; } 
                .container { width: 50%; margin: auto; overflow: hidden; padding: 20px; background: #ffffff; margin-top: 50px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
                h1 { text-align: center; color: #009bb5; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border: 1px solid #009bb5; text-align: left; }
                th { background-color: #009bb5; color: #ffffff; }
                tr:nth-child(even) { background-color: #f2f2f2; }
                a { color: #009bb5; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .button { display: inline-block; padding: 10px 20px; background-color: #009bb5; color: #ffffff; border: none; border-radius: 4px; text-align: center; cursor: pointer; }
                .button:hover { background-color: #007b8f; }
                .copy-button { display: inline-block; padding: 10px 20px; background-color: #009bb5; color: #ffffff; border: none; border-radius: 4px; text-align: center; cursor: pointer; }
                .copy-button:hover { background-color: #007b8f; }
            </style> 
        </head>
        <body>
            <div class="container"> 
                <h1>Lista de URLs Encurtadas</h1> 
                <table>
                    <thead>
                        <tr>
                            <th>URL Original</th> <!--mudar isso-->
                            <th>URL Encurtada</th>
                            <th>Acessos</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for url in url_list %}
                            <tr>
                                <td>{{ url.original_url }}</td>
                                <td><a href="{{ base_url }}/{{ url.short_id }}" target="_blank">{{ base_url }}/{{ url.short_id }}</a></td>
                                <td>{{ url.access_count }}</td>
                                <td>
                                    <button class="copy-button" onclick="copyToClipboard('{{ base_url }}/{{ url.short_id }}')">Copiar</button>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
                <p><a href="/" class="button">Voltar à página inicial</a></p>
                <script>
                    function copyToClipboard(text) {
                        navigator.clipboard.writeText(text).then(function() {
                            alert('Link copiado para a área de transferência!');
                        }, function(err) {
                            console.error('Erro ao copiar para a área de transferência: ', err);
                        });
                    }
                </script>
            </div>
        </body>
        </html>
    ''', url_list=url_list, base_url=BASE_URL)

if __name__ == '__main__':
    app.run(debug=True)
