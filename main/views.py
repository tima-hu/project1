from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from main.models import Product
from main.forms import ProductForm

# Create your views here.
def index(request):
    context = {
        'title': 'Geek',
        'image': 'https://jymysh.kg/media/orders/photos/Frame_38.webp',
        'description': 'Geek is a platform for learning programming and IT skills.',
        'title1:': 'computer',
        'image1': 'https://i.pinimg.com/736x/c4/6f/3a/c46f3af2166093bf0711a370807062b1.jpg',
        'description1': '''🖥️ Обзор и технические характеристики
ThinkPad X1 Carbon Gen 13 (Aura Edition, выпуск: 2024–2025)
Процессор: Intel Core Ultra 7 258V с интегрированной графикой Intel Arc Graphics 140V 
NOTES FOR SENIOR HIGH STUDENTS
+10
TechRadar
+10
laptopmedia.com
+10

Память: 32 GB LPDDR5x (soldered), без возможности апгрейда 
TechRadar

Накопитель: до 2 TB PCIe 5.0 SSD 
TechRadar

Экран: 14″ OLED-дисплей с разрешением 2.8K (2880 × 1800), 120 Hz, анти-отражающее покрытие 
Digital Trends
+6
TechRadar
+6
laptopmedia.com
+6

Корпус: карбоновый и магниевый сплав, вес всего около 0.99 кг (2.2 lb) 
TechRadar

Порты: 2 × Thunderbolt 4, 2 × USB‑A, HDMI 2.1, 3.5 mm аудио­разъём 
bhphotovideo.com
+3
TechRadar
+3
bhphotovideo.com
+3

Связь: Wi‑Fi 7, Bluetooth 5.4 
NOTES FOR SENIOR HIGH STUDENTS
+4
TechRadar
+4
laptopmedia.com
+4

Особенности безопасности: TPM 2.0, детектор посторонних зрителей, защита приватности, кнопка Aura Experience и др. 
TechRadar
WIRED

Батарея: 57 Wh, почти до 11–12 ч активной работы в реалистичном использовании, скорость зарядки хорошая 
bhphotovideo.com
+4
NOTES FOR SENIOR HIGH STUDENTS
+4
TechRadar
+4

🔍 Отзывы: аппарат хвалят за эргономику, клавиатуру, лёгкость и портативность — идеален для офисной работы и мобильного бизнеса 
TechRadar
WIRED
Digital Trends
Windows Central
.''',
        'title2': 'book',
        'image2': 'https://avatars.mds.yandex.net/i?id=5ee82fcc34f6c1ade4f14a8b3d6c032b48ed381e-9008017-images-thumbs&n=13',
        'description2': 'книга "Изучаем Python" — это идеальное руководство для начинающих и опытных программистов, желающих освоить язык Python. Книга охватывает основы синтаксиса, структуры данных, функции, модули и библиотеки, а также продвинутые темы, такие как работа с веб-технологиями и базами данных. Практические примеры и задания помогут закрепить полученные знания.',
        'title3': 'keyboard',
        'image3': 'https://masterpiecer-images.s3.yandex.net/ff1b1359a72d11ee882caa451a4af6da:upscaled',
        'description3': 'SteelSeries Apex Pro — топовая игровая механическая клавиатура с настраиваемыми переключателями OmniPoint 2.0, RGB-подсветкой, OLED-экраном и алюминиевым корпусом. Позволяет менять чувствительность клавиш, поддерживает макросы и имеет съёмную подставку под запястья. Одна из лучших для киберспорта и игр.',
        'title4': 'phone',
        'image4': 'https://avatars.mds.yandex.net/i?id=a1f97f31be21403b69f5eeff16d5130f06eb1565-5850342-images-thumbs&n=13',
        'description4': '''Vivo X200 Pro — флагманский смартфон, представленный в октябре 2024 и поступивший в продажу глобально с начала 2025 года. 
Diario AS
+15
Cinco Días
+15
Notebookcheck
+15

Процессор: MediaTek Dimensity 9400 на 3 нм с графикой Immortalis‑G925 и до 16 ГБ LPDDR5X + 512 ГБ или 1 ТБ UFS 4.0. 
Реддит
+10
vivo.com
+10
Википедия
+10

Экран: 6.78″ LTPO AMOLED, разрешение 2800×1260 (≈452–453 ppi), 120 Гц адаптивной частоты (0.1‑120 Гц), HDR10+, Dolby Vision, яркость до 4500 нит. 
vivo.com
+9
gsmarena.com
+9
whatmobile.com.pk
+9

Камеры: Тройная основная камера — 50 МП (широкоугольная, f/1.57 с OIS), 200 МП перископ (3.7× оптический зум, f/2.7‑2.65 с OIS) и 50 МП ультраширокая (119°). Фронтальная камера — 32 МП (поддержка записи 4K видео). 
Cinco Días
+15
gsmarena.com
+15
Notebookcheck
+15

Батарея и зарядка: ёмкость 6000 mAh, поддержка 90 W быстрой зарядки и 30 W беспроводной зарядки (в ряде регионов), резервное обратное зарядное. 
Cinco Días
+10
vivo.com
+10
Википедия
+10

Защита и материалы: корпус из стекла и алюминия, стандарт IP68/IP69 — влагозащита до 1.5 м / 30 мин, устойчивость к водяным струям высокого давления и пыли. 
gsmarena.com

''',  
        'title5': 'mouse',
        'image5': 'https://avatars.mds.yandex.net/i?id=eb3c82a9309bc5424b2953b7de64ed20869cda04-7056086-images-thumbs&n=13',
        'description5': 'Logitech G Pro X Superlight 2 — топовая игровая мышь весом всего 60 г, с сенсором HERO 2 (до 32 000 DPI), частотой отклика 2000 Гц и сверхточным отслеживанием. Беспроводная, с низкой задержкой и отличной эргономикой — идеальна для киберспорта.',
    }
    return render(request, 'index.html', context=context)

class ProductCreateView(CreateView):
        template_name = 'create.html'
        model = Product
        form_class = ProductForm
        success_url = reverse_lazy('index')