# PenFul 🖋️
### Production-Grade College Practical Front Page Vector Automation Platform

> *"Stop fighting with PDF editors. Automate the boring stuff so we can build the awesome stuff."*

PenFul is a coordinate-mapped vector engine designed for engineering students. Instead of clumsy, misaligned edits in online PDF editors that corrupt font dictionaries or shift borders, PenFul edits raw PDF vector streams in sub-milliseconds with mathematical precision.

---

## ✨ Features

- **True Vector Coordinate Redaction**: Masks target student glyphs without touching the college crest, borders, or faculty details (`Mrs. Ramneet kaur`, `Ms. Rakhi Antil`, `CSE Department, IITM`).
- **Dynamic Branch Reflow**: Automatically wraps long branches across dual baselines for Core CSE, AIML, DS, IoT, and IT without column collisions.
- **3 College Templates Supported**:
  1. `DSA Practical File` (Branch-based auto-reflow)
  2. `Data Structures — PCCSE201` (Enr. No + Sem)
  3. `OOPs Java — PCCSE203` (Enr. No + Sem)
- **Live 60fps Vector Preview**: Live real-time canvas updating dynamically as you type.
- **Batch Friend Mode**: Generate personalized front pages for your entire lab bench in one single `.zip` file.
- **Zero Heavy Native Dependencies**: Bundled TrueType font metrics with pure Python serverless compatibility.

---

## 📁 Repository Structure

```text
penful/
├── api/                       # Vercel Serverless Functions
│   ├── index.py               # Main HTTP request router (/api/generate & /api/batch)
│   ├── generate.py            # Direct route for /api/generate
│   └── batch.py               # Direct route for /api/batch
├── fonts/                     # Bundled TrueType fonts for serverless environments
│   ├── LiberationSerif-Bold.ttf
│   └── LiberationSerif-Regular.ttf
├── templates/                 # Master PDF base templates
│   ├── DSA_Practical_File_Edited.pdf
│   ├── ds_front.pdf
│   └── Java_front.pdf
├── public/                    # Frontend client
│   ├── index.html             # Sleek editorial UI (PenFul) + 60fps vector canvas
│   └── assets/                # High-DPI base preview assets
│       ├── preview.png
│       ├── preview_ds.png
│       └── preview_java.png
├── src/                       # Local server & core vector engine
│   ├── engine.py              # Sub-millisecond PDF stream reflow engine
│   └── server.py              # Standalone HTTP server for local development
├── tests/                     # Validation test suite
│   └── test_suite.py
├── requirements.txt           # Python dependencies (fonttools)
├── vercel.json                # Vercel deployment configuration
├── .gitignore
└── README.md
```

---

## 🚀 Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KumarCreator1/penful.git
   cd penful
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the local server:**
   ```bash
   python3 src/server.py
   ```
   Open [http://localhost:3000](http://localhost:3000) in your browser.

4. **Run test verification suite:**
   ```bash
   python3 tests/test_suite.py
   ```

---

## 🌐 Deploy to Vercel (1-Click Guide)

### Method A: Via Vercel Web Dashboard (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git remote add origin https://github.com/KumarCreator1/penful.git
   git branch -M main
   git push -u origin main
   ```

2. Go to **[vercel.com](https://vercel.com)** and sign in with GitHub.
3. Click **"Add New..."** ➔ **"Project"**.
4. Import your **`KumarCreator1/penful`** repository.
5. In the project configure settings:
   - **Framework Preset**: *Other*
   - **Root Directory**: `./` (leave default)
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
6. Click **Deploy**. Vercel will automatically:
   - Deploy `public/index.html` as the static website root.
   - Detect `requirements.txt` and install `fonttools`.
   - Mount `api/index.py` serverless functions for `/api/generate` and `/api/batch`.

### Method B: Via Vercel CLI

```bash
npm install -g vercel
vercel login
vercel --prod
```

---

## 👨‍💻 Author & Credits

Developed with precision by **Vicky Kumar** (~fellow classmate at IITM).
- Instagram: [@kumarcreator1](https://instagram.com/kumarcreator1)
- GitHub: [KumarCreator1](https://github.com/KumarCreator1)
