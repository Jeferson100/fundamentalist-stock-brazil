install:
	# Comando para atualizar pip e instalar dependências do arquivo requirements.txt
	# pip install --user -r requirements.txt
	pip install --upgrade pip && \
	pip install -r requirements.txt
format:
	black StockBrazil/*.py

lint:
	pylint --disable=R,C StockBrazil/*.py