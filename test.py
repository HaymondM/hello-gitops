from app import app

with app.test_client() as client:
    response = client.get('/')
    print(response.get_data(as_text=True))