import matplotlib.pyplot as plt
import numpy as np

# Данные и названия категорий
data = [10, 15, 25, 50, 5, 20]
categories = ['Категория 1', 'Категория 2', 'Категория 3', 'Категория 4', 'Категория 5', 'Категория 6']

# Создание массива цветов
colors = plt.cm.viridis(np.linspace(0, 1, len(data)))

# Указание "выдвижения" для каждого сегмента (подсветим одну из категорий)
explode = [0.1 if i == np.argmax(data) else 0.05 for i in range(len(data))]

# Построение круговой диаграммы с более сложными параметрами
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    data,
    labels=categories,
    autopct='%1.1f%%',
    startangle=140,
    colors=colors,
    explode=explode,
    shadow=True,
    wedgeprops={'edgecolor': 'black', 'linewidth': 1.2}
)

# Настройка внешнего вида текста
for text in texts:
    text.set_fontsize(10)
    text.set_color('navy')
for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_color('white')
    autotext.set_weight('bold')

# Настройка заголовка и стиля
ax.set_title('Стильная круговая диаграмма для 6 категорий', fontsize=14, weight='bold', color='darkblue')
plt.show()
