import sys
import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import cv2
import io
import numpy as np
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import json

# Elasticsearch Configuration (Replace with your actual Elasticsearch endpoint)
ES_HOST = "http://your-elasticsearch-host:9200"

# Initialize Elasticsearch Client
try:
    es = Elasticsearch([ES_HOST], verify_certs=False)

    if not es.ping():
        print("Error: Elasticsearch is not available. Please check the connection.")
        sys.exit(1)
except Exception as e:
    print("Error connecting to Elasticsearch:", e)
    sys.exit(1)

def extract_text_from_text_pdf(pdf_path):
    """
    Extracts text from a text-based PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print("Error extracting text from text-based PDF:", e)
    return text

def extract_text_from_scanned_pdf(pdf_path):
    """
    Extracts text from an image-based (scanned) PDF file using OCR.

    Args:
        pdf_path (str): Path to the scanned PDF file.

    Returns:
        str: Extracted text.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                image_list = page.get_images(full=True)
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_data = base_image["image"]
                    image = Image.open(io.BytesIO(image_data))
                    
                    # Convert image to grayscale for better OCR accuracy
                    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
                    extracted_text = pytesseract.image_to_string(gray_image)
                    text += extracted_text
    except Exception as e:
        print("Error extracting text from scanned PDF:", e)
    return text

def extract_text_from_pdf(pdf_path):
    """
    Determines whether the PDF is text-based or scanned and extracts text accordingly.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text.
    """
    text = extract_text_from_text_pdf(pdf_path)
    if not text:
        text = extract_text_from_scanned_pdf(pdf_path)
    return text

def index_text_to_elasticsearch(text, pdf_path):
    """
    Indexes extracted text into Elasticsearch.

    Args:
        text (str): Extracted text content.
        pdf_path (str): Path to the PDF file.
    """
    filename = os.path.basename(pdf_path)  # Extract filename
    try:
        es.index(index="pdf_index", body={"text": text, "filename": filename, "path": pdf_path})
    except Exception as e:
        print("Error indexing document:", e)

def search_text(query):
    """
    Searches indexed documents in Elasticsearch.

    Args:
        query (str): Search query.

    Returns:
        list: Search results from Elasticsearch.
    """
    try:
        res = es.search(
            index="pdf_index",
            body={
                "query": {"match": {"text": {"query": query, "fuzziness": "AUTO"}}},
                "highlight": {"fields": {"text": {}}}
            }
        )
        return res["hits"]["hits"]
    except Exception as e:
        print("Error searching Elasticsearch:", e)
        return []

if __name__ == "__main__":
    """
    Command-line interface for the script.
    Usage:
        - Upload a PDF: python3 doc_parser.py upload <pdf_path>
        - Search for text: python3 doc_parser.py search <query>
    """
    if len(sys.argv) < 2:
        print("Usage: python3 doc_parser.py [upload | search]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "upload":
        if len(sys.argv) < 3:
            print("Please provide the path to the PDF file for upload.")
            sys.exit(1)

        pdf_path = sys.argv[2]
        if not os.path.exists(pdf_path):
            print("Error: File does not exist:", pdf_path)
            sys.exit(1)

        try:
            es.indices.get(index="pdf_index")
        except NotFoundError:
            try:
                es.indices.create(index="pdf_index")
            except Exception as e:
                print("Error creating Elasticsearch index:", e)
                sys.exit(1)

        extracted_text = extract_text_from_pdf(pdf_path)
        index_text_to_elasticsearch(extracted_text, pdf_path)
        print("File uploaded successfully and indexed in Elasticsearch.")

    elif action == "search":
        if len(sys.argv) < 3:
            print("Please provide the search query.")
            sys.exit(1)

        query = " ".join(sys.argv[2:])
        search_results = search_text(query)

        if not search_results:
            print("No results found.")
            sys.exit(1)

        results = []
        for hit in search_results:
            highlighted_text = hit.get("highlight", {}).get("text", [""])[0]
            highlighted_part = highlighted_text[:50]  # Display snippet of highlighted text
            result = {
                "filename": hit["_source"]["filename"],
                "path": hit["_source"]["path"],
                "highlighted": highlighted_part,
            }
            results.append(result)

        print(json.dumps(results, indent=4))

    else:
        print("Invalid request. Please use 'upload' or 'search'.")