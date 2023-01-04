

def test_get_all_board_with_no_records(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_one_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "board": {
            "title": "This is an inspiration board",
            # can we rename 'owners_name' to just 'owner'?
            "owners_name": "Curious Georges",
            "board_id": 1
        }
    }

# we need to build code to deal with requesting a board that doesn't exist
def test_get_board_not_found(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Board 1 not found"}, 404


# this test is failing because right now our post request returns the same info as our
# get request. We can change the post request to return a creation message
def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "My inspiration board",
        "owners name": "Curious Georges"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Board My inspiration board successfully created"


def test_create_board_missing_title(client):
    # Act
    response = client.post("/boards", json={
        "owners name": "Curious Georges"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"Error": "Please provide both the board title and owner's name"}


def test_create_board_missing_owner(client):
    # Act
    response = client.post("/boards", json={
        "title": "My board"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"Error": "Please provide both the board title and owner's name"}


# We can edit our post route to account for posts without a request body
def test_create_board_missing_body(client):
    # Act
    response = client.post("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"Error": "Please provide both the board title and owner's name"}


def test_get_all_cards_with_no_records(client):
	# Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# create tests to figure out the relationship between board and card- will try to imitate task list