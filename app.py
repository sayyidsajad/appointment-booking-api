from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, time, timedelta
from models import db, Appointment
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

db.init_app(app)

with app.app_context():
    db.create_all()

BREAK_START = time(13, 0)
BREAK_END = time(14, 0)

def generate_slots():
    slots = []
    current = time(10, 0)
    end = time(17, 0)
    while current < end:
        if not (BREAK_START <= current < BREAK_END):
            slots.append(current.strftime('%H:%M'))
        current = (datetime.combine(datetime.today(), current) + timedelta(minutes=30)).time()
    return slots

@app.route('/api/available-slots', methods=['GET'])
def get_slots():
    date = request.args.get('date')
    all_slots = generate_slots()
    booked_slots = [a.time_slot for a in Appointment.query.filter_by(date=date).all()]
    available = [s for s in all_slots if s not in booked_slots]
    return jsonify(available)

@app.route('/api/book', methods=['POST'])
def book_slot():
    data = request.json or {}

    required_fields = ['name', 'phone', 'date', 'time_slot']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    if Appointment.query.filter_by(date=data['date'], time_slot=data['time_slot']).first():
        return jsonify({'error': 'Slot already booked'}), 400

    appointment = Appointment(
        name=data['name'],
        phone=data['phone'],
        date=data['date'],
        time_slot=data['time_slot']
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)