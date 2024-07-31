from http.server import SimpleHTTPRequestHandler, HTTPServer
import sqlite3
import json
from urllib.parse import parse_qs
import os

# Database setup
def init_db():
    conn = sqlite3.connect('website.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS submissions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  email TEXT,
                  message TEXT)''')
    conn.commit()
    conn.close()

init_db()

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        fields = parse_qs(post_data)

        conn = sqlite3.connect('website.db')
        c = conn.cursor()
        c.execute("INSERT INTO submissions (name, email, message) VALUES (?, ?, ?)",
                  (fields.get('name', [''])[0], fields.get('email', [''])[0], fields.get('message', [''])[0]))
        conn.commit()
        conn.close()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({"status": "success", "message": "Submission received successfully!"})
        self.wfile.write(response.encode('utf-8'))

    def do_GET(self):
        if self.path == '/get_submissions':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            conn = sqlite3.connect('website.db')
            c = conn.cursor()
            c.execute("SELECT * FROM submissions")
            submissions = c.fetchall()
            conn.close()

            self.wfile.write(json.dumps(submissions).encode('utf-8'))
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

# Set up the server
PORT = 8000
Handler = MyHandler

# Change the current working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with HTTPServer(("", PORT), Handler) as httpd:
    print(f"Server running at <http://localhost>:{PORT}")
    httpd.serve_forever()
