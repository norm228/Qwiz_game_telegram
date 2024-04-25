from random import choice, shuffle

import flask
from flask import jsonify, request, make_response

from .user import User
from . import db_session
from .question import Question

blueprint = flask.Blueprint(
    'qwiz_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/quest/<int:level>', methods=['POST', 'GET'])
def quest(level):
    if request.method == 'GET':
        db_sess = db_session.create_session()
        questions = db_sess.query(Question).filter(Question.level == level, Question.id.notin_(
            request.json['ids'])).all()
        if not questions:
            return make_response(jsonify({'error': 'Not found'}), 404)
        question = choice(questions)
        print(question.id)
        a = question.answers.split('|')
        shuffle(a)
        return jsonify(
            {
                'id': question.id,
                'text': question.question,
                'answers': a,
                'r_answer': question.r_answer[1:-1],
                'type': question.type,
                'photo': question.photo
            }
        )
    if request.method == 'POST':
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in
                     ['title', 'content', 'user_id', 'is_private']):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        db_sess = db_session.create_session()
        qwest = Question(
            question=request.json['question'],
            level=request.json['level'],
            answers='|'.join(request.json['answers']),
            r_answer=request.json['r_answer'],
            type=request.json['type'],
            photo=request.json['photo']
        )
        db_sess.add(qwest)
        db_sess.commit()
        return jsonify({'id': qwest.id})


@blueprint.route('/api/user/<int:user_id>', methods=['GET', 'POST'])
def user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.user_id == user_id).first()
    if not user:
        user = User(
            user_id=user_id,
            account=0
        )
        db_sess.add(user)
        db_sess.commit()
    if request.method == 'GET':
        return make_response({
            'money': user.account
        })
    if request.method == 'POST':
        user.account += request.json['money']
        db_sess.commit()
        return {'success': 'OK'}
