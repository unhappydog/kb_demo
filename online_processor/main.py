from rest_apps import create_app
import settings

app = create_app()

if __name__ == '__main__':
    app.run(host=settings.host, port=settings.port)
