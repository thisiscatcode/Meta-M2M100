from flask import Flask, request, jsonify
from transformers import pipeline
from argostranslate import package, translate
import mysql.connector
import time
import ctranslate2
import transformers

app = Flask(__name__)

# Initialize translation models
fugu_translator_enja = pipeline('translation', model='staka/fugumt-en-ja')
fugu_translator_jaen = pipeline('translation', model='staka/fugumt-ja-en')

def install_translation_package(from_code, to_code):
    package.update_package_index()
    available_packages = package.get_available_packages()
    matching_packages = [pkg for pkg in available_packages 
                        if pkg.from_code == from_code and pkg.to_code == to_code]
    
    if matching_packages:
        package_to_install = matching_packages[0]
        try:
            package.install_from_path(package_to_install.download())
        except Exception as e:
            print(f"Error installing package: {e}")

# Install translation packages
install_translation_package('ja', 'en')
install_translation_package('en', 'ja')

@app.route('/fugu_translate', methods=['POST'])
def fugu_translate():
    data = request.get_json()
    user_question = data.get('question')
    from_code = data.get('from_code')
    
    if not user_question:
        return jsonify({"error": "Text parameter is missing"}), 400

    if from_code == 'en':
        result = fugu_translator_enja(user_question)
    elif from_code == 'ja':
        result = fugu_translator_jaen(user_question)
    else:
        result = fugu_translator_enja(user_question)
        
    translation_text = result[0]['translation_text']
    return jsonify({"translation_text": translation_text})

@app.route('/argo_translate', methods=['POST'])
def argo_translate():
    data = request.get_json()
    user_question = data.get('question')
    argo_from_code = data.get('from_code')
    start_time = time.time()
    
    if not user_question:
        return jsonify({"error": "Text parameter is missing"}), 400
     
    if argo_from_code == 'en':
        translated_text = translate.translate(user_question, 'en', 'ja')
    else:
        translated_text = translate.translate(user_question, 'ja', 'en')

    total_execution_time = time.time() - start_time
    save_to_mysql("(argo2)"+user_question, translated_text, "", "", total_execution_time)

    return jsonify({"translatedText": translated_text})

def save_to_mysql(user_question, translated_text, response, translated_response, 
                 total_execution_time):
    try:
        insert_query = """
            INSERT INTO bot_llama 
            (user_question, translated_english, llama_response, translated_japanese, 
             exe_time, creator, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s, now())
        """
        
        mysql_conn = mysql.connector.connect(
            host='xxx',
            user='xxx',
            password='xxx',
            database='xxx',
            charset='utf8mb
