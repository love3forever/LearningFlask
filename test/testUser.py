import unittest
import sys
sys.path.append('..')
from app.main import models


class UserTestCase(unittest.TestCase):
	'''def test_query(self):
					qury={'username':'wm'}
					self.assertEqual(models.User.query(qury).id,1)'''

	def test_commit(self):
		import forgery_py
		from random import randint
		email = forgery_py.internet.email_address()
		username = forgery_py.internet.user_name(True)
		data = {"id":randint(1, 10000),
				"email":email,
				"username":username,
				"password":forgery_py.lorem_ipsum.word(),
				"location":forgery_py.address.city(),
				"about_me":forgery_py.lorem_ipsum.sentence()
			}
		models.User.commit(data)
		self.assertEqual(models.User.query(data).email,email)



if __name__=='__main__':
	#unittest.main()
	import forgery_py
	from random import randint
	email = forgery_py.internet.email_address()
	username = forgery_py.internet.user_name(True)
	id = randint(1,10000)
	print id
	u = models.User(
			email=email,
			username=username,
			password=forgery_py.lorem_ipsum.word(),
			location=forgery_py.address.city(),
			about_me=forgery_py.lorem_ipsum.sentence())
	print type(u.data)
	print u.data['id']
	u.commit(u.data)
