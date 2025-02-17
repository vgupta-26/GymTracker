from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gymtracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    exercises = db.relationship('Exercise', back_populates='workout')

    def __repr__(self):
        return f"Workout: {self.exercises.name}"

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    workout = db.relationship('Workout', back_populates='exercises')

    def __repr__(self):
        return f"{self.name}: {self.sets} sets"

@app.route('/')
def index():
    workouts = Workout.query.all()
    return render_template('index.html', workouts=workouts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        exercisename = request.form['exercisename']
        workoutname = request.form['workoutname']
        workout = Workout(name=workoutname)
        exercise = Exercise(name=exercisename, sets=4, workout=workout)
        workout.exercises.append(exercise)
        db.session.add(workout)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    workout = Workout.query.filter_by(id=id).first()
    db.session.delete(workout)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    exercise = Exercise.query.get(id)
    workout = exercise.workout
    if request.method == 'POST':
        exercise.name = request.form['exercisename']
        workout.name = request.form['workoutname']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', exercise=exercise, workout=workout)

if __name__ == '__main__':
    app.run(debug=True)

