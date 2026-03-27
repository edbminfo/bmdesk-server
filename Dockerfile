FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o servidor
COPY servidor_atualizacoes.py .

# Cria pastas necessárias
RUN mkdir -p instaladores

# Expõe a porta
EXPOSE 5119

# Comando para iniciar
CMD ["python", "servidor_atualizacoes.py"]
