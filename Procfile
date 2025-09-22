# Streamlit Uygulaması için Procfile
# Bu dosya Streamlit Cloud'un uygulamanın nasıl çalıştırılacağını bilmesini sağlar
# Gunicorn ile dayanıklı web sunucusu kullanıyoruz
web: gunicorn -c gunicorn.conf.py --worker-class=uvicorn.workers.UvicornWorker --workers=1 --threads=2 --timeout=120 --keep-alive=60 --log-file=- --log-level=info app.wsgi:app