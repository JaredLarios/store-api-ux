from app.common.token_schema import Token, AccessToken

test_data = {
    "iss": "www.sample.com",
    "sub" : "sample",
    "iat": 123123,
    "exp": 123123
}

def test_token_base():
    data = Token(
        sub=test_data["sub"],
        iss=test_data["iss"],
        iat=test_data["iat"],
        exp=test_data["exp"]
    )
    assert data == Token.model_validate(test_data)

def test_token_base():
    data = Token(
        sub=test_data["sub"],
        iss=test_data["iss"],
        iat=test_data["iat"],
        exp=test_data["exp"]
    )
    assert data == Token.model_validate(test_data)

def test_access_token():
    data = AccessToken(
        name="asd",
        role="asdf",
        sub=test_data["sub"],
        iss=test_data["iss"],
        iat=test_data["iat"],
        exp=test_data["exp"]
    )
    assert data != Token.model_validate(test_data)
