from flask import Flask, jsonify, send_file, render_template_string, request, redirect, Response
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configurações
PORTA = 5119
ARQUIVO_VERSOES = 'versoes.json'

def get_base_url():
    """
    Retorna a URL base dinâmica baseada no request
    """
    if request.headers.get('X-Forwarded-Host'):
        host = request.headers.get('X-Forwarded-Host')
    else:
        host = request.host

    scheme = 'https' if request.is_secure else 'http'
    return f"{scheme}://{host}"

def carregar_versoes():
    """
    Carrega as informações de versão do arquivo JSON
    """
    try:
        with open(ARQUIVO_VERSOES, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "versao_atual": "1.0.0",
            "nome_app": "bmdesk",
            "data_lancamento": datetime.now().strftime("%Y-%m-%d"),
            "changelog": ["Versão inicial"],
            "downloads": {}
        }

def salvar_versoes(dados):
    """
    Salva as informações de versão no arquivo JSON
    """
    with open(ARQUIVO_VERSOES, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

# Template HTML (mantém o mesmo)
HTML_DOWNLOAD = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ dados.nome_app }} - Download</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 30px auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .version-badge {
            background: rgba(255,255,255,0.2);
            padding: 10px 25px;
            border-radius: 25px;
            display: inline-block;
            font-size: 1.2em;
            font-weight: bold;
        }
        .content {
            padding: 40px;
        }
        .info-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .downloads {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .download-card {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s;
        }
        .download-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            border-color: #4CAF50;
        }
        .download-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        .platform-name {
            color: #333;
            font-size: 1.3em;
            font-weight: bold;
            margin: 10px 0;
        }
        .download-btn {
            background: #2196F3;
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            margin-top: 10px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .download-btn:hover {
            background: #0b7dda;
        }
        .file-info {
            font-size: 0.9em;
            color: #666;
            margin-top: 10px;
        }
        .changelog {
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .changelog h3 {
            color: #1976D2;
            margin-bottom: 15px;
        }
        .changelog ul {
            list-style-position: inside;
            color: #333;
        }
        .changelog li {
            padding: 5px 0;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ dados.nome_app }}</h1>
            <div class="version-badge">Versão {{ dados.versao_atual }}</div>
            <p style="margin-top: 15px; opacity: 0.9;">Lançado em {{ dados.data_lancamento }}</p>
        </div>

        <div class="content">
            <div class="info-box">
                <strong>ℹ️ Informação:</strong> Baixe a versão apropriada para seu dispositivo.
            </div>

            <h2>Downloads Disponíveis:</h2>
            <div class="downloads">
                {% if dados.downloads.windows %}
                <div class="download-card">
                    <div class="download-icon">🪟</div>
                    <div class="platform-name">{{ dados.downloads.windows.plataforma }}</div>
                    <div class="file-info">
                        {{ dados.downloads.windows.tamanho }}<br>
                        <small>{{ dados.downloads.windows.arquivo }}</small>
                    </div>
                    <a href="{{ base_url }}/releases/download/{{ dados.versao_atual }}/{{ dados.downloads.windows.arquivo }}" class="download-btn" download>📥 Baixar</a>
                </div>
                {% endif %}

                {% if dados.downloads.celular %}
                <div class="download-card">
                    <div class="download-icon">📱</div>
                    <div class="platform-name">{{ dados.downloads.celular.plataforma }}</div>
                    <div class="file-info">
                        {{ dados.downloads.celular.tamanho }}<br>
                        <small>{{ dados.downloads.celular.arquivo }}</small>
                    </div>
                    <a href="{{ base_url }}/releases/download/{{ dados.versao_atual }}/{{ dados.downloads.celular.arquivo }}" class="download-btn" download>📥 Baixar</a>
                </div>
                {% endif %}

                {% if dados.downloads.sunmi %}
                <div class="download-card">
                    <div class="download-icon">🏪</div>
                    <div class="platform-name">{{ dados.downloads.sunmi.plataforma }}</div>
                    <div class="file-info">
                        {{ dados.downloads.sunmi.tamanho }}<br>
                        <small>{{ dados.downloads.sunmi.arquivo }}</small>
                    </div>
                    <a href="{{ base_url }}/releases/download/{{ dados.versao_atual }}/{{ dados.downloads.sunmi.arquivo }}" class="download-btn" download>📥 Baixar</a>
                </div>
                {% endif %}
            </div>

            <div class="changelog">
                <h3>📋 Novidades da versão {{ dados.versao_atual }}:</h3>
                <ul>
                    {% for item in dados.changelog %}
                    <li>{{ item }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>

        <div class="footer">
            Servidor de Atualizações {{ dados.nome_app }}
        </div>
    </div>
</body>
</html>
"""

# API version
@app.route('/api/version', methods=['GET'])
def check_version():
    """
    Retorna informações sobre a versão mais recente
    """
    dados = carregar_versoes()
    if not dados:
        return jsonify({"error": "Erro ao carregar informações de versão"}), 500

    base_url = get_base_url()

    return jsonify({
        "version": dados['versao_atual'],
        "url": f"{base_url}/releases/tag/{dados['versao_atual']}",
        "changelog": "\n".join(dados['changelog']),
        "date": dados['data_lancamento'],
        "nome_app": dados['nome_app']
    })

# Latest release
@app.route('/releases/latest', methods=['GET', 'HEAD'])
def latest_release():
    """
    Simula a API do GitHub releases/latest
    """
    dados = carregar_versoes()
    if not dados:
        return jsonify({"error": "Erro ao carregar informações de versão"}), 500

    base_url = get_base_url()

    assets = []
    for plataforma, info in dados['downloads'].items():
        assets.append({
            "name": info['arquivo'],
            "browser_download_url": f"{base_url}/releases/download/{dados['versao_atual']}/{info['arquivo']}",
            "size": info.get('tamanho', 'N/A'),
            "content_type": "application/octet-stream"
        })

    return jsonify({
        "tag_name": dados['versao_atual'],
        "name": f"{dados['nome_app']} {dados['versao_atual']}",
        "published_at": dados['data_lancamento'],
        "body": "\n".join(dados['changelog']),
        "assets": assets,
        "html_url": f"{base_url}/releases/tag/{dados['versao_atual']}"
    })

# Tag (redireciona para download)
@app.route('/releases/tag/<version>', methods=['GET'])
def release_tag(version):
    """
    Redireciona para a página de download
    """
    base_url = get_base_url()
    return redirect(f"{base_url}/releases/download/{version}", code=302)

# Página de download da versão
@app.route('/releases/download/<version>', methods=['GET'])
def release_download_page(version):
    """
    Página HTML mostrando os downloads da versão
    """
    dados = carregar_versoes()
    if not dados:
        return "Erro ao carregar informações de versão", 500

    base_url = get_base_url()
    return render_template_string(HTML_DOWNLOAD, dados=dados, base_url=base_url)

# Download do arquivo - CORRIGIDO PARA CHROME
@app.route('/releases/download/<version>/<filename>', methods=['GET', 'HEAD'])
def download_file(version, filename):
    """
    Download dos instaladores - compatível com Chrome
    """
    arquivo = f"instaladores/{filename}"

    if not os.path.exists(arquivo):
        return f"Arquivo não encontrado: {filename}", 404

    # HEAD request
    if request.method == 'HEAD':
        file_size = os.path.getsize(arquivo)
        response = app.response_class()
        response.headers['Content-Length'] = str(file_size)
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Accept-Ranges'] = 'bytes'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        # Headers adicionais para Chrome
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response

    # GET request - com headers corretos para Chrome
    try:
        # Detecta o tipo de arquivo
        if filename.endswith('.exe'):
            mimetype = 'application/x-msdownload'
        elif filename.endswith('.apk'):
            mimetype = 'application/vnd.android.package-archive'
        else:
            mimetype = 'application/octet-stream'

        # Cria resposta com send_file
        response = send_file(
            arquivo,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )

        # Adiciona headers de segurança para Chrome
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

        # Se tiver range request (downloads parciais)
        if request.range:
            response.headers['Accept-Ranges'] = 'bytes'

        return response

    except Exception as e:
        return f"Erro ao baixar arquivo: {str(e)}", 500

# /download redireciona automaticamente para a versão mais recente
@app.route('/download', methods=['GET'])
def download_redirect():
    """
    Redireciona automaticamente para a versão mais recente
    """
    dados = carregar_versoes()
    if not dados:
        return "Erro ao carregar informações de versão", 500

    base_url = get_base_url()
    return redirect(f"{base_url}/releases/download/{dados['versao_atual']}", code=302)

# Página inicial
@app.route('/', methods=['GET'])
def index():
    """
    Página inicial
    """
    dados = carregar_versoes()
    if not dados:
        return "Erro ao carregar informações", 500

    base_url = get_base_url()

    return f"""
    <html>
    <head>
        <title>{dados['nome_app']} - Servidor de Atualizações</title>
        <style>
            body {{ 
                font-family: Arial; 
                max-width: 700px; 
                margin: 50px auto; 
                padding: 30px;
                background: #f5f5f5;
            }}
            .card {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{ color: #4CAF50; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
            a {{ 
                color: #2196F3; 
                text-decoration: none; 
                display: block;
                padding: 10px;
                margin: 5px 0;
                background: #e7f3ff;
                border-radius: 5px;
            }}
            a:hover {{ background: #cce7ff; }}
            .version {{ 
                background: #4CAF50; 
                color: white; 
                padding: 15px; 
                border-radius: 5px; 
                margin: 20px 0;
                font-size: 1.2em;
            }}
            .info {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 {dados['nome_app']} - Servidor de Atualizações</h1>
            <div class="version">📦 Versão Atual: <strong>{dados['versao_atual']}</strong></div>
            <p>🗓️ Lançado em: {dados['data_lancamento']}</p>

            <div class="info">
                <strong>🌐 URL Base:</strong> {base_url}<br>
                <strong>📱 Plataformas:</strong> Windows, Android, Sunmi
            </div>

            <h2>🔗 Links Disponíveis:</h2>
            <a href="/download">📥 Download (redireciona automaticamente)</a>
            <a href="/api/version">📋 API - Informações da Versão</a>
            <a href="/releases/latest">📋 API - Latest Release</a>

            <p style="margin-top: 30px; color: #666; font-size: 0.9em;">
                💡 Edite <code>versoes.json</code> para atualizar
            </p>
        </div>
    </body>
    </html>
    """

# Adicionar CORS se necessário (pode ajudar em alguns casos)
@app.after_request
def after_request(response):
    # Permite downloads de qualquer origem
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == '__main__':
    # Cria estrutura inicial
    if not os.path.exists('instaladores'):
        os.makedirs('instaladores')
        print(f"\n✅ Pasta 'instaladores' criada!")

    if not os.path.exists(ARQUIVO_VERSOES):
        dados_iniciais = {
            "versao_atual": "1.2.5",
            "nome_app": "bmdesk",
            "data_lancamento": datetime.now().strftime("%Y-%m-%d"),
            "changelog": [
                "Servidor customizado configurado",
                "Sistema de atualizações automáticas",
                "Suporte para Windows, Android e Sunmi"
            ],
            "downloads": {
                "windows": {
                    "arquivo": "bmdesk-1.2.5-x86_64.exe",
                    "tamanho": "45 MB",
                    "checksum": "",
                    "plataforma": "Windows"
                },
                "celular": {
                    "arquivo": "bmdesk-1.2.5-arm64-v8a.apk",
                    "tamanho": "35 MB",
                    "checksum": "",
                    "plataforma": "Android"
                },
                "sunmi": {
                    "arquivo": "bmdesk-1.2.5-sunmi-armeabi-v7a.apk",
                    "tamanho": "32 MB",
                    "checksum": "",
                    "plataforma": "Sunmi"
                }
            }
        }
        salvar_versoes(dados_iniciais)
        print(f"✅ Arquivo {ARQUIVO_VERSOES} criado!")

    dados = carregar_versoes()
    print(f"\n🚀 Servidor {dados['nome_app']} iniciando na porta {PORTA}...")
    print(f"🌐 Acesse: http://0.0.0.0:{PORTA}")
    print(f"📥 Download automático: /download")
    print(f"📱 Plataformas: Windows, Android, Sunmi\n")

    app.run(host='0.0.0.0', port=PORTA, debug=False, threaded=True)
