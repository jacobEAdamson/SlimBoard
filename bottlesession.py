#!/usr/bin/env python
#
#  Bottle session manager.  See README for full documentation.
#
#  Written by: Sean Reifschneider <jafo@tummy.com>

from __future__ import with_statement

import bottle


def authenticator(session_manager, login_url = '/auth/login'):
	'''Create an authenticator decorator.

	:param session_manager: A session manager class to be used for storing
			and retrieving session data.  Probably based on :class:`BaseSession`.
	:param login_url: The URL to redirect to if a login is required.
			(default: ``'/auth/login'``).
	'''
	def valid_user(login_url = login_url):
		def decorator(handler, *a, **ka):
			import functools
			@functools.wraps(handler)
			def check_auth(*a, **ka):
				try:
					data = session_manager.get_session()
					if not data['valid']: raise KeyError('Invalid login')
				except (KeyError, TypeError):
					bottle.response.set_cookie('validuserloginredirect',
							bottle.request.fullpath, path = '/')
					bottle.redirect(login_url)

				#  set environment
				if data.get('name'):
					bottle.request.environ['REMOTE_USER'] = data['name']
				else:
					bottle.request.environ['REMOTE_USER'] = None

				return handler(*a, **ka)
			return check_auth
		return decorator
	return(valid_user)


import pickle, os, uuid

class BaseSession(object):
	'''Base class which implements some of the basic functionality required for
	session managers.  Cannot be used directly.

	:param cookie_expires: Expiration time of session ID cookie, either `None`
			if the cookie is not to expire, a number of seconds in the future,
			or a datetime object.  (default: 30 days)
	'''
	def __init__(self, cookie_expires = 86400*30):
		self.cookie_expires = cookie_expires

	def load(self, sessionid):
		raise NotImplementedError

	def save(self, sessionid, data):
		raise NotImplementedError

	def make_session_id(self):
		return str(uuid.uuid4())

	def allocate_new_session_id(self):
		#  retry allocating a unique sessionid
		for i in range(100):
			sessionid = self.make_session_id()
			if not self.load(sessionid): return sessionid
		raise ValueError('Unable to allocate unique session')

	def get_session(self):
		#  get existing or create new session identifier
		sessionid = bottle.request.COOKIES.get('sessionid')
		if not sessionid:
			sessionid = self.allocate_new_session_id()
			bottle.response.set_cookie('sessionid', sessionid,
					path = '/')

		#  load existing or create new session;
		#  field 'new' indicates which of these two happened
		data = self.load(sessionid)
		if not data:
			data = { 'sessionid' : sessionid, 'valid' : False, 'new': True }
			self.save(data)
		else:
			data['new'] = False
			self.save(data)

		return data


class PickleSession(BaseSession):
	'''Class which stores session information in the file-system.

	:param session_dir: Directory that session information is stored in.
			(default: ``'/tmp'``).
	'''
	def __init__(self, session_dir = '/tmp', *args, **kwargs):
		super(PickleSession, self).__init__(*args, **kwargs)
		self.session_dir = session_dir

	def load(self, sessionid):
		filename = os.path.join(self.session_dir, 'session-%s' % sessionid)
		if not os.path.exists(filename): return None
		with open(filename, 'r') as fp: session = pickle.load(fp)
		return session

	def save(self, data):
		sessionid = data['sessionid']
		fileName = os.path.join(self.session_dir, 'session-%s' % sessionid)
		tmpName = fileName + '.' + str(uuid.uuid4())
		with open(tmpName, 'w') as fp: self.session = pickle.dump(data, fp)
		os.rename(tmpName, fileName)


class MemorySession(BaseSession):
	'''Class which stores session information in the server memory.
	'''
	def __init__(self, *args, **kwargs):
		super(MemorySession, self).__init__(*args, **kwargs)
		self.sessions = dict()

	def load(self, sessionid):
		if not sessionid in self.sessions: return None
		return self.sessions[sessionid]

	def save(self, data):
		sessionid = data['sessionid']
		self.sessions[sessionid] = data

class PreconfiguredSession(BaseSession):
	'''Class which always returns same session data, given in initializer.

	:param session_data: the session data to return, always.
			(default: None)
	'''
	def __init__(self, session_data = None, *args, **kwargs):
		super(PreconfiguredSession, self).__init__(*args, **kwargs)
		self.session_data = session_data

	def get_session(self):
		return self.session_data

	def load(self, sessionid):
		return self.session_data

	def save(self, data):
		self.session_data = data

class CookieSession(BaseSession):
	'''Session manager class which stores session in a signed browser cookie.

	:param cookie_name: Name of the cookie to store the session in.
			(default: ``session_data``)
	:param secret: Secret to be used for "secure cookie".  If ``None``,
			a random secret will be generated and written to a temporary
			file for future use.  This may not be suitable for systems which
			have untrusted users on it.  (default: ``None``)
	:param secret_file: File to read the secret from.  If ``secret`` is
			``None`` and ``secret_file`` is set, the first line of this file
			is read, and stripped, to produce the secret.
	'''

	def __init__(self, secret = None, secret_file = None,
			cookie_name = 'session_data', *args, **kwargs):
		super(CookieSession, self).__init__(*args, **kwargs)
		self.cookie_name = cookie_name

		if not secret and secret_file is not None:
			with open(secret_file, 'r') as fp:
				secret = fp.readline().strip()

		if not secret:
			import string, random, tempfile, sys

			tmpfilename = os.path.join(tempfile.gettempdir(),
					'%s.secret' % os.path.basename(sys.argv[0]))
			print(tmpfilename)
			
			if os.path.exists(tmpfilename):
				with open(tmpfilename, 'r') as fp:
					secret = fp.readline().strip()
			else:
				#  save off a secret to a tmp file
				secret = ''.join([ random.choice(string.ascii_letters)
								for x in range(32) ])

				"""old_umask = os.umask(077)"""
				with open(tmpfilename, 'w') as fp:
					fp.write(secret)
				"""os.umask(old_umask)"""

		self.secret = secret

	def load(self, sessionid):
		cookie = bottle.request.get_cookie(self.cookie_name, secret = self.secret)
		if cookie == None: return {}
		return pickle.loads(cookie)

	def save(self, data):
		bottle.response.set_cookie(self.cookie_name, pickle.dumps(data),
				secret = self.secret, path = '/')
