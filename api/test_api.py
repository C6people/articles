import requests

base_url = "http://localhost:8000"

# 1. Signup
signup_data = {"name": "testuser_post", "password": "password123"}
r_signup = requests.post(f"{base_url}/auth/signup", json=signup_data)
print("Signup:", r_signup.status_code, r_signup.text)

# 2. Login
login_data = {"name": "testuser_post", "password": "password123"}
r_login = requests.post(f"{base_url}/auth/login", json=login_data)
print("Login:", r_login.status_code, r_login.text)

token = r_login.json().get("token")
if token:
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Post article
    article_data = {"title": "My Article", "body": "Hello World", "category": "プログラミング"}
    r_article = requests.post(f"{base_url}/articles", json=article_data, headers=headers)
    print("Post Article:", r_article.status_code, r_article.text)
    
    # 4. Post question
    question_data = {"title": "My Question", "body": "Help me"}
    r_question = requests.post(f"{base_url}/questions", json=question_data, headers=headers)
    print("Post Question:", r_question.status_code, r_question.text)
else:
    print("No token received")
