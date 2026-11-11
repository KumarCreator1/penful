import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from engine import build_pdf

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

test_cases = [
    {
        "name": "Vicky Kumar",
        "branch": "B.Tech. — Computer Science and Engineering (AIML)",
        "sem": "3rd Semester",
        "out": "vicky_aiml.pdf"
    },
    {
        "name": "Rohit Sharma",
        "branch": "B.Tech. — Computer Science and Engineering (DS)",
        "sem": "3rd Semester",
        "out": "rohit_ds.pdf"
    },
    {
        "name": "Dr. Dharmendra Vikramaditya Singh Rajput",
        "branch": "B.Tech. — Information Technology",
        "sem": "3rd Semester",
        "out": "long_name.pdf"
    }
]

for tc in test_cases:
    data = build_pdf(tc["name"], tc["branch"], tc["sem"])
    path = os.path.join(OUTPUT_DIR, tc["out"])
    with open(path, 'wb') as f:
        f.write(data)
    print(f"✓ Generated {tc['out']} ({len(data)} bytes) for {tc['name']}")
