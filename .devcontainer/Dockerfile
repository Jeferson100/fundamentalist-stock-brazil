FROM selenium/standalone-chrome

COPY requirements.txt /tmp/

COPY Makefile /tmp/

USER root

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    make && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Inspecionar o conteúdo de /tmp
RUN ls -l /tmp/

# Instalar pacotes Python necessários
#RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    #&& apt-get install -y python3-pip \  
    #&& pip3 install --no-cache-dir -r /tmp/requirements.txt

USER seluser

# Definir o diretório de trabalho
WORKDIR /workspaces/fundamentalist-stock-brazil
