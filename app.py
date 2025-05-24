from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli_anahtar'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kullanicilar.db'


@app.route('/')
def home():
    return redirect(url_for('login'))


# Ana uploads klasörü
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Kullanıcı modeli
class Kullanici(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kullanici_adi = db.Column(db.String(150), unique=True, nullable=False)
    sifre = db.Column(db.String(150), nullable=False)

# Kullanıcı yükleme fonksiyonu
@login_manager.user_loader
def load_user(user_id):
    return Kullanici.query.get(int(user_id))

# İzin verilen dosya türleri
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Kullanıcıya özel klasör oluştur
def get_user_folder():
    folder = os.path.join(app.config['UPLOAD_FOLDER'], current_user.kullanici_adi)
    os.makedirs(folder, exist_ok=True)
    return folder

# Kayıt
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        kullanici_adi = request.form.get('kullanici_adi')
        sifre = request.form.get('sifre')

        # Kullanıcı adı uzunluk kontrolü
        if len(kullanici_adi) < 8:
            flash('Kullanıcı adı en az 8 karakter olmalıdır.', 'error')
            return redirect(url_for('register'))

        # Şifre büyük harf ve rakam kontrolü
        if not re.search(r'[A-Z]', sifre):
            flash('Şifre en az bir büyük harf içermelidir.', 'error')
            return redirect(url_for('register'))
        if not re.search(r'[0-9]', sifre):
            flash('Şifre en az bir rakam içermelidir.', 'error')
            return redirect(url_for('register'))

        kullanici_var_mi = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()
        if kullanici_var_mi:
            flash('Bu kullanıcı adı zaten alınmış.', 'error')
            return redirect(url_for('register'))

        yeni_kullanici = Kullanici(
            kullanici_adi=kullanici_adi,
            sifre=generate_password_hash(sifre, method='pbkdf2:sha256')
        )
        db.session.add(yeni_kullanici)
        db.session.commit()
        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Giriş
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        kullanici_adi = request.form.get('kullanici_adi')
        sifre = request.form.get('sifre')

        kullanici = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()
        if not kullanici or not check_password_hash(kullanici.sifre, sifre):
            flash('Kullanıcı adı veya şifre hatalı.', 'error')
            return redirect(url_for('login'))

        login_user(kullanici)
        return redirect(url_for('dashboard'))

    return render_template('login.html')

# Panel
@app.route('/dashboard')
@login_required
def dashboard():
    user_folder = get_user_folder()
    dosyalar = os.listdir(user_folder)
    return render_template('dashboard.html', dosyalar=dosyalar)

# Dosya yükleme
@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'dosya' not in request.files:
        flash('Dosya bulunamadı.', 'error')
        return redirect(url_for('dashboard'))

    file = request.files['dosya']

    if file.filename == '':
        flash('Dosya seçilmedi.', 'error')
        return redirect(url_for('dashboard'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_folder = get_user_folder()
        file.save(os.path.join(user_folder, filename))
        flash('Dosya başarıyla yüklendi.', 'success')
    else:
        flash('İzin verilmeyen dosya formatı.', 'error')

    return redirect(url_for('dashboard'))

# Dosya indirme
@app.route('/uploads/<filename>')
@login_required
def download_file(filename):
    user_folder = get_user_folder()
    return send_from_directory(user_folder, filename, as_attachment=True)

# Dosya silme
@app.route('/delete/<filename>')
@login_required
def delete_file(filename):
    try:
        user_folder = get_user_folder()
        os.remove(os.path.join(user_folder, filename))
        flash('Dosya başarıyla silindi.', 'success')
    except Exception as e:
        flash('Dosya silinemedi: ' + str(e), 'error')
    return redirect(url_for('dashboard'))

# Çıkış
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yapıldı.', 'success')
    return redirect(url_for('login'))

# Veritabanını oluştur
with app.app_context():
    db.create_all()

# Uygulama başlatma
if __name__ == '__main__':
    app.run(debug=True)
