import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card

# # adding to try something
# from flask.signals import request_finished


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    # # adding to try something
    # @request_finished.connect_via(app)
    # def expire_session(sender, response, **extra): 
    #     db.session.remove()


    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


### creating model tables for our tests ###
@pytest.fixture
def one_board(app):
    example_board = Board(
        title="This is an inspiration board", owner="Curious Georges")
    db.session.add(example_board)
    db.session.commit()
