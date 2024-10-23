# Flask Meta-M2M100 Translation Service

This repository provides a Flask web service for translating text between multiple languages using the M2M100 model from Facebook. The service supports translation for both regular queries and YouTube subtitles.

## Features

- **Language Translation**: Supports translation between multiple languages.
- **REST API**: Two endpoints for text translation.
- **Execution Time Logging**: Tracks translation execution time for performance monitoring.

## Requirements

- Python 3.7 or higher
- Flask
- ctranslate2
- transformers

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/thisiscatcode/Meta-M2M100.git
   cd Meta-M2M100
   ```

2. **Install required packages**:
   ```bash
   pip install flask ctranslate2 transformers
   ```

3. **Download the M2M100 model**:
   - Ensure that the model files are available in the specified path (`m2m100_1.2B`).

## Usage

1. **Run the Flask application**:
   ```bash
   python app.py
   ```

2. **Send a POST request to translate text**:
   ```bash
   curl -X POST http://127.0.0.1:5000/m2m_translate -H "Content-Type: application/json" -d '{"question": "Hello, world!", "from_code": "en", "to_code": "ja"}'
   ```

3. **Response**: The service will return a JSON object containing the translated text:
   ```json
   {
       "translatedText": "こんにちは、世界！"
   }
   ```

## Endpoints

- **`/m2m_translate`**: Translates text from a source language to a target language. Expects JSON with `question`, `from_code`, and `to_code` parameters.
- **`/m2m_translate_youtube`**: Similar to the main translation endpoint but does not save to the database.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests. If you encounter any issues or have suggestions, please open an issue.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- **M2M100**: For providing state-of-the-art multilingual translation capabilities.
- **Flask**: For creating the web service.
- **CTranslate2**: For efficient translation implementation.
