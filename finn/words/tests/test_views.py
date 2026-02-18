from django.test import TestCase
from ..models import Word
from django.contrib.auth.models import User
from django.urls import reverse

class TestWordModel(TestCase):
    def setUp(self):
        u = User.objects.create_user(username='testuser', password='password67')
        Word.objects.create(eng='test', fin='testi', user=u)
        Word.objects.create(eng='cat', fin='kissa', user=u)
        Word.objects.create(eng='dog', fin='koira', user=u)

    def test_words_created(self):
        self.assertEqual(Word.objects.count(), 3)

    def test_words_contents(self):
        w = Word.objects.first()

        self.assertEqual(w.eng, 'test')
        self.assertEqual(w.fin, 'testi')
        self.assertEqual(str(w), w.eng)

class TestUserWordsView(TestCase):
    def setUp(self):
        self.u = User.objects.create_user(username='testuser', password='password67')
        self.url = reverse('home')

    def test_view_url_exists(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home.html')
        self.assertContains(res, 'Log in to view your words')

    def test_word_post(self):
        self.client.force_login(self.u)

        self.client.post(self.url, {
            'eng': 'test',
            'fin': 'testi'
        })

        self.assertEqual(Word.objects.count(), 1)
        self.assertEqual(self.u.word.count(), 1)

    def test_word_diaplay(self):
        words = []
        for i in range(0, 5):
            words.append(Word.objects.create(eng='test' + str(i), fin='testi' + str(i), user=self.u))
        
        self.client.force_login(self.u)
        res = self.client.get(self.url)
        self.assertEqual(self.u.word.count(), 5)
        
        for word in words:
            self.assertContains(res, word.eng)
            self.assertContains(res, word.fin)

class TestDeleteWordView(TestCase):
    def setUp(self):
        self.u = User.objects.create_user(username='testuser', password='password67')
        self.w = Word.objects.create(eng='test', fin='testi', user=self.u)

    def test_view_deletes_word(self):
        self.client.force_login(self.u)
        res = self.client.post('/word/delete/' + str(self.w.pk))

        self.assertEqual(res.status_code, 302)
        self.assertEqual(Word.objects.count(), 0)

class TestShuffledWordsView(TestCase):
    def setUp(self):
        self.u = User.objects.create_user(username='testuser', password='password67')
        for i in range(0, 5):
            Word.objects.create(eng='test' + str(i), fin='testi' + str(i), user=self.u)
        self.url = reverse('card')

    def test_view_url_exists(self):
        res = self.client.get('/card')

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'card.html')
        self.assertContains(res, 'Log in to view cards')

    def test_view_returns_user_words(self):
        self.client.force_login(self.u)
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, 200)
        self.assertIn('words', res.context)
        self.assertEqual(self.u.word.count(), len(res.context['words']))