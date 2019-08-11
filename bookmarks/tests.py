from django.test import TestCase
from bookmarks.views import parse_meta


class IndexTest(TestCase):

    def test_index_view(self):
        response = self.client.get("/bookmarks/")
        self.assertEqual(response.status_code, 200)


class RegisterTest(TestCase):

    def test_register_view(self):
        response = self.client.get("/bookmarks/register/")
        self.assertEqual(response.status_code, 200)

    def test_new_user(self):
        data = {"name": "test", "password": "12345", "email": ""}
        response = self.client.post("/bookmarks/register/", data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User has been created")

    def test_existing_user(self):
        data = {"name": "", "password": "", "email": ""}
        response = self.client.post("/bookmarks/register/", data)
        self.assertContains(response, "Enter username")


class TestParse(TestCase):

    def test_parse_meta(self):
        meta = parse_meta("http://www.google.com")
        self.assertEqual(meta["title"], "Google")
        self.assertEqual(meta["description"],
                         "Поиск информации в интернете: веб страницы," +
                         " картинки, видео и многое другое.")
        self.assertEqual(meta["favicon"],
                         "http://www.google.com/images/branding/" +
                         "googleg/1x/googleg_standard_color_128dp.png")

        meta = parse_meta("https://stackoverflow.com")
        self.assertEqual(meta["title"],
                         "Stack Overflow - Where Developers " +
                         "Learn, Share, & Build Careers")
        self.assertEqual(meta["description"],
                         "Stack Overflow is the largest, most trusted online" +
                         " community for developers to learn, share​ ​their" +
                         " programming ​knowledge, and build their careers.")
        self.assertEqual(meta["favicon"],
                         "https://cdn.sstatic.net/Sites/" +
                         "stackoverflow/img/favicon.ico?v=4f32ecc8f43d")


class LoginTest(TestCase):

    def test_login_view(self):
        response = self.client.get("/bookmarks/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_no_name(self):
        data = {"name": "", "password": ""}
        response = self.client.get("/bookmarks/login/", data)
        self.assertContains(response, "Incorrect username or password")


class ShowTest(TestCase):

    def test_show_view(self):
        response = self.client.get("/bookmarks/show/")
        self.assertEqual(response.status_code, 200)


class AddTest(TestCase):

    def test_show_view(self):
        response = self.client.get("/bookmarks/show/")
        self.assertEqual(response.status_code, 200)
