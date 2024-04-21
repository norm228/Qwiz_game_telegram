from flask import Flask, make_response, jsonify

from data import db_session, qwiz_api
from db import DataB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qqweertty_secret_key'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/data_for_game.db")
    app.register_blueprint(qwiz_api.blueprint)
    DataB()
    app.run(port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()
