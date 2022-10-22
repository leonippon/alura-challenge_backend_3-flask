from flask import session
import re


class TestUsers:
    def test_user_login_admin(self, client, auth):
        with client:
            # LOGIN
            auth.login()
            # IS LOGGED IN?
            assert session['user_logged'] == 'admin@email.com.br'


    def test_user_logout(self, client, auth):
        with client:
            # LOGIN
            auth.login()
            # IS LOGGED IN?
            assert session['user_logged'] == 'admin@email.com.br'
            # LOGOUT
            auth.logout()
            # IS LOGGED OUT?
            assert session['user_logged'] == None


    def test_user_list(self, client, auth):
        with client:
            # LOGIN
            auth.login()
            # LIST USERS
            response = client.get('/users', follow_redirects=True)
            text = response.get_data(as_text=True)
            # ASSERT USERS LISTED EXCEPT ADMIN
            assert 'admin@email.com.br' not in text
            assert 'user1@email.com.br' in text
            assert 'user2@email.com.br' in text
            assert 'user3@email.com.br' in text


    def test_user_create(self, client, auth):
        with client:
            # LOGIN
            auth.login()
            # CREATE USER
            response = client.post('/users', data={"username": "teste", "email": "teste@teste.com.br"})
            text = response.get_data(as_text=True)
            passwd = re.search("[0-9]{6}\" />", text)
            # LOGOUT
            auth.logout()
            assert session['user_logged'] == None
            # LOGIN NEW USER
            if passwd is not None:
                client.post("/auth", data={"username": "teste", "password": passwd[0][:6],  "from_page": "index"})
            else:
                return ('Error, passwd is type None!')
            assert session['user_logged'] == "teste@teste.com.br"
            # USER DOESN'T LIST ITSELF
            response = client.get('/users', follow_redirects=True)
            text = response.get_data(as_text=True)
            assert 'teste@teste.com.br' not in text


    def test_user_create_duplicate(self, client, auth):
        with client:
            # LOGIN
            auth.login()
            # CREATE REPEATED USERNAME
            client.post('/users', data={"username": "User1", "email": "other@email.com.br"})
            # CREATE REPEATED EMAIL
            client.post('/users', data={"username": "Other", "email": "user1@email.com.br"})
            # GET USER LIST
            response = client.get('/users')
            text = response.get_data(as_text=True)
            # ASSERT
            assert 'other@email.com.br' not in text
            assert 'Other' not in text


    def test_user_update(self, client, auth):
        with client:
            # LOGIN
            auth.login()
            # CHANGE USER EMAIL
            client.post('/user_details_update', data={"email": "other@email.com.br", "user_email": "user1@email.com.br"})
            # CANNOT CHANGE EMAIL TO DUPLICATE
            client.post('/user_details_update', data={"email": "user3@email.com.br", "user_email": "user2@email.com.br"})
            # CHANGE USERNAME
            client.post('/user_details_update', data={"username": "Other", "user_email": "user2@email.com.br"})
            # CANNOT CHANGE USERNAME TO DUPLICATE
            response = client.post('/user_details_update', data={"username": "Other", "user_email": "user1@email.com.br"})
            # CHANGE PASSWORD
            client.post('/user_details_update', data={"password": 123456, "user_email": "user3@email.com.br"})
            auth.logout()
            auth.login(username='User3', password=123456)
            # ASSERTS
            response = client.get('/users', follow_redirects=True)
            text = response.get_data(as_text=True)
            assert 'other@email.com.br' in text
            assert 'user2@email.com.br' in text
            assert 'Other' in text
            assert 'User1' in text
            assert session['user_logged'] == 'user3@email.com.br'


    def test_user_delete(self, client, auth):
        with client:
            # LOGIN
            auth.login(username='User3', password=123546)
            # CANNOT DELETE ITSELF
            client.post('/user_delete', data={"user_data": "user3@email.com.br"})
            # DELETE OTHER USER
            client.post('/user_delete', data={"user_data": "user2@email.com.br"})
            # CANNOT DELETE ADMIN
            client.post('/user_delete', data={"user_data": "admin@email.com.br"})
            auth.logout()
            auth.login()
            # ASSERTS
            response = client.get('/users', follow_redirects=True)
            text = response.get_data(as_text=True)
            assert 'user3@email.com.br' in text
            assert 'user2@email.com.br' not in text
            assert session['user_logged'] == 'admin@email.com.br'