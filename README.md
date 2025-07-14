
# 🕵️‍♂️ Ransomware Report & Incident Response Downloader

A Python desktop application to:
- Search and download ransomware-related reports and incident response documents
- Automatically extract entities such as ransomware gangs, CVEs, MITRE ATT&CK TTPs, and security tools from PDF files

## 🔧 Features

- Select from top 30 ransomware gangs (2020–2024)
- Choose report type: standard report or incident response
- Search using DuckDuckGo (Google not supported due to scraping limitations)
- Download files (PDF, DOCX, etc.) from public web sources
- Analyze downloaded PDFs to extract:
  - Ransomware gang name
  - CVEs
  - MITRE TTPs (e.g. T1059)
  - Mentioned organizations, products or tools

## 💻 Requirements

Python 3.8+
Install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Dependencies include:
- `requests`
- `pandas`
- `tkinter`
- `pymupdf`
- `spacy`
- `openpyxl`
- `ddgs`

## 🚀 Usage

1. Run the app:

```bash
python main_with_analysis.py
```

2. From the GUI:
   - Select ransomware gangs and categories
   - Click **"Start Download"**
   - After download, click **"Analyze downloaded reports"**
   - Choose the folder containing downloaded reports
   - An Excel file `estrazione_ransomware.xlsx` will be generated with structured intelligence

## 📁 Output

- All files are downloaded into a structured folder: `YEAR/GANG/CATEGORY/`
- Summary saved as `report_summary.xlsx`
- Extracted intelligence saved as `estrazione_ransomware.xlsx`

## 📌 Notes

- DuckDuckGo is used for compatibility and to avoid scraping blocks
- Only non-HTML documents are saved (application/pdf, etc.)
- Files with ambiguous extensions are saved as `.pdf`

## 📷 GUI Screenshot

![screenshot-placeholder](docs/screenshot.png)  *(Replace with your own screenshot)*

## 👨‍💻 Author

Pietro Melillo  
CISO & Cyber Threat Intelligence Researcher  
Würth Italia | RedHotCyber | University of Sannio

---

> For contributions, feedback or collaboration opportunities, feel free to open an issue or contact me.
