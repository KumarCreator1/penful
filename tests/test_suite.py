import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from engine import build_pdf

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

test_cases = [
    {
        "name": "Vicky Kumar",
        "branch": "B.Tech. — Computer Science and Engineering (AIML)",
        "sem": "3rd Semester",
        "roll": "",
        "template": "dsa",
        "out": "test_dsa_vicky.pdf"
    },
    {
        "name": "Virat Yadav",
        "branch": "",
        "sem": "3rd Sem",
        "roll": "ITM2529855",
        "template": "ds_code",
        "out": "test_ds_virat.pdf"
    },
    {
        "name": "Rohit Sharma",
        "branch": "",
        "sem": "3rd Sem",
        "roll": "ITM274643",
        "template": "java_code",
        "out": "test_java_rohit.pdf"
    }
]

for tc in test_cases:
    data = build_pdf(
        student_name=tc["name"],
        branch_name=tc["branch"],
        semester=tc["sem"],
        roll_no=tc["roll"],
        template_key=tc["template"]
    )
    path = os.path.join(OUTPUT_DIR, tc["out"])
    with open(path, 'wb') as f:
        f.write(data)
    print(f"✓ Generated {tc['out']} ({len(data)} bytes) for {tc['name']} [Template: {tc['template']}]")
