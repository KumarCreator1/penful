import json
import os
import sys
from http.server import BaseHTTPRequestHandler

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from engine import build_pdf

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        try:
            payload = json.loads(post_data.decode('utf-8'))
        except Exception:
            payload = {}

        template_key = payload.get('template', 'dsa').strip()
        name = payload.get('name', '').strip() or 'Sudhanshu Ranjan Adarsh'
        branch = payload.get('branch', '').strip()
        sem = payload.get('sem', '').strip() or '3rd Sem'
        roll_no = payload.get('roll_no', '').strip()
        id_label = payload.get('id_label', 'enr').strip().lower()
        id_label = 'roll' if id_label == 'roll' else 'enr'

        try:
            pdf_bytes = build_pdf(
                student_name=name,
                branch_name=branch,
                semester=sem,
                roll_no=roll_no,
                id_label=id_label,
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

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
