import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, send_from_directory
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URL = os.environ.get("MONGODB_URL")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URL)
db = client[DB_NAME]
app = Flask(__name__)

if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=["POST"])
def uploadPost():
    try:
        image_receive = request.files['image_give']
        pdf_receive = request.files['pdf_give']
        judul_receive = request.form['judul_give']
        deskripsi_receive = request.form['deskripsi_give']
        
        image_path = os.path.join('static/uploads', image_receive.filename)
        image_receive.save(image_path)
        
        pdf_path = os.path.join('static/uploads', pdf_receive.filename)
        pdf_receive.save(pdf_path)
        
        doc = {
            'image': image_path,
            'pdf': pdf_path,
            'judul': judul_receive,
            'deskripsi': deskripsi_receive,
        }
        db.card.insert_one(doc)
        
        return jsonify({'msg': 'Data Berhasil Masuk'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'msg': 'Terjadi kesalahan saat mengupload data'}), 500


# Route untuk mengambil data card
@app.route('/cards', methods=["GET"])
def cardsget():
    card_list = list(db.card.find({}, {'_id': False}))
    return jsonify({'card': card_list})


# Route untuk mengunduh PDF
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory('static/uploads', filename)


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
