from flask import Flask, request, jsonify
from extensions import db
from models import User
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.environ.get('MYSQL_USER')}:{os.environ.get('MYSQL_PASSWORD')}"
    f"@{os.environ.get('MYSQL_HOST')}/{os.environ.get('MYSQL_DB')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered")

@app.route('/api/users')
def get_users():
    users = User.query.all()
    return jsonify([u.username for u in users])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
