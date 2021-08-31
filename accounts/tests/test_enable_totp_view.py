from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account
from django.urls import reverse
from bs4 import BeautifulSoup
from cairosvg import svg2png
from PIL import Image
from pyzbar.pyzbar import decode
import pyotp
import pathlib


class TestEnableTOTPViewTestCase(TestCase):

    def setUp(self):
        user_a = User.objects.create(username='user_a')
        user_a.set_password('password_user_a')
        user_a.save()
        Account.objects.create(user=user_a)
        user_b = User.objects.create(username='user_b')
        user_b.set_password('password_user_b')
        user_b.save()
        Account.objects.create(
            user=user_b,
            use_totp=True, totp_key=pyotp.random_base32())

    def test_enable_totp_view_no_login(self):
        get_response = self.client.get(reverse('accounts:enable_totp'), follow=True)
        self.assertEquals(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'audio/index.html')
        self.assertEquals(get_response.request['PATH_INFO'], '/')

    def test_enable_totp_view_already_enabled(self):
        user_b = User.objects.get(username='user_b')
        current_totp_key = user_b.account.totp_key
        self.client.login(username='user_b', password='password_user_b')
        get_response = self.client.get(reverse('accounts:enable_totp'), follow=True)
        self.assertEquals(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'base_form.html')
        self.assertEquals(get_response.request['PATH_INFO'], '/accounts/edit-profile/')
        user_bb = User.objects.get(username='user_b')
        self.assertEquals(user_bb.account.totp_key, current_totp_key)

    def test_enable_totp_view_bad_data(self):
        self.client.login(username='user_a', password='password_user_a')
        response = self.client.post(reverse('accounts:enable_totp'), {
            'totp_code': '666666'}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/totp_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/enable-totp/')
        self.assertEquals(response.content.decode('utf-8').count("Wrong Code, try again"), 1)

    def test_enable_totp_view_no_data(self):
        self.client.login(username='user_a', password='password_user_a')
        response = self.client.post(reverse('accounts:enable_totp'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/totp_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/enable-totp/')
        self.assertEquals(response.content.decode('utf-8').count("This field is required."), 1)

    def test_enable_totp_view(self):
        self.client.login(username='user_a', password='password_user_a')
        get_response = self.client.get(reverse('accounts:enable_totp'))
        self.assertEquals(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'accounts/totp_form.html')
        self.assertEquals(get_response.request['PATH_INFO'], '/accounts/enable-totp/')
        soup = BeautifulSoup(get_response.content, features="lxml")
        svg_container = soup.find("div", {"id": "svgcontainer"})
        self.assertIsNotNone(svg_container)
        scsvg = svg_container.findChild("svg", recursive=False)
        self.assertIsNotNone(scsvg)
        with open('qr.svg', 'w') as f:
            f.write("<?xml version='1.0' encoding='utf-8'?>\n" + str(scsvg))
        svg2png(url='qr.svg', write_to='qr.png', scale=8)
        t_image = Image.open('qr.png')
        t_image.load()
        background = Image.new("RGB", t_image.size, (255, 255, 255))
        background.paste(t_image, mask=t_image.split()[3])
        background.save('qr.jpg', "JPEG", quality=100)
        image = Image.open('qr.jpg')
        img_data = decode(image)
        qr_data = img_data[0].data.decode("utf-8")
        totp_code = pyotp.TOTP(pyotp.parse_uri(qr_data).secret).now()
        response = self.client.post(reverse('accounts:enable_totp'), {
            'totp_code': totp_code}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/edit-profile/')
        user_a = User.objects.get(username='user_a')
        self.assertTrue(user_a.account.use_totp)
        self.assertEquals(len(user_a.account.totp_key), 32)
        pathlib.Path('qr.svg').unlink()
        pathlib.Path('qr.png').unlink()
        pathlib.Path('qr.jpg').unlink()
