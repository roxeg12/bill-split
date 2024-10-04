import skimage as ski
import cv2
import pytesseract
import openai
from openai import OpenAI
from PIL import Image

def extract_text_from_image(img_path):

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening


    extracted_text = pytesseract.image_to_string(invert, config='--psm 6')

    return extracted_text

def extract_info_gpt(extracted_text, key):
    
    prompt = f"""
    Extract the following information from the receipt below:
    1. Good or service name
    2. Price
    3. Quantity purchased
    4. Bill total
    
    Then, return ONLY a JSON object with 4 inner JSON objects:
    1. Key: Items, Value: a 2D JSON array where each inner array 
    is of the format: [Good/Service name, price, quantity]
    2. Key: Total, Value: the total amount charged
    For example, an acceptable response could look like:
    '{{Items: [[Latte, 3.50, 2], [Americano, 2.75, 1]], Total: 12.55}}'
    Receipt text:
    {extracted_text}
    """

    client = OpenAI(
        api_key=key,
    )
    

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        #max_tokens=100
    )

    extracted_info = response.choices[0].message.content.strip()

    return extracted_info

def parse_image(api_key):
    
    image_path = "./imgs/crop2.jpg"

    

    extracted_text = extract_text_from_image(image_path)

    extracted_info = extract_info_gpt(extracted_text, api_key)

    print("Extracted Information:")
    print(extracted_info)


