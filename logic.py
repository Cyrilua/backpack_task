# массив с весами предметов
def get_item_weights(items_dict):
    item_weights = []
    for item in items_dict:
        item_weights.append(items_dict[item][0])
    return item_weights


# массив со стоимостями предметов
def get_item_values(items_dict):
    item_values = []
    for item in items_dict:
        item_values.append(items_dict[item][1])
    return item_values


def get_memory_table(items_dict, weight_limit, item_weights, item_values):
    items_quantity = len(items_dict)  # находим размеры таблицы
    # создаём таблицу из нулевых значений
    memory_table = []
    for i in range(items_quantity + 1):
        memory_table.append([])
        for j in range(weight_limit + 1):
            memory_table[i].append(0)
    # У нас есть таблица memory_table размера N на W, где N - количество предметов, а W - максимальный вес рюкзака.
    # В memory_table[i][j] мы будем хранить объект, который описывает,
    # какую максимальную сумму и вес можно набрать, если использовать предметы a1,a2,...,ai
    # (предполагается, что все предметы, которые поданы на вход, пронумерованы от 0 до N-1).
    # При этом вес не должен превышать j.

    # На каждом шаге для расчета memory_table[i][j] у нас есть три варианта:
    # - Мы можем взять те же предметы, что и в memory_table[i-1][j].
    # Мы точно знаем, что они поместятся, поскольку сумма вещей не превышает j.
    # - Мы можем взять текущий i-й предмет веса w и взять memory_table[i][j-w],
    # они тоже поместятся, потому что мы зарезервировали место для них, вычитая из j текущий вес w.
    # Нужно учесть, что memory_table[i][j-w] может не существовать, потому в программе стоит условие.
    # - Мы можем взять текущий i-й предмет веса w и взять memory_table[i-1][j-w]. Тут то же самое, что и пунктом выше.
    # Из всех вариантов выше выбираем тот, в котором мы получаем наибольшую стоимость
    for i in range(items_quantity + 1):
        for j in range(weight_limit + 1):
            # базовый случай
            if i == 0 or j == 0:
                memory_table[i][j] = 0
            # если площадь предмета меньше площади столбца, максимизируем значение суммарной стоимости
            elif item_weights[i - 1] <= j:
                memory_table[i][j] = max(item_values[i - 1] + memory_table[i - 1][j - item_weights[i - 1]],
                                         memory_table[i - 1][j])
            # если вес предмета больше веса столбца, забираем значение ячейки из предыдущей строки
            else:
                memory_table[i][j] = memory_table[i - 1][j]

    for i in memory_table:
        print(i)
    print()
    return memory_table


def get_selected_items_list(items_dict, weight_limit):
    item_weights = get_item_weights(items_dict)
    item_values = get_item_values(items_dict)
    memory_table = get_memory_table(items_dict, weight_limit, item_weights, item_values)
    items_quantity = len(items_dict)

    foo = memory_table[items_quantity][weight_limit]  # начинаем с последнего элемента таблицы
    weights_and_values_list = []  # список весов и стоимостей

    for i in range(items_quantity, 0, -1):  # идём в обратном порядке
        if foo <= 0:  # условие остановки - собрали рюкзак
            break
        if foo == memory_table[i - 1][weight_limit]:  # ничего не делаем, двигаемся дальше
            continue
        else:
            # забираем предмет
            weights_and_values_list.append((item_weights[i - 1], item_values[i - 1]))
            foo -= item_values[i - 1]  # отнимаем значение стоимости от общей
            weight_limit -= item_weights[i - 1]  # отнимаем вес от общего

    selected_items = []

    # заполняем массив названиями выбранных предметов для вывода на экран
    for e in weights_and_values_list:
        for key, item_values in items_dict.items():
            if item_values == e and not selected_items.__contains__(key):
                selected_items.append(key)
    return selected_items

