"""
FrontCraft Multi-Template Vector Coordinate & Typography Engine
================================================================
Supports:
1. "dsa"      : Classic DSA Front Page (Mrs. Ramneet Kaur) with Branch & Specialization reflow
2. "ds_code"   : Data Structures (PCCSE201 — Mrs. Ramneet Kaur) with Enr. No & Sem
3. "java_code" : OOPs Java (PCCSE203 — Ms. Rakhi Antil) with Enr. No & Sem
"""

import os
import re
import zlib
from fontTools.ttLib import TTFont

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FILE_DIR = os.path.dirname(CURRENT_FILE_DIR)

def _find_templates_dir():
    candidates = [
        os.path.join(CURRENT_FILE_DIR, 'templates'),
        os.path.join(PARENT_FILE_DIR, 'templates'),
        os.path.join(PARENT_FILE_DIR, 'api', 'templates'),
        '/vercel/path0/templates',
        '/vercel/path0/api/templates'
    ]
    for c in candidates:
        if os.path.isdir(c) and os.path.exists(os.path.join(c, 'DSA_Practical_File_Edited.pdf')):
            return c
    return os.path.join(PARENT_FILE_DIR, 'templates')

TEMPLATES_DIR = _find_templates_dir()

TEMPLATE_MAP = {
    'dsa': {
        'file': os.path.join(TEMPLATES_DIR, 'DSA_Practical_File_Edited.pdf'),
        'mode': 'dsa_branch',
        'title': 'Data Structures & Algorithms (Branch-based)',
        'teacher': 'Mrs. Ramneet Kaur'
    },
    'ds_code': {
        'file': os.path.join(TEMPLATES_DIR, 'ds_front.pdf'),
        'mode': 'code_enr',
        'title': 'Data Structures — PCCSE201',
        'teacher': 'Mrs. Ramneet kaur'
    },
    'java_code': {
        'file': os.path.join(TEMPLATES_DIR, 'Java_front.pdf'),
        'mode': 'code_enr',
        'title': 'OOPs Java — PCCSE203',
        'teacher': 'Ms. Rakhi Antil'
    }
}

# Typography font metrics
def _find_fonts_dir():
    candidates = [
        os.path.join(CURRENT_FILE_DIR, 'fonts'),
        os.path.join(PARENT_FILE_DIR, 'fonts'),
        os.path.join(PARENT_FILE_DIR, 'api', 'fonts'),
        '/vercel/path0/fonts',
        '/vercel/path0/api/fonts'
    ]
    for c in candidates:
        if os.path.isdir(c) and os.path.exists(os.path.join(c, 'LiberationSerif-Bold.ttf')):
            return c
    return os.path.join(PARENT_FILE_DIR, 'fonts')

FONTS_DIR = _find_fonts_dir()

def _load_font(filename: str, fallback_path: str) -> TTFont:
    local_path = os.path.join(FONTS_DIR, filename)
    if os.path.exists(local_path):
        return TTFont(local_path)
    if os.path.exists(fallback_path):
        return TTFont(fallback_path)
    raise FileNotFoundError(f"Font {filename} could not be found at {local_path} or {fallback_path}")

FONT_BOLD = _load_font('LiberationSerif-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf')
FONT_REGULAR = _load_font('LiberationSerif-Regular.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf')

def measure_width(text: str, font: TTFont, font_size: float) -> float:
    """Calculate exact text width in points using TrueType font metrics."""
    cmap = font.getBestCmap()
    hmtx = font['hmtx']
    units_per_em = font['head'].unitsPerEm
    width = 0
    for char in text:
        code = ord(char)
        glyph = cmap.get(code)
        if glyph and glyph in hmtx.metrics:
            advance, _ = hmtx.metrics[glyph]
            width += advance
        else:
            width += units_per_em * 0.5
    return (width / units_per_em) * font_size

