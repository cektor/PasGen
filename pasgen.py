from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QSlider, QPushButton, QLineEdit, QMessageBox, QComboBox, QProgressBar, QRadioButton, QGroupBox
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QClipboard, QFont, QIcon, QPixmap, QColor, QPalette
import random
import string
import sys
import os

def get_logo_path():
    """Logo dosyasının yolunu döndürür."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "pasgenlo.png")
    elif os.path.exists("/usr/share/icons/hicolor/48x48/apps/pasgenlo.png"):
        return "/usr/share/icons/hicolor/48x48/apps/pasgenlo.png"
    elif os.path.exists("pasgenlo.png"):
        return "pasgenlo.png"
    return None

def get_icon_path():
    """Simge dosyasının yolunu döndürür."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "pasgenlo.png")
    elif os.path.exists("/usr/share/icons/hicolor/48x48/apps/pasgenlo.png"):
        return "/usr/share/icons/hicolor/48x48/apps/pasgenlo.png"
    return None

LOGO_PATH = get_logo_path()
ICON_PATH = get_icon_path()

class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        # QSettings ile dil ayarlarını yükle
        self.settings = QSettings("PasGen", "settings")
        
        # UI'yi başlat
        self.initUI()
        
        # Ayarları yükle
        self.loadSettings()
        self.password_history = []

    def loadSettings(self):
        # Dil ayarlarını yükle
        current_language = self.settings.value("language", "tr")
        self.settings.setValue("language", current_language)
        self.updateUI()

    def initUI(self):
        self.setWindowTitle(self.translate("PasGen"))
        self.setGeometry(100, 100, 500, 400)
        
        # Form boyutunun sabit olması için
        self.setFixedSize(450, 630)  # Sabit boyut

        # Varsayılan koyu tema (artık tema değişimi olmayacak)
        self.setStyleSheet("background-color: #2d2d2d; color: white;")

        # Ana layout
        layout = QVBoxLayout()

        # Dil seçimi combobox
        self.combo_language = QComboBox()
        self.combo_language.addItem("Türkçe")
        self.combo_language.addItem("English")
        self.combo_language.currentIndexChanged.connect(self.changeLanguage)
        layout.addWidget(self.combo_language)

        if LOGO_PATH:
            self.logo_label = QLabel(self)  # Logo için QLabel oluştur
            pixmap = QPixmap(LOGO_PATH)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(scaled_pixmap)  # Logo resmini set et
            self.logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.logo_label)  # Logo'yu layout'a ekle    

        # Parola uzunluğu
        self.label_length = QLabel(self.translate("Password Length: 8"))
        layout.addWidget(self.label_length)

        self.slider_length = QSlider(Qt.Horizontal)
        self.slider_length.setMinimum(4)
        self.slider_length.setMaximum(32)
        self.slider_length.setValue(8)
        self.slider_length.valueChanged.connect(self.updateLengthLabel)
        layout.addWidget(self.slider_length)

        # Parola güvenlik göstergesi
        self.security_bar = QProgressBar()
        self.security_bar.setRange(0, 100)
        layout.addWidget(self.security_bar)

        # Karakter seçenekleri
        self.checkbox_uppercase = QCheckBox(self.translate("Uppercase"))
        self.checkbox_uppercase.setChecked(True)
        layout.addWidget(self.checkbox_uppercase)

        self.checkbox_lowercase = QCheckBox(self.translate("Lowercase"))
        self.checkbox_lowercase.setChecked(True)
        layout.addWidget(self.checkbox_lowercase)

        self.checkbox_numbers = QCheckBox(self.translate("Numbers"))
        self.checkbox_numbers.setChecked(True)
        layout.addWidget(self.checkbox_numbers)

        self.checkbox_special = QCheckBox(self.translate("Special Characters"))
        self.checkbox_special.setChecked(True)
        layout.addWidget(self.checkbox_special)

        # Parola türü seçimi (Kategori)
        self.groupbox_type = QGroupBox(self.translate("Password Type"))
        self.layout_type = QVBoxLayout()
        self.radio_account = QRadioButton(self.translate("Account Password"))
        self.radio_wifi = QRadioButton(self.translate("Wi-Fi Password"))
        self.radio_custom = QRadioButton(self.translate("Custom Password"))
        self.radio_account.setChecked(True)  # Varsayılan: Hesap Parolası
        self.layout_type.addWidget(self.radio_account)
        self.layout_type.addWidget(self.radio_wifi)
        self.layout_type.addWidget(self.radio_custom)
        self.groupbox_type.setLayout(self.layout_type)
        layout.addWidget(self.groupbox_type)

        # Parola alanı ve oluştur düğmesi
        self.input_password = QLineEdit()
        self.input_password.setReadOnly(True)
        self.input_password.mousePressEvent = self.copyToClipboard  # Mouse tıklama ile panoya kopyala
        layout.addWidget(self.input_password)

        self.button_generate = QPushButton(self.translate("Generate Password"))
        self.button_generate.clicked.connect(self.generatePassword)
        layout.addWidget(self.button_generate)

        # Geçmiş parolalar butonu
        self.button_show_history = QPushButton(self.translate("Show Password History"))
        self.button_show_history.clicked.connect(self.showHistory)
        layout.addWidget(self.button_show_history)

        # Parola gizleme / gösterme butonu
        self.button_toggle_password = QPushButton(self.translate("Show Password"))
        self.button_toggle_password.clicked.connect(self.togglePasswordVisibility)
        layout.addWidget(self.button_toggle_password)

        # Parola sıfırlama butonu
        self.button_reset = QPushButton(self.translate("Reset"))
        self.button_reset.clicked.connect(self.resetSettings)
        layout.addWidget(self.button_reset)

        # Hakkında butonu
        self.button_about = QPushButton(self.translate("About"), self)
        self.button_about.setFont(QFont("Arial", 10))
        self.button_about.clicked.connect(self.show_about)

        self.button_about.setStyleSheet("""
            QPushButton {
                background-color: #353535;
                color: white;
                border: 1px solid gray;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #454545;
            }
        """)
        layout.addWidget(self.button_about)

        self.setLayout(layout)
        self.selected_path = None
        self.setAcceptDrops(True)

    def updateLengthLabel(self):
        length = self.slider_length.value()
        self.label_length.setText(self.translate(f"Password Length: {length}"))

    def generatePassword(self):
        length = self.slider_length.value()
        use_uppercase = self.checkbox_uppercase.isChecked()
        use_lowercase = self.checkbox_lowercase.isChecked()
        use_numbers = self.checkbox_numbers.isChecked()
        use_special = self.checkbox_special.isChecked()

        character_pool = ""
        if use_uppercase:
            character_pool += string.ascii_uppercase
        if use_lowercase:
            character_pool += string.ascii_lowercase
        if use_numbers:
            character_pool += string.digits
        if use_special:
            character_pool += string.punctuation

        if not character_pool:
            QMessageBox.warning(self, self.translate("Warning"), self.translate("At least one character type must be selected!"))
            return

        # Seçilen parolanın tipine göre karakter eklemeleri
        if self.radio_account.isChecked():
            character_pool += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        elif self.radio_wifi.isChecked():
            character_pool += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"

        password = ''.join(random.choice(character_pool) for _ in range(length))
        self.input_password.setText(password)

        # Güvenlik derecesini değerlendirme
        self.evaluatePasswordSecurity(password)

        # Parolayı geçmişe kaydet
        self.password_history.append(password)

    def evaluatePasswordSecurity(self, password):
        score = 0
        # Güvenlik skoru hesaplama
        if len(password) >= 12:
            score += 30
        if any(c.islower() for c in password):
            score += 20
        if any(c.isupper() for c in password):
            score += 20
        if any(c.isdigit() for c in password):
            score += 20
        if any(c in string.punctuation for c in password):
            score += 10

        self.security_bar.setValue(score)

    def showHistory(self):
        history = "\n".join(self.password_history[-5:])  # Son 5 parolayı göster
        QMessageBox.information(self, self.translate("Password History"), history)

    def togglePasswordVisibility(self):
        if self.input_password.echoMode() == QLineEdit.Normal:
            self.input_password.setEchoMode(QLineEdit.Password)
            self.button_toggle_password.setText(self.translate("Show Password"))
        else:
            self.input_password.setEchoMode(QLineEdit.Normal)
            self.button_toggle_password.setText(self.translate("Hide Password"))

    def resetSettings(self):
        self.slider_length.setValue(8)
        self.checkbox_uppercase.setChecked(True)
        self.checkbox_lowercase.setChecked(True)
        self.checkbox_numbers.setChecked(True)
        self.checkbox_special.setChecked(True)
        self.radio_account.setChecked(True)

    def copyToClipboard(self, event):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.input_password.text())
        QMessageBox.information(self, self.translate("Copied to Clipboard"), self.translate("Password has been copied to clipboard!"))

    def translate(self, text):
        """Metin için uygun dil çevirisini döndürür."""
        current_language = self.settings.value("language", "tr")
        translations = {
            "tr": {
                "Password Length: 8": "Parola Uzunluğu: 8",
                "Uppercase": "Büyük Harfler",
                "Lowercase": "Küçük Harfler",
                "Numbers": "Sayılar",
                "Special Characters": "Özel Karakterler",
                "Password Type": "Parola Tipi",
                "Account Password": "Hesap Parolası",
                "Wi-Fi Password": "Wi-Fi Parolası",
                "Custom Password": "Özel Parola",
                "Generate Password": "Parola Oluştur",
                "Show Password History": "Parola Geçmişini Göster",
                "Show Password": "Parolayı Göster",
                "Hide Password": "Parolayı Gizle",
                "Reset": "Sıfırla",
                "About": "Hakkında",
                "Copied to Clipboard": "Panoya Kopyalandı",
                "Password has been copied to clipboard!": "Parola panoya kopyalandı!",
                "Password History": "Parola Geçmişi",
                "Warning": "Uyarı",
                "At least one character type must be selected!": "En az bir karakter tipi seçilmelidir!"
            },
            "en": {
                "Password Length: 8": "Password Length: 8",
                "Uppercase": "Uppercase",
                "Lowercase": "Lowercase",
                "Numbers": "Numbers",
                "Special Characters": "Special Characters",
                "Password Type": "Password Type",
                "Account Password": "Account Password",
                "Wi-Fi Password": "Wi-Fi Password",
                "Custom Password": "Custom Password",
                "Generate Password": "Generate Password",
                "Show Password History": "Show Password History",
                "Show Password": "Show Password",
                "Hide Password": "Hide Password",
                "Reset": "Reset",
                "About": "About",
                "Copied to Clipboard": "Copied to Clipboard",
                "Password has been copied to clipboard!": "Password has been copied to clipboard!",
                "Password History": "Password History",
                "Warning": "Warning",
                "At least one character type must be selected!": "At least one character type must be selected!"
            }
        }
        return translations.get(current_language, translations["tr"]).get(text, text)

    def changeLanguage(self):
        """Dil değiştirildiğinde ayarları kaydet ve arayüzü güncelle."""
        language = self.combo_language.currentText()
        self.settings.setValue("language", "tr" if language == "Türkçe" else "en")
        self.updateUI()

    def updateUI(self):
        """Arayüzü günceller ve öğeleri çevirir."""
        self.label_length.setText(self.translate("Password Length: 8"))
        self.checkbox_uppercase.setText(self.translate("Uppercase"))
        self.checkbox_lowercase.setText(self.translate("Lowercase"))
        self.checkbox_numbers.setText(self.translate("Numbers"))
        self.checkbox_special.setText(self.translate("Special Characters"))
        self.groupbox_type.setTitle(self.translate("Password Type"))
        self.radio_account.setText(self.translate("Account Password"))
        self.radio_wifi.setText(self.translate("Wi-Fi Password"))
        self.radio_custom.setText(self.translate("Custom Password"))
        self.button_generate.setText(self.translate("Generate Password"))
        self.button_show_history.setText(self.translate("Show Password History"))
        self.button_reset.setText(self.translate("Reset"))
        self.button_about.setText(self.translate("About"))
        self.setWindowTitle(self.translate("PasGen"))

    def show_about(self):
        """Hakkında penceresini gösterir."""
        about_text = (
        "PasGen | PASsword GENeratorn \n\n"
        "PasGen, kullanıcıların güçlü ve güvenli parolalar oluşturmasına yardımcı olan bir masaüstü uygulamasıdır. Kullanıcılar, parola uzunluğunu, içerik türlerini (büyük harf, küçük harf, rakamlar, özel karakterler) ve parola türünü (hesap parolası, Wi-Fi parolası, özel parola) seçerek kişisel ihtiyaçlarına uygun parolalar oluşturabilirler. Ayrıca, önceki oluşturulan parolaların kaydını tutarak kolayca erişim sağlar. Uygulama, Türkçe ve İngilizce dil desteği sunar ve şifre güvenliği hakkında bilgi vermek için bir güvenlik göstergesi de içerir. Uygulama, kullanıcı dostu arayüzü ve çeşitli özellikleriyle parola güvenliğini basit ve etkili bir şekilde sağlamayı hedefler.\n\n"
        "Geliştirici: ALG Yazılım Inc.©\n"
        "www.algyazilim.com | info@algyazilim.com\n\n"
        "Fatih ÖNDER (CekToR) | fatih@algyazilim.com\n"
        "GitHub: https://github.com/cektor\n\n"
        "ALG Yazılım Pardus'a Göç'ü Destekler.\n\n"
        "Sürüm: 1.0"
        )
        # Hakkında penceresini doğru şekilde göster
        QMessageBox.information(self, "PasGen Hakkında", about_text, QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
        # Simgeyi ayarla
    if ICON_PATH:
        app.setWindowIcon(QIcon(ICON_PATH))
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())
