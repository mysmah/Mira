# Global Database
# version 0.0.1

_DATABASE = None

import logging
import sqlite3

class _databased:
	def __init__(self):
		self.db = sqlite3.connect('database.mira')
		self.api = self.db.cursor()
		self.queue = []

		api = self.api
		api.execute('CREATE TABLE if not exists rules (name text, value integer)')
		api.execute('CREATE TABLE if not exists listen_to(id integer)')

	async def a_queue(self, ):
		pass
	def add_to_wlist(self, target_id):
		self.api.execute('SELECT * FROM listen_to WHERE id = ?', (target_id, ))
		if self.api.fetchall():
			return -1
		try:
			self.api.execute('INSERT INTO listen_to VALUES (?)', (target_id,))
			self.db.commit()
		except Exception:
			return -2
		return self.get_wlist()
	def get_wlist(self):
		self.api.execute('SELECT id FROM listen_to')
		prelist = self.api.fetchall()
		lisst = []
		for i in prelist:
			lisst.append(i[0])
		return lisst
	def remove_from_wlist(self, target_id):
		self.api.execute('SELECT * FROM listen_to WHERE id = ?', (target_id, ))
		if not self.api.fetchall():
			return -1
		try:
			self.api.execute('DELETE FROM listen_to WHERE id = ?', (target_id,))
			self.db.commit()
		except Exception:
			return -2
		return self.get_wlist()
	def clear_wlist(self):
		try:
			self.api.execute('DELETE FROM listen_to')
		except Exception:
			return -2
		self.db.commit()
		return []
	def close(self):
		global _DATABASE
		_DATABASE = None
		self.db.commit()
		self.db.close()
		del self


def INITIALIZATE():
	global _DATABASE
	if _DATABASE:
		return -1
	_DATABASE = _databased()
	return _DATABASE