from flask import Blueprint, request, jsonify, make_response
from app import db

from .models.board import Board 
from .models.card import Card 

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# Returns all boards
@boards_bp.route("", methods=["GET"]) 
def get_all_boards():
    board_query = Board.query
    boards = board_query.all()
    boards_response = [board.create_dict() for board in boards]
    return jsonify(boards_response), 200

# Returns a single board with a given board_id 
@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board_query = Board.query
    board = board_query.get(board_id) 
    return {"board": board.create_dict()}, 200

# Posts a board when there is a title and owner's name
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json(force=True) 
    if not "title" in request_body or not "owners name" in request_body:
        return {"Error": "Please provide both the board title and owner's name"}, 400
    new_board = Board(title=request_body["title"], owners_name=request_body["owners name"] )
    db.session.add(new_board)
    db.session.commit()
    return {"board": new_board.create_dict()}, 201

# Delete a board 
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board_query = Board.query
    board = board_query.get(board_id)

    db.session.delete(board)
    db.session.commit()

    return {"details": f"Board {board_id} {board.title} successfully deleted"}, 200

# Returns all cards (or use query parameter to return cards with a given board_id [note])
@cards_bp.route("", methods=["GET"])
def get_all_cards():
    board_query = request.args.get("board_id")
    if board_query:
        cards = Card.query.filter_by(board_id=board_query)
    else:
        cards = Card.query.all()
    cards_response = [card.create_dict() for card in cards]
    return jsonify(cards_response), 200
    
# Returns single card with a given card_id number
@cards_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card_query = Card.query
    card = card_query.get(card_id)
    return {"card": card.create_dict()}, 200

# Posts a card when there is a likes count, a message, and a board_id
@cards_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json(force=True) 
    if not "likes count" in request_body or not "message" or not "board id" in request_body:
        return {"Error": "Please provide a likes count, message and board id"}, 400
    new_card = Card(likes_count=request_body["likes count"], message=request_body["message"], board_id=request_body["board id"] )
    db.session.add(new_card)
    db.session.commit()
    return {"card": new_card.create_dict()}, 201

# Delete a card
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card_query = Card.query
    card = card_query.get(card_id)

    db.session.delete(card)
    db.session.commit()

    return {"details": f"Card {card_id} successfully deleted"}, 200

