from app.models.board import Board


def test_get_all_board_with_no_records(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_boards_with_one_record(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "title": "This is an inspiration board",
            "owner": "Curious Georges",
            "board_id": 1
        }
    ]


def test_get_one_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "board": {
            "title": "This is an inspiration board",
            "owner": "Curious Georges",
            "board_id": 1
        }
    }


# to pass, change 'message' to 'error'
def test_get_nonexistent_board(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"error": "Board 1 not found"}, 404


# to pass, we can add quotes to message
def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "My inspiration board",
        "owner": "Curious Georges"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "message": "Board 'My inspiration board' successfully created",
        "board": {
            "title": "My inspiration board",
            "owner": "Curious Georges",
            "board_id": 1
        }
    }
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "My inspiration board"
    assert new_board.owner == "Curious Georges"
    assert new_board.board_id == 1


# to pass, we can change add 'with a title and owner' for continuity
def test_create_board_missing_body(client):
    # Act
    response = client.post("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"error": "Please include a request body with a title and owner"}


def test_create_board_missing_title(client):
    # Act
    response = client.post("/boards", json={
        "owner": "Curious Georges"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"error": "Please provide both the title and owner"}


def test_create_board_missing_owner(client):
    # Act
    response = client.post("/boards", json={
        "title": "My board"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"error": "Please provide both the title and owner"}


# to pass, we can rephrase the delete response
def test_delete_board(client, one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {"message": "Board 'This is an inspiration board' successfully deleted"}
    
    old_board = Board.query.get(1)
    assert not old_board


# to pass, change 'message' to 'error'
def test_delete_nonexistent_board(client):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"error": "Board 1 not found"}, 404