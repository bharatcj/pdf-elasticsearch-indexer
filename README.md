### PDF Elasticsearch Indexer

A Python script that **extracts text from PDFs** (both text-based and scanned) and **indexes the content into Elasticsearch** for full-text search.

## 🚀 Features
- **Extracts text from text-based PDFs** using PyMuPDF (`fitz`).
- **Performs OCR on scanned PDFs** using Tesseract (`pytesseract`).
- **Indexes extracted text into Elasticsearch** for full-text search.
- **Supports text search with fuzzy matching** for better accuracy.
- **Returns structured JSON output** for easy integration.

---

## 🔧 **Installation**

### **1. Install Python and Required Libraries**
Ensure Python is installed. If not, download it from [Python.org](https://www.python.org/downloads/).

Then, install the required dependencies:

```sh
pip3 install pymupdf pytesseract pillow opencv-python numpy elasticsearch
```

Additionally, install **Tesseract OCR** for text recognition:

#### **Windows**
1. Download **Tesseract OCR**: [Download Here](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install it and add the **Tesseract `bin` folder** to your system PATH.
3. Verify installation:
   ```sh
   tesseract --version
   ```

#### **Linux (Ubuntu)**
```sh
sudo apt update
sudo apt install tesseract-ocr
```

#### **Mac (Homebrew)**
```sh
brew install tesseract
```

---

## 🏗 **Elasticsearch Setup**
### **1. Install Elasticsearch**
Download and install **Elasticsearch 7.x or later** from:
🔗 [Elasticsearch Official Site](https://www.elastic.co/downloads/elasticsearch)

### **2. Start Elasticsearch**
Run the following command:
```sh
elasticsearch
```

or if using Docker:
```sh
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.10.2
```

---

## 🎯 **Running the Script**
### **Step 1: Clone the Repository**
```sh
git clone https://github.com/bharatcj/pdf-elasticsearch-indexer.git
cd pdf-elasticsearch-indexer
```

### **Step 2: Set Up Elasticsearch Connection**
Edit `doc_parser.py` and update this line with your Elasticsearch host:
```python
ES_HOST = "http://your-elasticsearch-host:9200"
```
Replace `"your-elasticsearch-host"` with your actual Elasticsearch URL.

### **Step 3: Upload a PDF**
Run the script in **upload mode** to extract text and index it in Elasticsearch:

```sh
python3 doc_parser.py upload sample.pdf
```

### **Step 4: Search for Text**
Run the script in **search mode** to find text inside indexed PDFs:

```sh
python3 doc_parser.py search "contract agreement"
```

---

## 📜 **Example Output**
### **For Uploading a PDF**
```sh
File uploaded successfully and indexed in Elasticsearch.
```

### **For Searching Text**
```json
[
    {
        "filename": "sample.pdf",
        "path": "/path/to/sample.pdf",
        "highlighted": "This is a contract agreement..."
    }
]
```

---

## ⚠️ **Error Handling**
If an error occurs:
- The script **verifies the PDF file exists** before processing.
- If **Elasticsearch is unavailable**, the script exits with an error.
- **OCR processing errors** are logged for debugging.

---

## 🔄 **Customization**
- Modify `doc_parser.py` to **change the Elasticsearch index name**.
- Adjust **OCR settings** for better text recognition.

---

## 🛡️ **License**
This project is licensed under the **MIT License**.

---

## 🤝 **Contributing**
Contributions are welcome! Feel free to **fork this repository** and submit pull requests.

---

### **Author**
Developed by **Bharat CJ**  
GitHub: https://github.com/bharatcj

---

💡 **Did you know?** This script can be used for **legal document search, academic research, and contract analysis**! 🔍📄🚀