from django.test			import TestCase
from django.core.files.base	import ContentFile
from PIL					import Image
from .models				import CustomUser
import io

class CustomUserManagerTests(TestCase):

	def setUp(self):
		self.user = CustomUser.objects.create_user(
			username='testuser',
			email='testuser@example.com',
			password='testpassword123'
		)
		self.superuser = CustomUser.objects.create_superuser(
			username='superuser',
			email='superuser@example.com',
			password='superpassword123'
		)

	def test_create_user(self):
		self.assertEqual(self.user.username, 'testuser')
		self.assertEqual(self.user.email, 'testuser@example.com')
		self.assertTrue(self.user.check_password('testpassword123'))
		self.assertFalse(self.user.is_staff)
		self.assertFalse(self.user.is_superuser)

	def test_create_superuser(self):
		self.assertEqual(self.superuser.username, 'superuser')
		self.assertEqual(self.superuser.email, 'superuser@example.com')
		self.assertTrue(self.superuser.check_password('superpassword123'))
		self.assertTrue(self.superuser.is_staff)
		self.assertTrue(self.superuser.is_superuser)

	def test_user_string_representation(self):
		self.assertEqual(str(self.user), 'testuser@example.com')
		self.assertEqual(str(self.superuser), 'superuser@example.com')

	def test_user_avatar_size(self):
		image = Image.new('RGB', (400, 400), color=(73, 109, 137))
		byte_arr = io.BytesIO()
		image.save(byte_arr, format='JPEG')

		self.user.avatar.save('test_avatar.jpg', ContentFile(byte_arr.getvalue()), save=True)
		self.user.save()

		img = Image.open(self.user.avatar.path)
		self.assertLessEqual(img.height, 300)
		self.assertLessEqual(img.width, 300)

class CustomUserModelTests(TestCase):

	def test_user_friends(self):
		user1 = CustomUser.objects.create_user(
			username='user1',
			email='user1@example.com',
			password='password123'
		)
		user2 = CustomUser.objects.create_user(
			username='user2',
			email='user2@example.com',
			password='password123'
		)
		user1.friends.add(user2)
		self.assertIn(user2, user1.friends.all())
		self.assertIn(user1, user2.friends.all())

	def test_win_lose_count(self):
		user = CustomUser.objects.create_user(
			username='testuser',
			email='testuser@example.com',
			password='password123'
		)
		self.assertEqual(user.win_count, 0)
		self.assertEqual(user.lose_count, 0)
		user.win_count += 1
		user.lose_count += 1
		user.save()
		self.assertEqual(user.win_count, 1)
		self.assertEqual(user.lose_count, 1)