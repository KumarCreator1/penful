import os
import re
import zlib
from fontTools.ttLib import TTFont

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TEMPLATE = os.path.join(ROOT_DIR, 'templates', 'DSA_Practical_File_Edited.pdf')

# Load font metrics for exact pixel-perfect center alignment
FONT_BOLD = TTFont('/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf')
FONT_REGULAR = TTFont('/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf')

def measure_width(text, font, font_size):
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

def encode_pdf_string(s):
    # PDF string in WinAnsiEncoding / CP1252
    encoded = s.encode('cp1252', errors='replace')
    out = bytearray()
    for b in encoded:
        if b in (ord('\\'), ord('('), ord(')')):
            out.append(ord('\\'))
            out.append(b)
        else:
            out.append(b)
    return bytes(out)

def build_pdf(
    student_name="Sudhanshu Ranjan Adarsh",
    branch_name="B.Tech. — Computer Science and Engineering (AIML)",
    semester="3rd Semester",
    template_path=DEFAULT_TEMPLATE
):
    with open(template_path, 'rb') as f:
        orig = f.read()

    # 1. Clean original stream 29 (remove hardcoded Sudhanshu text)
    obj29_len = int(re.search(rb'29 0 obj\s*<<\s*/Length\s*(\d+)', orig).group(1))
    idx29 = orig.find(b'29 0 obj')
    s29_idx = orig.find(b'stream\n', idx29) + len(b'stream\n')
    stream29_bytes = orig[s29_idx : s29_idx + obj29_len]
    decomp29 = zlib.decompress(stream29_bytes)

    name_block = b'BT/EXGNNA 18.666668 Tf 1 0 0 -1 147.20258 720.56936 Tm[<003600580047004B004400510056004B00580003003500440051004D004400510003>55<00240047004400550056004B>]TJ ET'
    branch_block = b'BT/EXGNNA 14.666667 Tf 1 0 0 -1 149.99848 743.67776 Tm[<002500110037>91.000019<00480046004B001100030209000300260052005000530058005700480055>18<000300360046004C00480051004600480003004400510047>]TJ 1 0 0 -1 216.81684 759.9209 Tm[<00280051004A004C0051004800480055004C0051004A>]TJ ET'
    sem_block = b'BT/KFDXKX 14.666667 Tf 1 0 0 -1 216.62787 779.16409 Tm[<001600550047000300360048005000480056005700480055>]TJ ET'

    decomp29_clean = decomp29.replace(name_block, b'q Q ' + b' '*(len(name_block)-4))
    decomp29_clean = decomp29_clean.replace(branch_block, b'q Q ' + b' '*(len(branch_block)-4))
    decomp29_clean = decomp29_clean.replace(sem_block, b'q Q ' + b' '*(len(sem_block)-4))
    recomp29 = zlib.compress(decomp29_clean)

    # 2. Dynamic reflow and line wrapping for Branch
    CENTER_X = 191.33
    MAX_WIDTH = 190.0

    # Auto scale name if very long
    name_size = 14.0
    w_name = measure_width(student_name, FONT_BOLD, name_size)
    if w_name > MAX_WIDTH:
        name_size = max(11.0, name_size * (MAX_WIDTH / w_name))
        w_name = measure_width(student_name, FONT_BOLD, name_size)

    name_x = CENTER_X - (w_name / 2.0)
    name_y = 301.46

    # Wrap Branch
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
            if measure_width(candidate, FONT_BOLD, branch_size) <= MAX_WIDTH:
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
            if measure_width(candidate, FONT_BOLD, branch_size) <= MAX_WIDTH:
                curr.append(w)
            else:
                if curr: branch_lines.append(" ".join(curr))
                curr = [w]
        if curr: branch_lines.append(" ".join(curr))

    # Assemble stream lines
    stream_cmds = [b'q']

    # Draw Student Name
    name_str = encode_pdf_string(student_name)
    stream_cmds.extend([
        b'BT',
        f'1 0 0 1 {name_x:.2f} {name_y:.2f} Tm'.encode('latin1'),
        f'/tibo {name_size:.1f} Tf'.encode('latin1'),
        b'.066667 .094118 .152941 RG .066667 .094118 .152941 rg',
        b'(' + name_str + b')Tj',
        b'ET'
    ])

    # Draw Branch lines
    curr_y = 284.13
    for bline in branch_lines:
        w_b = measure_width(bline, FONT_BOLD, branch_size)
        bx = CENTER_X - (w_b / 2.0)
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

    # Draw Semester
    sem_size = 11.0
    w_sem = measure_width(semester, FONT_REGULAR, sem_size)
    sem_x = CENTER_X - (w_sem / 2.0)
    sem_y = curr_y - 2.0
    sem_str = encode_pdf_string(semester)
    stream_cmds.extend([
        b'BT',
        f'1 0 0 1 {sem_x:.2f} {sem_y:.2f} Tm'.encode('latin1'),
        f'/tiro {sem_size:.1f} Tf'.encode('latin1'),
        b'.294118 .333333 .388235 RG .294118 .333333 .388235 rg',
        b'(' + sem_str + b')Tj',
        b'ET',
        b'Q\n'
    ])

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

    out_data = orig + new_obj29 + new_obj4 + new_obj37 + new_xref
    return out_data
