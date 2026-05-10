# Avila&Costa Gestão e Inovação em Saúde - Site Flask v2

MVP modular para Diagnóstico Inteligente da Clínica, com visual premium, Flask Application Factory, rotas separadas, dados dos blocos em módulo próprio, serviço de pontuação e banco SQLite.

## Instalação

```bash
python -m venv env
env\Scripts\activate
python -m pip install -r requirements.txt
python run.py
```

Acesse: http://127.0.0.1:5000

## Estrutura

```text
app/
  __init__.py
  database.py
  data/blocos.py
  routes/main.py
  services/scoring.py
templates/
  base.html
  index.html
  diagnostico.html
  resultado.html
  lista.html
  components/
static/
  css/main.css
  js/app.js
run.py
app.py
```
