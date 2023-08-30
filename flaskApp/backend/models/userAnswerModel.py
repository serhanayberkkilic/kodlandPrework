from flaskApp.backend.config import db

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    userOption = db.Column(db.Integer, nullable=False)