# FrontCraft 🚀
### Production-Grade College Practical Front Page Automation Platform

A sleek, instant practical front page generator built for college students. Replace names and branch details with vector-level precision in milliseconds without distorting college borders, logos, or typography.

---

## 📁 Clean Directory Structure

```text
makeFrontPage/
├── templates/                 # Master PDF templates
│   └── DSA_Practical_File_Edited.pdf
├── src/                       # Application core & services
│   ├── engine.py              # Precision PDF vector stream reflow engine
│   └── server.py              # Lightweight HTTP backend API & asset server
├── public/                    # Frontend client
│   ├── index.html             # Responsive Tailwind UI + live 60fps preview
│   └── assets/                # Clean high-DPI base preview images
│       └── preview.png
├── tests/                     # Test suite
│   └── test_suite.py
├── output/                    # Generated test files (.gitignored)
├── .gitignore
└── README.md
```

---

## ⚡ Key Highlights
1. **Vector Stream Reflow**: Directly modifies PDF content streams rather than pixelated HTML canvas snapshots.
2. **Dynamic Wrapping & Alignment**: Automatically center-aligns variables at `X = 191.33 pt` and wraps branch specializations (`AIML`, `DS`, `IoT`) seamlessly.
3. **Batch Generation**: Download all front pages for your entire friend group in one `.zip` file for quick printing.

---

## 🚀 Quickstart

```bash
# Start server
python3 src/server.py

# Run tests
python3 tests/test_suite.py
```
Open **`http://localhost:3000`** in your browser.
