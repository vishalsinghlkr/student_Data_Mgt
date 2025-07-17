
from src import create_app
from src.models import db
from src.auth import auth, login_manager 
# from flasgger import Swagger 

app = create_app()
login_manager.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
