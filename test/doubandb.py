import unittest
import sys
sys.path.append('..')
from app.main.DBdata import logindb

class DoubanDBTestCase():

	def test_firstpage(self):
		db= logindb.douban_robot()
		print db.get_firstpage()
