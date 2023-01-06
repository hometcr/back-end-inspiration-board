from app.models.board import Board
from app.models.card import Card


def test_get_all_cards_with_no_records(client):
	# Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_cards_with_one_record(client, one_card_belongs_to_one_board):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "card_id": 1,
            "board_id": 1,
            "message": "This is an inspirational card",
            "likes_count": 0
        }
    ]

    this_board = Board.query.get(1)
    this_card = Card.query.get(1)
    assert this_board.cards == [this_card]


def test_get_one_card(client, one_card_belongs_to_one_board):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "card": {
            "card_id": 1,
            "board_id": 1,
            "message": "This is an inspirational card",
            "likes_count": 0
        }
    }


# to pass, change 'message' to 'error'
def test_get_one_nonexistant_card(client):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"error": "Card 1 not found"}, 404


# to pass, add message to response
def test_create_card(client, one_board):
    # Act
    response = client.post("/cards", json={
        "message": "I feel inspired",
        "board_id": 1
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "message": "Card I feel inspired successfully created", 
        "card": {
            "message": "I feel inspired",
            "board_id": 1,
            "card_id": 1,
            "likes_count": 0
        }
    }

    new_card = Card.query.get(1)
    this_board = Board.query.get(1)

    assert new_card.message == "I feel inspired"
    assert new_card.board_id == 1
    assert new_card.card_id == 1
    assert new_card.likes_count == 0

    assert this_board.cards == [new_card]


def test_create_card_missing_body(client, one_board):
    # Act
    response = client.post("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"error": "Please include a request body with a message and board id"}


def test_create_card_missing_board_id(client, one_board):
    # Act
    response = client.post("/cards", json={
        "message": 1
    })
    response_body = response.get_json()

    # Assert 
    assert response.status_code == 400
    assert response_body == {"error": "Please provide a message and board id"}


def test_create_card_missing_message(client, one_board):
    # Act
    response = client.post("/cards", json={
        "board_id": 1
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"error": "Please provide a message and board id"}


# def test_create_card_to_nonexistent_board(client):

