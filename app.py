import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# API anahtarını güvenli bir şekilde ortam değişkenlerinden al
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    # Bu, API anahtarı ayarlanmamışsa bir hata mesajı verir
    print(f"API anahtarı yapılandırılamadı: {e}")
    model = None

@app.route('/')
def index():
    # index.html dosyasını kullanıcıya göster
    return render_template('index.html')

@app.route('/soru-sor', methods=['POST'])
def soru_sor():
    if not model:
        return jsonify({'hata': 'Sunucu tarafında API anahtarı ayarlanmamış.'}), 500

    data = request.get_json()
    kullanici_sorusu = data.get('soru')

    if not kullanici_sorusu:
        return jsonify({'hata': 'Soru boş olamaz!'}), 400

    try:
        # Gemini modeline isteği gönder
        response = model.generate_content(kullanici_sorusu)
        cevap = response.text
        return jsonify({'cevap': cevap})
    except Exception as e:
        return jsonify({'hata': f'Google AI API hatası: {str(e)}'}), 500

# Codespaces'te çalışması için host ve port ayarları
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
