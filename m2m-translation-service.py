from flask import Flask, request, jsonify
import time
import ctranslate2
import transformers

app = Flask(__name__)

# Initialize M2M100 translator and tokenizer
ct2_model_path = "m2m100_1.2B"
translator = ctranslate2.Translator(ct2_model_path)
tokenizer = transformers.AutoTokenizer.from_pretrained("facebook/m2m100_1.2B")

@app.route('/m2m_translate', methods=['POST'])
def m2m_translate():
    """
    Endpoint for translating text using M2M100 model.
    Expects JSON with:
    - question: text to translate
    - from_code: source language code
    - to_code: target language code
    """
    data = request.get_json()
    user_question = data.get('question')
    argo_from_code = data.get('from_code')
    to_code = data.get('to_code')
    start_time = time.time()
    
    if not user_question:
        return jsonify({"error": "Text parameter is missing"}), 400

    # Set source language and tokenize input
    tokenizer.src_lang = argo_from_code
    source = tokenizer.convert_ids_to_tokens(tokenizer.encode(user_question))
    
    # Prepare target language prefix
    target_prefix = [tokenizer.lang_code_to_token[to_code]]
    
    # Perform translation
    results = translator.translate_batch([source], target_prefix=[target_prefix])
    target = results[0].hypotheses[0][1:]

    # Convert tokens back to text
    translated_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(target))
    
    print(translated_text)

    # Calculate execution time
    total_execution_time = time.time() - start_time
    
    # Save translation to database (if needed)
    save_to_mysql("(m2m)" + user_question, translated_text, "", "", total_execution_time)

    return jsonify({"translatedText": translated_text})

@app.route('/m2m_translate_youtube', methods=['POST'])
def m2m_translate_youtube():
    """
    Similar endpoint for YouTube translations.
    Does not save to database.
    """
    data = request.get_json()
    user_question = data.get('question')
    argo_from_code = data.get('from_code')
    to_code = data.get('to_code')
    start_time = time.time()
    
    if not user_question:
        return jsonify({"error": "Text parameter is missing"}), 400

    # Set source language and tokenize input
    tokenizer.src_lang = argo_from_code
    source = tokenizer.convert_ids_to_tokens(tokenizer.encode(user_question))
    
    # Prepare target language prefix
    target_prefix = [tokenizer.lang_code_to_token[to_code]]
    
    # Perform translation
    results = translator.translate_batch([source], target_prefix=[target_prefix])
    target = results[0].hypotheses[0][1:]

    # Convert tokens back to text
    translated_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(target))
     
    print(user_question)
    print(translated_text)

    # Calculate execution time
    total_execution_time = time.time() - start_time

    return jsonify({"translatedText": translated_text})

def save_to_mysql(user_question, translated_text, llama_response, translated_japanese, total_execution_time):
    """
    Helper function to save translations to MySQL database.
    Implementation details would go here.
    """
    # Database connection and saving logic would go here
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
