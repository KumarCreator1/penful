import http.server
import socketserver
import json
import urllib.parse
import os
import io
import zipfile
from engine import build_pdf

PORT = 3000
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
PUBLIC_DIR = os.path.join(ROOT_DIR, 'public')

class FrontPageHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        rel = path.lstrip('/')
        if not rel or rel == 'index.html':
            return os.path.join(PUBLIC_DIR, 'index.html')
        return os.path.join(PUBLIC_DIR, rel)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode('utf-8'))
        except Exception:
            payload = {}

        if parsed.path == '/api/generate':
            template_key = payload.get('template', 'dsa').strip()
            name = payload.get('name', '').strip() or 'Sudhanshu Ranjan Adarsh'
            branch = payload.get('branch', '').strip()
            sem = payload.get('sem', '').strip() or '3rd Sem'
            roll_no = payload.get('roll_no', '').strip()
            id_label = payload.get('id_label', 'enr').strip().lower()
            id_label = 'roll' if id_label == 'roll' else 'enr'

            pdf_bytes = build_pdf(
                student_name=name,
                branch_name=branch,
                semester=sem,
                roll_no=roll_no,
                id_label=id_label,
                template_key=template_key
            )
            
            clean_filename = f"{name.replace(' ', '_')}_{template_key.upper()}_FrontPage.pdf"
            self.send_response(200)
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Disposition', f'attachment; filename="{clean_filename}"')
            self.send_header('Content-Length', str(len(pdf_bytes)))
            self.end_headers()
            self.wfile.write(pdf_bytes)
            return

        elif parsed.path == '/api/batch':
            template_key = payload.get('template', 'dsa').strip()
            students = payload.get('students', [])
            sem = payload.get('sem', '3rd Sem')
            branch = payload.get('branch', '')
            id_label = payload.get('id_label', 'enr').strip().lower()
            id_label = 'roll' if id_label == 'roll' else 'enr'
            
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
                        id_label=id_label,
                        template_key=template_key
                    )
                    filename = f"{(idx+1):02d}_{s_name.replace(' ', '_')}_{template_key.upper()}_FrontPage.pdf"
                    zip_file.writestr(filename, pdf_data)

            zip_bytes = zip_buffer.getvalue()
            self.send_response(200)
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Disposition', f'attachment; filename="{template_key.upper()}_FrontPages_Batch.zip"')
            self.send_header('Content-Length', str(len(zip_bytes)))
            self.end_headers()
            self.wfile.write(zip_bytes)
            return

        self.send_error(404)

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), FrontPageHandler) as httpd:
        print(f"FrontCraft server running at http://localhost:{PORT}")
        httpd.serve_forever()
