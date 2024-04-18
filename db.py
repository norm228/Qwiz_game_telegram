import sqlite3


class DataB:
    def __init__(self):
        self.con = sqlite3.connect("Qwiz_game_telegram/source/base.db")
        self.con1 = sqlite3.connect("Qwiz_game_telegram/source/pic_base.db")
        self.cur = self.con.cursor()
        self.cur1 = self.con1.cursor()
        self.createnewtable()
        self.createnewtable_with_images()
        self.con.commit()
        self.con1.commit()
        self.add_to_table_w_i('Кто изображен на картинке?', 'Qwiz_game_telegram/pictures/img11.png', 1,
                              '"Райан Гослинг" "Алеша Попович" "Брэд Пит"', '"Человек паук"')
        self.add_to_table_w_i('Что изображено на картинке?', 'Qwiz_game_telegram/pictures/img12.png', 1,
                              '"Круг" "Морфологический разбор" "Квадрат"', '"Трегольник"')
        self.add_to_table_w_i('С чем связана данное изображение?', 'Qwiz_game_telegram/pictures/img13.png', 1,
                              '"День Святого Валентина" "День Святого Патрика" "Николай Валуев"', '"Новый Год"')
        self.add_to_table_w_i('С каким процессом связана картинка?', 'Qwiz_game_telegram/pictures/img21.png', 2,
                              '"Продажа диванов" "Миграция уток" "34"', '"Преобразование растения в торф"')
        self.add_to_table_w_i('Владельцем какой компании является человек на фото?',
                              'Qwiz_game_telegram/pictures/img22.png',
                              2,
                              '"Озон" "Бентли" "Амазон"', '"Форд"')
        self.add_to_table_w_i('Где были изобретены первые часы?', 'Qwiz_game_telegram/pictures/img23.png', 2,
                              '"Рим" "Люксембург" "Шумеры"', '"Древний Египет"')
        self.add_to_table_w_i('Какое событие отражено на картине?', 'Qwiz_game_telegram/pictures/img31.png', 3,
                              '"Резня старообрядцев" "Празднование пасхи" "Римская революция"',
                              '"Варфоломеевская ночь"')
        self.add_to_table_w_i('Что изображено на чертеже?', 'Qwiz_game_telegram/pictures/img32.png', 3,
                              '"Мотор лодки" "Подвеска Audi Q6" "Двигатель трактора"', '"Двигатель белаза"')
        self.add_to_table_w_i('Где находится данное здание?', 'Qwiz_game_telegram/pictures/img33.png', 3,
                              '"Германия" "Англия" "Черногория"', '"Россия"')
        self.add_to_table_w_i('Какое вещество здесь изображено?', 'Qwiz_game_telegram/pictures/img41.png', 4,
                              '"Кремний" "Алмаз" "Серебро"', '"Палладий"')
        self.add_to_table_w_i('Отгадайте загадку?', 'Qwiz_game_telegram/pictures/img42.png', 4,
                              '"Электрон" "Закон тяготения" "Микросхема"', '"Электромагнитное поле"')
        self.add_to_table_w_i('Кем была написана данная картина?', 'Qwiz_game_telegram/pictures/img43.png', 4,
                              '"Английским художником" "Французским художником" "Прусским художником"',
                              '"Австрийским художником"')
        self.add_to_table_w_i('От чего эта схема?', 'Qwiz_game_telegram/pictures/img51.png', 5,
                              '"От монитора" " От роутера" "От фонарика"', '"От пылесоса"')
        self.add_to_table_w_i('Чей данный логотип?', 'Qwiz_game_telegram/pictures/img52.png', 5,
                              '"Tostitos" "Ferrari" "Berkshire"', '"Roxy"')
        self.add_to_table_w_i('Переведите сообщение:', 'Qwiz_game_telegram/pictures/img53.png', 5,
                              '"Важно - никогда не сдавайся!" "Порхай - как красивая бабочка!" "Черепаха"',
                              '"Квест - это очень веселая затея!"')
        self.add_to_table('К какому типу относится яблоко?', 1, 'Овощ Ягода Корнеплод Фрукт',
                          'Фрукт')
        self.add_to_table('2+2=', 1, '1, 2, 3', '4')
        self.add_to_table('На какой планете мы живем?', 1, 'Венера Сатурн Нептун', 'Земля')
        self.add_to_table('Кем является бобер?', 2, 'Птицей Насекомым Поляком',
                          'Млекопитающим')
        self.add_to_table('Из чего сделан стул, если он :\n '
                          'скрипит, шершавый на ощупь, легковоспламеняющийся?\n Из ____', 2,
                          'пластика полиетилена пенапласта', 'дерева')
        self.add_to_table('Назови столицу Китая', 2, 'Лондон Москва Сарай', 'Пекин')
        self.add_to_table('Назови машину немецкого производства', 3,
                          '"Mozo" "Toyota Mark II" "DAB"', '"Daimler Grafton Phaeton"')
        self.add_to_table('Кто из них может быть русским поэтом??', 3,
                          'К.В.Эккерсберг Н.В.Гоголь РайанГослинг', 'А.С.Пушкин')
        self.add_to_table('Из чего сделан корпус телефона?', 3,
                          'Сталь Пластик Адамантий', 'Металл')
        self.add_to_table('В каком году была основана первая космическая станция "Мир"?', 4,
                          '1971  1973 1976 ', '1985')
        self.add_to_table('Какое из следующих произведений Шекспира было написано последним?', 4,
                          '"Гамлет" "Король Лир" "Отелло"', '"Два благородных родственника"')
        self.add_to_table('Из чего сделан корпус телефона?', 4,
                          'Сталь Пластик Адамантий', 'Металл')
        self.add_to_table('Назови формулу пороха', 5,
                          'CuO (NH2)2CO CO2', 'KNO3')
        self.add_to_table('Кто из перечисленных деятелей был номинирован на Нобелевскую премию по литературе?', 5,
                          '"Jorge Luis Borges" "Virginia Woolf" "Leo Tolstoy"', '"Ivan Bunin"')
        self.add_to_table('Кто из перечисленных ученых не '
                          'получил Нобелевскую премию по физике за открытие квантовой механики?', 5,
                          '"Ален Аспе" "Джон Клаузер" "Антон Цайлингер"', '"Пауль Дирак"')

    def createnewtable(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS base (
        id INTEGER,
        question TEXT,
        level INTEGER,
        answers TEXT,
        r_answer TEXT
        )''')

        self.con.commit()

    def createnewtable_with_images(self):
        self.cur1.execute('''CREATE TABLE IF NOT EXISTS pic_base (
                id INTEGER,
                question TEXT,
                pic BLOB,
                level INTEGER,
                answers TEXT,
                r_answer TEXT
                )''')

    def convert_to_binary_data(self, filename: str):
        with open(filename, 'rb') as file:
            bi_data = file.read()
        return bi_data

    def add_to_table(self, question: str, level: int, answers: str, r_answer: str):
        some_tuple = (question, level, answers, r_answer)
        some_add = '''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?, ?)'''
        self.cur.execute(some_add, some_tuple)
        self.con.commit()

    def add_to_table_w_i(self, question: str, pic, level: int, answers: str, r_answer: str):
        bi_pic = self.convert_to_binary_data(pic)
        some_tuple = (question, bi_pic, level, answers, r_answer)
        some_add = '''INSERT INTO pic_base (question, pic, level, answers, r_answer) VALUES (?, ?, ?, ?, ?)'''
        self.cur1.execute(some_add, some_tuple)
        self.con1.commit()
