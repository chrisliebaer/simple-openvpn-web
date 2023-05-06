import string
import os
import json
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer



# configuration variables
LOGIN_FILE_PATH = os.environ.get('LOGIN_FILE_PATH', os.path.abspath('logins.txt'))
PAGE_TITLE = os.environ.get('PAGE_TITLE', 'Simple')
FILE_PERMISSIONS = int(os.environ.get('FILE_PERMISSIONS', '600'), 8)

VALID_PASSWORD_CHARS = string.ascii_letters + string.digits

def is_valid_username(username):
	return username.isalnum() and username.islower()

def is_valid_password(password):
	return all(char in VALID_PASSWORD_CHARS for char in password)
	

class LoginHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == '/logins':
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()

			with open(LOGIN_FILE_PATH, 'r') as file:
				logins = []
				for line in file:
					username, password = line.split(':')
					password = password[:-1]
					logins.append([username, password])

				self.wfile.write(json.dumps(logins).encode())
		elif self.path == '/':
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			with open('index.html', 'r') as file:
				page = file.read().replace('%TITLE%', PAGE_TITLE)
				self.wfile.write(page.encode())
		else:
			self.send_response(404)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			self.wfile.write(b'404 Not Found')

	def do_PUT(self):
		if self.path == '/login':
			content_length = int(self.headers['Content-Length'])
			body = self.rfile.read(content_length).decode()
			body = json.loads(body)
			username, password = body['username'], body['password']

			if not is_valid_username(username):
				self.send_response(400)
				self.send_header('Content-type', 'text/plain')
				self.end_headers()
				self.wfile.write(b'Username does not match the criteria')
				return
			if not is_valid_password(password):
				self.send_response(400)
				self.send_header('Content-type', 'text/plain')
				self.end_headers()
				self.wfile.write(b'Password does not match the criteria')
				return
			
			# update login atomically
			with open(LOGIN_FILE_PATH, 'r') as file:
				for line in file:
					if username == line.split(':')[0]:
						self.send_response(400)
						self.send_header('Content-type', 'text/plain')
						self.end_headers()
						self.wfile.write(b'Username already exists')
						return
			
			with tempfile.NamedTemporaryFile('w', suffix=".tmp", dir=os.path.dirname(LOGIN_FILE_PATH), delete=False) as temp_file:
				with open(LOGIN_FILE_PATH, 'r') as file:
					for line in file:
						temp_file.write(line)
					temp_file.write(username + ':' + password + '\n')
				temp_file.flush()
				os.chmod(temp_file.name, FILE_PERMISSIONS)
				os.rename(temp_file.name, LOGIN_FILE_PATH)

			self.send_response(200)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			self.wfile.write(b'Login created')
				
		else:
			self.send_response(404)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			self.wfile.write(b'404 Not Found')

	def do_PATCH(self):
		if self.path == '/login':
			content_length = int(self.headers['Content-Length'])
			body = self.rfile.read(content_length).decode()
			body = json.loads(body)
			username, password = body['username'], body['password']

			if not is_valid_username(username):
				self.send_response(400)
				self.send_header('Content-type', 'text/plain')
				self.end_headers()
				self.wfile.write(b'Username does not match the criteria')
				return
			if not is_valid_password(password):
				self.send_response(400)
				self.send_header('Content-type', 'text/plain')
				self.end_headers()
				self.wfile.write(b'Password does not match the criteria')
				return

			with tempfile.NamedTemporaryFile('w', suffix=".tmp", dir=os.path.dirname(LOGIN_FILE_PATH), delete=False) as temp_file:
				with open(LOGIN_FILE_PATH, 'r') as file:
					for line in file:
						if username == line.split(':')[0]:
							temp_file.write(username + ':' + password + '\n')
						else:
							temp_file.write(line)
				temp_file.flush()
				os.chmod(temp_file.name, FILE_PERMISSIONS)
				os.rename(temp_file.name, LOGIN_FILE_PATH)

			self.send_response(200)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			self.wfile.write(b'Login updated')

	def do_DELETE(self):
		if self.path == '/login':
			content_length = int(self.headers['Content-Length'])
			body = self.rfile.read(content_length).decode()
			body = json.loads(body)
			username = body['username']

			if not is_valid_username(username):
				self.send_response(400)
				self.send_header('Content-type', 'text/plain')
				self.end_headers()
				self.wfile.write(b'Username does not match the criteria')
				return

			with tempfile.NamedTemporaryFile('w', suffix=".tmp", dir=os.path.dirname(LOGIN_FILE_PATH), delete=False) as temp_file:
				with open(LOGIN_FILE_PATH, 'r') as file:
					for line in file:
						if username != line.split(':')[0]:
							temp_file.write(line)
				temp_file.flush()
				os.chmod(temp_file.name, FILE_PERMISSIONS)
				os.rename(temp_file.name, LOGIN_FILE_PATH)

			self.send_response(200)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			self.wfile.write(b'Login deleted')

def create_login_file():
	if not os.path.exists(LOGIN_FILE_PATH):
		with open(LOGIN_FILE_PATH, 'w') as file:
			pass
		permissions_octal = str(oct(FILE_PERMISSIONS))
		print('Login file not found. Creating new login file with path: ' + LOGIN_FILE_PATH + " and permissions: " + permissions_octal)
		os.chmod(LOGIN_FILE_PATH, FILE_PERMISSIONS)


# clean up in case of server crash
def delete_tmp_files():
	for file in os.listdir(os.path.dirname(LOGIN_FILE_PATH)):
		if file.endswith('.tmp'):
			os.remove(os.path.join(os.path.dirname(LOGIN_FILE_PATH), file))
	

def start_server():
	create_login_file()
	delete_tmp_files()
	server_address = ('', 8080)
	httpd = HTTPServer(server_address, LoginHandler)
	httpd.serve_forever()

if __name__ == '__main__':
	start_server()
