from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Define the UserProfile model
class UserProfile(db.Model):
    __tablename__ = 'UserProfiles'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    activity_level = db.Column(db.String(50), nullable=False)

# Define the Preferences model
# class Preferences(db.Model):
#     __tablename__ = 'Preferences'
#     user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), primary_key=True)
#     dietary_preferences = db.Column(db.JSON, nullable=False)
#     emotional_goal = db.Column(db.String(150), nullable=False)


@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if username or email already exists
        existing_user = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()
        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 409
        
        # Create new user
        new_user = User(username=data['username'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': 'Registration successful',
            'user_id': new_user.user_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=data['email'], password=data['password']).first()
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        return jsonify({
            'message': 'Login successful',
            'user_id': user.user_id,
            'username': user.username
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['POST'])
def create_update_profile():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        # Validate required fields
        required_fields = ['age', 'gender', 'height', 'weight', 'activity_level']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if profile exists
        existing_profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        if existing_profile:
            # Update existing profile
            existing_profile.age = data['age']
            existing_profile.gender = data['gender']
            existing_profile.height = data['height']
            existing_profile.weight = data['weight']
            existing_profile.activity_level = data['activity_level']
        else:
            # Create new profile
            new_profile = UserProfile(
                user_id=user_id, age=data['age'], gender=data['gender'],
                height=data['height'], weight=data['weight'], activity_level=data['activity_level']
            )
            db.session.add(new_profile)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        if not profile:
            return jsonify({'message': 'Profile not found'}), 404
        
        return jsonify({
            'age': profile.age,
            'gender': profile.gender,
            'height': profile.height,
            'weight': profile.weight,
            'activity_level': profile.activity_level
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @app.route('/api/preferences', methods=['POST'])
# def update_preferences():
#     try:
#         data = request.get_json()
#         user_id = data.get('user_id')
        
#         if not user_id:
#             return jsonify({'error': 'user_id is required'}), 400
        
#         # Validate required fields
#         required_fields = ['dietary_preferences', 'emotional_goal']
#         for field in required_fields:
#             if field not in data:
#                 return jsonify({'error': f'Missing required field: {field}'}), 400
        
#         # Check if preferences exist
#         existing_prefs = Preferences.query.filter_by(user_id=user_id).first()
        
#         if existing_prefs:
#             # Update existing preferences
#             existing_prefs.dietary_preferences = data['dietary_preferences']
#             existing_prefs.emotional_goal = data['emotional_goal']
#         else:
#             # Create new preferences
#             new_prefs = Preferences(
#                 user_id=user_id,
#                 dietary_preferences=data['dietary_preferences'],
#                 emotional_goal=data['emotional_goal']
#             )
#             db.session.add(new_prefs)
        
#         db.session.commit()
        
#         return jsonify({
#             'message': 'Preferences updated successfully'
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/preferences/<int:user_id>', methods=['GET'])
# def get_preferences(user_id):
#     try:
#         preferences = Preferences.query.filter_by(user_id=user_id).first()
        
#         if not preferences:
#             return jsonify({
#                 'dietary_preferences': {},
#                 'emotional_goal': None
#             })
        
#         return jsonify({
#             'dietary_preferences': preferences.dietary_preferences,
#             'emotional_goal': preferences.emotional_goal
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
