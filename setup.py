from setuptools import setup

setup(
    name="pasgen",
    version="1.0",
    packages=['pasgen'],  # Eğer tek bir .py dosyanız varsa, bunu değiştirebilirsiniz.
    install_requires=[
        'pyqt5',  # PyQt5 bağımlılığı
    ],
    package_data={
        '': ['*.png', '*.desktop'],  # Kök dizindeki .png ve .desktop dosyalarını ekler
    },
    data_files=[
        ('share/applications', ['pasgen.desktop']),  # Uygulama menüsüne .desktop dosyasını ekler
        ('share/icons/hicolor/48x48/apps', ['pasgenlo.png']),  # Simgeyi uygun bir yere ekler
    ],
    entry_points={
        'gui_scripts': [
            'pasgen=pasgen:main',  # Uygulamanın giriş noktası (main fonksiyonunu buraya eklemelisiniz)
        ]
    },
)

