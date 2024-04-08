import sqlite3


class DataB:
    def __init__(self):
        self.con = sqlite3.connect("Qwiz_game_telegram/source/base.db")
        self.cur = self.con.cursor()
        self.createnewtable()
        self.con.commit()

    def createnewtable(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS base (
        id INTEGER PRIMARY KEY,
        question TEXT,
        level INTEGER,
        answers TEXT,
        r_answer TEXT
        )''')
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('К какому типу относится яблоко?', 1, 'Овощ Ягода Корнеплод Фрукт',
                          'b)Фрукт'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('2+2=', 1, '1, 2, 3', '4'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('На какой планете мы живем?', 1, 'Венера Сатурн Нептун', 'Земля'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('Кем является бобер?', 2, 'Птицей Насекомым Поляком',
                          'Млекопитающим'))
        self.cur.execute('''INSERT INTO base (question, level, answers, answer) VALUES (?, ?, ?, ?)''',
                         ('Из чего сделан стул, если он :\n '
                          'скрипит, шершавый на ощупь, легковоспламеняющийся?\n Из ____', 2,
                          'пластика полиетилена пенапласта', 'дерева'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('Назови столицу Китая', 2, 'Лондон Москва Сарай', 'Пекин'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('Назови машину немецкого производства', 3,
                          '"Mozo" "Toyota Mark II" "DAB"', '"Daimler Grafton Phaeton"'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('Кто из них может быть русским поэтом??', 3,
                          'К.В.Эккерсберг Н.В.Гоголь РайанГослинг', 'А.С.Пушкин'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('Из чего сделан корпус телефона?', 3,
                          'Сталь Пластик Адамантий', 'Металл'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('В каком году была основана первая космическая станция "Мир"?', 4,
                          '1971  1973 1976 ', '1985'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('Какое из следующих произведений Шекспира было написано последним?', 4,
                          '"Гамлет" "Король Лир" "Отелло"', '"Два благородных родственника"'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('Из чего сделан корпус телефона?', 4,
                          'Сталь Пластик Адамантий', 'Металл'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('Назови формулу пороха', 5,
                          'CuO (NH2)2CO CO2', 'KNO3'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('Кто из перечисленных деятелей был номинирован на Нобелевскую премию по литературе?', 5,
                          '"Jorge Luis Borges" "Virginia Woolf" "Leo Tolstoy"', '"Ivan Bunin"'))
        self.cur.execute('''INSERT INTO base (question, level, answers, r_answer) VALUES (?, ?, ?, ?)''',
                         ('Кто из перечисленных ученых не '
                          'получил Нобелевскую премию по физике за открытие квантовой механики?', 5,
                          '"Ален Аспе" "Джон Клаузер" "Антон Цайлингер"', '"Пауль Дирак"'))
        self.con.commit()