def encode_pdf_string(s: str) -> bytes:
    """Encode string in WinAnsiEncoding (CP1252) with PDF literal escaping."""
    encoded = s.encode('cp1252', errors='replace')
    out = bytearray()
    for b in encoded:
        if b in (ord('\\'), ord('('), ord(')')):
            out.append(ord('\\'))
            out.append(b)
        else:
            out.append(b)
    return bytes(out)

def build_pdf_dsa(
    student_name: str,
    branch_name: str,
    semester: str,
    template_path: str = TEMPLATE_MAP['dsa']['file']
) -> bytes:
    """Engine for Classic DSA Template (Branch-based reflow)."""
    with open(template_path, 'rb') as f:
        orig = f.read()

    obj29_len = int(re.search(rb'29 0 obj\s*<<\s*/Length\s*(\d+)', orig).group(1))
    idx29 = orig.find(b'29 0 obj')
    s29_idx = orig.find(b'stream\n', idx29) + len(b'stream\n')
    stream29_bytes = orig[s29_idx : s29_idx + obj29_len]
    decomp29 = zlib.decompress(stream29_bytes)

    orig_name_block = b'BT/EXGNNA 18.666668 Tf 1 0 0 -1 147.20258 720.56936 Tm[<003600580047004B004400510056004B00580003003500440051004D004400510003>55<00240047004400550056004B>]TJ ET'
    orig_branch_block = b'BT/EXGNNA 14.666667 Tf 1 0 0 -1 149.99848 743.67776 Tm[<002500110037>91.000019<00480046004B001100030209000300260052005000530058005700480055>18<000300360046004C00480051004600480003004400510047>]TJ 1 0 0 -1 216.81684 759.9209 Tm[<00280051004A004C0051004800480055004C0051004A>]TJ ET'
    orig_sem_block = b'BT/KFDXKX 14.666667 Tf 1 0 0 -1 216.62787 779.16409 Tm[<001600550047000300360048005000480056005700480055>]TJ ET'

    decomp29_clean = decomp29.replace(orig_name_block, b'q Q ' + b' '*(len(orig_name_block)-4))
    decomp29_clean = decomp29_clean.replace(orig_branch_block, b'q Q ' + b' '*(len(orig_branch_block)-4))
    decomp29_clean = decomp29_clean.replace(orig_sem_block, b'q Q ' + b' '*(len(orig_sem_block)-4))
    recomp29 = zlib.compress(decomp29_clean)

    COLUMN_CENTER_X = 191.33
    MAX_SAFE_WIDTH = 190.0

    name_size = 14.0
    w_name = measure_width(student_name, FONT_BOLD, name_size)
    if w_name > MAX_SAFE_WIDTH:
        name_size = max(10.5, name_size * (MAX_SAFE_WIDTH / w_name))
        w_name = measure_width(student_name, FONT_BOLD, name_size)

    name_x = COLUMN_CENTER_X - (w_name / 2.0)
    name_y = 301.46

    branch_size = 11.0
    branch_lines = []
    clean_branch = branch_name.strip()
    if ' — ' in clean_branch:
        prefix, rest = clean_branch.split(' — ', 1)
        full_prefix = prefix + ' — '
    elif ' - ' in clean_branch:
        prefix, rest = clean_branch.split(' - ', 1)
        full_prefix = prefix + ' — '
    elif clean_branch.startswith('B.Tech.'):
        full_prefix = 'B.Tech. — '
        rest = clean_branch[len('B.Tech.'):].lstrip(' .—–-')
    else:
        full_prefix = ''
        rest = clean_branch

    words = rest.split()
    if full_prefix:
        line1_words = []
        line2_words = []
        for i, w in enumerate(words):
            candidate = full_prefix + " ".join(line1_words + [w])
            if measure_width(candidate, FONT_BOLD, branch_size) <= MAX_SAFE_WIDTH:
                line1_words.append(w)
            else:
                line2_words = words[i:]
                break
        if not line2_words and line1_words:
            branch_lines.append(full_prefix + " ".join(line1_words))
        else:
            branch_lines.append(full_prefix + " ".join(line1_words))
            branch_lines.append(" ".join(line2_words))
    else:
        curr = []
        for w in words:
            candidate = " ".join(curr + [w])
            if measure_width(candidate, FONT_BOLD, branch_size) <= MAX_SAFE_WIDTH:
                curr.append(w)
            else:
                if curr: branch_lines.append(" ".join(curr))
                curr = [w]
        if curr: branch_lines.append(" ".join(curr))

    stream_cmds = [b'q']
    name_str = encode_pdf_string(student_name)
    stream_cmds.extend([
        b'BT',
        f'1 0 0 1 {name_x:.2f} {name_y:.2f} Tm'.encode('latin1'),
        f'/tibo {name_size:.1f} Tf'.encode('latin1'),
        b'.066667 .094118 .152941 RG .066667 .094118 .152941 rg',
        b'(' + name_str + b')Tj',
        b'ET'
    ])

    curr_y = 284.13
    for bline in branch_lines:
        w_b = measure_width(bline, FONT_BOLD, branch_size)
        bx = COLUMN_CENTER_X - (w_b / 2.0)
        bline_str = encode_pdf_string(bline)
        stream_cmds.extend([
            b'BT',
            f'1 0 0 1 {bx:.2f} {curr_y:.2f} Tm'.encode('latin1'),
            f'/tibo {branch_size:.1f} Tf'.encode('latin1'),
            b'.117647 .227451 .541176 RG .117647 .227451 .541176 rg',
            b'(' + bline_str + b')Tj',
            b'ET'
        ])
        curr_y -= 13.5

    sem_size = 11.0
    w_sem = measure_width(semester, FONT_REGULAR, sem_size)
    sem_x = COLUMN_CENTER_X - (w_sem / 2.0)
    sem_y = curr_y - 2.0
    sem_str = encode_pdf_string(semester)
    stream_cmds.extend([
        b'BT',
        f'1 0 0 1 {sem_x:.2f} {sem_y:.2f} Tm'.encode('latin1'),
        f'/tiro {sem_size:.1f} Tf'.encode('latin1'),
        b'.294118 .333333 .388235 RG .294118 .333333 .388235 rg',
        b'(' + sem_str + b')Tj',
        b'ET'
    ])

    stream_cmds.append(b'Q\n')
    content37 = b'\n'.join(stream_cmds)
    recomp37 = zlib.compress(content37)

    new_obj4 = b'4 0 obj\n<</Type/Page/Parent 1 0 R/MediaBox[0 0 595.2756 841.8898]/Contents[29 0 R 30 0 R 32 0 R 34 0 R 37 0 R]/Resources<</ExtGState<</a1.0<</ca 1>>/a1<</ca 1>>>>/Font<</LZQZNB 15 0 R/EXGNNA 19 0 R/CYBALF 23 0 R/KFDXKX 27 0 R/tibo 31 0 R/tiro 33 0 R>>/XObject<</Im1 28 0 R>>>>/TrimBox[0 0 595.2756 841.8898]/BleedBox[0 0 595.2756 841.8898]/Annots[]>>\nendobj\n'

    append_start = len(orig)
    new_obj29 = f'29 0 obj\n<</Length {len(recomp29)}/Filter/FlateDecode>>\nstream\n'.encode('latin1') + recomp29 + b'\nendstream\nendobj\n'
    new_obj37 = f'37 0 obj\n<</Length {len(recomp37)}/Filter/FlateDecode>>\nstream\n'.encode('latin1') + recomp37 + b'\nendstream\nendobj\n'

    offset_29 = append_start
    offset_4 = offset_29 + len(new_obj29)
    offset_37 = offset_4 + len(new_obj4)

    last_startxref = int(re.findall(rb'startxref\s+(\d+)\s+%%EOF', orig)[-1])
    xref_offset = offset_37 + len(new_obj37)

    new_xref = (
        f'xref\n'
        f'4 1\n{offset_4:010d} 00000 n \n'
        f'29 1\n{offset_29:010d} 00000 n \n'
        f'37 1\n{offset_37:010d} 00000 n \n'
        f'trailer\n<< /Size 38 /Root 3 1 R /Prev {last_startxref} >>\n'
        f'startxref\n{xref_offset}\n%%EOF\n'
    ).encode('latin1')

    return orig + new_obj29 + new_obj4 + new_obj37 + new_xref

