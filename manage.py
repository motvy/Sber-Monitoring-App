import config
from app import create_app, db

if __name__ == '__main__':
    app = create_app(config.ProdactionConfig)

    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5000)
