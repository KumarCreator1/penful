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
        # Serve static assets out of public/
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
            # Single PDF generation
            name = payload.get('name', '').strip() or 'Sudhanshu Ranjan Adarsh'
            branch = payload.get('branch', '').strip() or 'B.Tech. — Computer Science and Engineering'
            sem = payload.get('sem', '').strip() or '3rd Semester'

            pdf_bytes = build_pdf(student_name=name, branch_name=branch, semester=sem)
            
            clean_filename = f"{name.replace(' ', '_')}_DSA_FrontPage.pdf"
            self.send_response(200)
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Disposition', f'attachment; filename="{clean_filename}"')
            self.send_header('Content-Length', str(len(pdf_bytes)))
            self.end_headers()
            self.wfile.write(pdf_bytes)
            return

        elif parsed.path == '/api/batch':
            # Batch mode: list of students -> ZIP file
            students = payload.get('students', [])
            sem = payload.get('sem', '3rd Semester')
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for idx, s in enumerate(students):
                    s_name = s.get('name', '').strip()
                    s_branch = s.get('branch', '').strip()
                    if not s_name:
                        continue
                    pdf_data = build_pdf(student_name=s_name, branch_name=s_branch, semester=sem)
                    filename = f"{(idx+1):02d}_{s_name.replace(' ', '_')}_DSA_FrontPage.pdf"
                    zip_file.writestr(filename, pdf_data)

            zip_bytes = zip_buffer.getvalue()
            self.send_response(200)
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="FrontPages_Batch.zip"')
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