def build_pdf_enr_sem(
    student_name: str,
    enr_no: str,
    semester: str,
    template_key: str,
    id_label: str = "enr"
) -> bytes:
    """
    Engine for Course Code Templates:
    - Data Structures (ds_front.pdf)
    - OOPs Java (Java_front.pdf)
    Variables: Name, Enr. No, and Sem.
    PRESERVES: Mrs. Ramneet kaur / Ms. Rakhi Antil, Assistant Professor, and CSE Department, IITM!
    """
    template_path = TEMPLATE_MAP[template_key]['file']
    with open(template_path, 'rb') as f:
        orig = f.read()

    # Decompress stream 45
    m45 = re.search(rb'45 0 obj\s*<<\s*/Filter\s*/FlateDecode\s*/Length\s*(\d+)\s*>>\s*stream\r?\n(.*?)\r?\nendstream', orig, re.DOTALL)
    decomp = zlib.decompress(m45.group(2))

    # Redact original hardcoded text blocks
    # 1. Student Name
    b_name = re.search(rb'BT\s+0 Tr\s+/F3 18.720699 Tf\s+1 0 0.000000 -1 116.800003 675.359985 Tm.*?ET', decomp, re.DOTALL).group(0)
    # 2. Enr/Roll label
    b_enr_label = re.search(rb'BT\s+0 Tr\s+/F3 14.720600 Tf\s+1 0 0.000000 -1 186.240005 696.000000 Tm.*?ET', decomp, re.DOTALL).group(0)
    # 3. Enr value
    b_enr = re.search(rb'BT\s+0 Tr\s+/F5 14.720600 Tf\s+1 0 0.000000 -1 239.520004 696.000000 Tm.*?ET', decomp, re.DOTALL).group(0)
    # 4. Sem block: redact old 3rd Sem block and re-inject with perfectly aligned CSE Department, IITM
    b_sem = re.search(rb'BT\s+0 Tr\s+/F5 14.720600 Tf\s+1 0 0.000000 -1 221.759995 714.239990 Tm.*?ET', decomp, re.DOTALL).group(0)

    clean_decomp = decomp.replace(b_name, b'q Q ' + b' '*(len(b_name)-4))
    clean_decomp = clean_decomp.replace(b_enr_label, b'q Q ' + b' '*(len(b_enr_label)-4))
    clean_decomp = clean_decomp.replace(b_enr, b'q Q ' + b' '*(len(b_enr)-4))
    clean_decomp = clean_decomp.replace(b_sem, b'q Q ' + b' '*(len(b_sem)-4))

    # In stream 45 coordinates: scale is 0.75, inverted Y
    # Center of SUBMITTED BY column = 168.60 / 0.75 = 224.8 pt
    stream_center_x = 224.8
    name_font_size = 18.72  # = 14.04 pt in user space
    w_name_user = measure_width(student_name, FONT_BOLD, 14.04)
    w_name_stream = w_name_user / 0.75

    name_x_stream = stream_center_x - (w_name_stream / 2.0)
    name_y_stream = 675.36

    enr_clean = enr_no.strip() if enr_no else "ITM2648475"
    sem_clean = semester.strip() if semester else "3rd Sem"
    label_text = "Roll No.:" if id_label == 'roll' else "Enr. No.:"

    name_str = encode_pdf_string(student_name).decode('latin1')
    label_str = encode_pdf_string(label_text).decode('latin1')
    enr_str = encode_pdf_string(enr_clean).decode('latin1')
    sem_str = encode_pdf_string(sem_clean).decode('latin1')

    # CSE Department, IITM alignment:
    # Java template original xMin in user space is 331.15 pt -> 441.54 in stream space
    # DS template original xMin in user space is 333.91 pt -> 445.22 in stream space
    dept_x = 441.54 if template_key == 'java_code' else 445.22
    dept_text = "CSE Department, IITM"

    stream_inject = f'''
q
0.066667 0.094118 0.152941 rg
BT
/tibo {name_font_size:.2f} Tf
1 0 0.000000 -1 {name_x_stream:.2f} {name_y_stream:.2f} Tm
({name_str}) Tj
ET
Q
q
0.066667 0.094118 0.152941 rg
BT
/tibo 14.72 Tf
1 0 0.000000 -1 186.24 696.00 Tm
({label_str}) Tj
ET
Q
q
0.294118 0.333333 0.388235 rg
BT
/tiro 14.72 Tf
1 0 0.000000 -1 241.00 696.00 Tm
({enr_str}) Tj
ET
BT
/tiro 14.72 Tf
1 0 0.000000 -1 224.00 714.24 Tm
({sem_str}) Tj
ET
BT
/tiro 14.72 Tf
1 0 0.000000 -1 {dept_x:.2f} 714.24 Tm
({dept_text}) Tj
ET
Q
'''.encode('latin1')

    new_stream45 = clean_decomp + stream_inject
    recomp45 = zlib.compress(new_stream45)

    new_obj46 = (
        b'46 0 obj\n<<\n'
        b'/Font <<\n'
        b'/F1 11 0 R\n'
        b'/F2 19 0 R\n'
        b'/F3 27 0 R\n'
        b'/F4 35 0 R\n'
        b'/F5 43 0 R\n'
        b'/tibo 48 0 R\n'
        b'/tiro 49 0 R\n'
        b'>>\n'
        b'/XObject <<\n'
        b'/Image1 44 0 R\n'
        b'>>\n'
        b'>>\nendobj\n'
    )

    obj_tibo = b'48 0 obj\n<</Type/Font/Subtype/Type1/BaseFont/Times-Bold/Encoding/WinAnsiEncoding>>\nendobj\n'
    obj_tiro = b'49 0 obj\n<</Type/Font/Subtype/Type1/BaseFont/Times-Roman/Encoding/WinAnsiEncoding>>\nendobj\n'

    append_start = len(orig)
    new_obj45 = f'\n45 0 obj\n<<\n/Filter /FlateDecode\n/Length {len(recomp45)}\n>>\nstream\n'.encode('latin1') + recomp45 + b'\nendstream\nendobj\n'

    offset_45 = append_start + 1
    offset_46 = offset_45 + len(new_obj45)
    offset_48 = offset_46 + len(new_obj46)
    offset_49 = offset_48 + len(obj_tibo)

    last_startxref = int(re.findall(rb'startxref\s+(\d+)\s+%%EOF', orig)[-1])
    xref_offset = offset_49 + len(obj_tiro)

    new_xref = (
        f'xref\n'
        f'45 2\r\n'
        f'{offset_45:010d} 00000 n\r\n'
        f'{offset_46:010d} 00000 n\r\n'
        f'48 2\r\n'
        f'{offset_48:010d} 00000 n\r\n'
        f'{offset_49:010d} 00000 n\r\n'
        f'trailer\n<< /Size 50 /Root 1 0 R /Prev {last_startxref} >>\n'
        f'startxref\n{xref_offset}\n%%EOF\n'
    ).encode('latin1')

    return orig + new_obj45 + new_obj46 + obj_tibo + obj_tiro + new_xref

def build_pdf(
    student_name: str = "Sudhanshu Ranjan Adarsh",
    branch_name: str = "B.Tech. — Computer Science and Engineering (AIML)",
    semester: str = "3rd Semester",
    roll_no: str = "",
    id_label: str = "enr",
    template_key: str = "dsa"
) -> bytes:
    """Master Router for all college practical templates."""
    if template_key == 'ds_code' or template_key == 'java_code':
        return build_pdf_enr_sem(
            student_name=student_name,
            enr_no=roll_no,
            semester=semester,
            template_key=template_key,
            id_label=id_label
        )
    else:
        return build_pdf_dsa(
            student_name=student_name,
            branch_name=branch_name,
            semester=semester
        )
