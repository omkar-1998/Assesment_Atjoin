import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
import string
from fuzzywuzzy import fuzz
import pandas as pd

# Download NLTK tokenizer resources
nltk.download('punkt_tab')

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to tokenize and preprocess the text
def tokenize_text(text):
    tokens = word_tokenize(text.lower())  # Convert to lowercase for uniformity
    words = [word for word in tokens if word.isalpha()]  # Remove punctuation and keep words
    return words

# Function for exact match with reference list
def exact_match(extracted_words, reference_list):
    matches = [word for word in extracted_words if word in reference_list]
    return len(matches), len(extracted_words), len(reference_list)

# Optional: Fuzzy match with reference list based on a threshold
def fuzzy_match(extracted_words, reference_list, threshold=80):
    matches = []
    for word in extracted_words:
        for ref_word in reference_list:
            if fuzz.ratio(word, ref_word) >= threshold:
                matches.append(word)
                break
    return len(matches), len(extracted_words), len(reference_list)

# Function to calculate match percentage
def calculate_match_percentage(matches, total_extracted, total_reference):
    percentage = (matches / total_reference) * 100
    return percentage

# Function to display result in the console
def display_result(percentage, matches, total_reference):
    print(f"Match Percentage: {percentage:.2f}%")
    print(f"Matched {matches} out of {total_reference} reference words.")

# Function to save results to a CSV file
def save_to_csv(matches, percentage, output_path='output.csv'):
    data = {
        'Matched Words': [matches],
        'Match Percentage': [percentage]
    }
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)

# Main function to execute the complete process
def main(pdf_path, reference_list, output_csv=False):
    # Step 1: Extract text from PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Tokenize the extracted text
    extracted_words = tokenize_text(extracted_text)
    
    # Step 3: Match values with reference list (using exact matching)
    matches, total_extracted, total_reference = exact_match(extracted_words, reference_list)
    
    # Step 4: Calculate match percentage
    match_percentage = calculate_match_percentage(matches, total_extracted, total_reference)
    
    # Step 5: Display results
    display_result(match_percentage, matches, total_reference)
    
    # Optional Step 6: Save results to CSV
    if output_csv:
        save_to_csv(matches, match_percentage)

# Example usage
reference_words = ['machine', 'learning', 'python', 'data', 'algorithm','aws','Dashboard','power bi', 'html','css']
# Provide the path to the PDF file you want to analyze in 'sample.pdf'
main('example1.pdf', reference_words, output_csv=True)