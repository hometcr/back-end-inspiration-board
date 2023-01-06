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


def test_get_one_nonexistant_card(client):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Card 1 not found"}, 404