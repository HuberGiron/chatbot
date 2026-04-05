# chatbot# Chatbot con Flask y Groq

## Ejecutar localmente

1. Crear entorno virtual

2. Instalar dependencias:
   pip install -r requirements.txt
   
3. Crear archivo .env a partir de .env.example
   venv\Scripts\activate
   cd venv\Scripts\activate
   python -m venv venv venv\Scripts\activate

4. Ejecutar:
   python app.py

## Producción en DigitalOcean

Usar:
gunicorn app:app

Variables:
- GROQ_API_KEY
- GROQ_MODEL