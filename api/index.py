import json
import urllib.parse
import os
import sys
import io
import zipfile
from http.server import BaseHTTPRequestHandler

# Ensure project root & src/ are in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
SRC_DIR = os.path.join(ROOT_DIR, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from engine import build_pdf

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        try:
            payload = json.loads(post_data.decode('utf-8'))
        except Exception:
            payload = {}

        path = parsed.path.rstrip('/')
        
        # Route 1: /api/generate
        if path.endswith('/generate') or path == '/api/generate':
            template_key = payload.get('template', 'dsa').strip()
            name = payload.get('name', '').strip() or 'Sudhanshu Ranjan Adarsh'
            branch = payload.get('branch', '').strip()
            sem = payload.get('sem', '').strip() or '3rd Sem'
            roll_no = payload.get('roll_no', '').strip()

            try:
                pdf_bytes = build_pdf(
                    student_name=name,
                    branch_name=branch,
                    semester=sem,
                    roll_no=roll_no,
                    template_key=template_key
                )
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                return
            
            clean_filename = f"{name.replace(' ', '_')}_{template_key.upper()}_FrontPage.pdf"
            self.send_response(200)
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Disposition', f'attachment; filename="{clean_filename}"')
            self.send_header('Content-Length', str(len(pdf_bytes)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(pdf_bytes)
            return

        # Route 2: /api/batch
        elif path.endswith('/batch') or path == '/api/batch':
            template_key = payload.get('template', 'dsa').strip()
            students = payload.get('students', [])
            sem = payload.get('sem', '3rd Sem')
            branch = payload.get('branch', '')
            
            try:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for idx, s in enumerate(students):
                        s_name = s.get('name', '').strip()
                        s_branch = s.get('branch', branch).strip()
                        s_roll = s.get('roll_no', '').strip()
                        if not s_name:
                            continue
                        pdf_data = build_pdf(
                            student_name=s_name,
                            branch_name=s_branch,
                            semester=sem,
                            roll_no=s_roll,
                            template_key=template_key
                        )
                        filename = f"{(idx+1):02d}_{s_name.replace(' ', '_')}_{template_key.upper()}_FrontPage.pdf"
                        zip_file.writestr(filename, pdf_data)

                zip_bytes = zip_buffer.getvalue()
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                return

            self.send_response(200)
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Disposition', f'attachment; filename="{template_key.upper()}_FrontPages_Batch.zip"')
            self.send_header('Content-Length', str(len(zip_bytes)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(zip_bytes)
            return

        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
