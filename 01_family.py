# -*- coding: utf-8 -*-
import random

from termcolor import cprint


######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:

    def __init__(self):
        self.money = 100
        self.food = 50
        self.dirt = 0
        self.bowl_for_cat = 90
        self.earned_money = 0
        self.eated_food = 0
        self.buying_fur_coat = 0

    def __str__(self):
        return f"В доме денег - {self.money}, еды - {self.food}, грязи - {self.dirt}, " \
               f"еды для кота - {self.bowl_for_cat}"


class Human:
    def __init__(self, name, house):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.house = house

    def __str__(self):
        return f"Я {self.name}, сытость - {self.fullness}, счастье - {self.happiness}"

    def get_a_cat(self, house, cat):
        self.house = house
        self.cat = cat
        self.cat.house = house
        self.cat.fullness -= 10
        cprint(f"{self.name} подобрал кота по имени {self.cat.name}", color="cyan")

    def eat(self):
        if self.house.food <= 0:
            cprint(f"Еды нет", color="yellow")
            self.fullness -= 10
        else:
            self.house.food -= min(self.house.food, 30)
            self.fullness += min(self.fullness, 30)
            self.house.eated_food += min(self.fullness, 30)
            cprint(f"{self.name} поел(а)", color="yellow")

    def stroking_the_cat(self):
        self.happiness += 5
        cprint(f"{self.name} погладил(а) кота", color="yellow")
        self.fullness -= 10

    def get_food_to_cat(self):
        if self.house.money <= 10:
            self.fullness -= 10
            return f"Денег нет"
        else:
            self.house.bowl_for_cat += min(self.house.money, 150)
            self.house.money -= min(self.house.money, 150)
            cprint(f"{self.name} купил(а) еды коту", color="green")
        self.fullness -= 10

    def act(self):
        if self.house.dirt > 90:
            self.happiness -= 10
        if not self.is_alive:
            cprint(f"{self.name} умер(ла)...", color="red")
            return True
        elif self.fullness <= 30:
            self.eat()
            return True

    @property
    def is_alive(self):
        return self.fullness > 0 and self.happiness >= 10


class Husband(Human):

    def act(self):
        if super().act():
            return
        elif self.house.money <= 200:
            self.work()
        elif self.house.bowl_for_cat <= 30:
            self.get_food_to_cat()
        elif self.happiness <= 50:
            self.gaming()
        else:
            self.stroking_the_cat()

    def work(self):
        self.fullness -= 10
        salary = random.randint(50, 400)
        self.house.money += salary
        self.house.earned_money += salary
        cprint(f"{self.name} сходил на работу", color="yellow")

    def gaming(self):
        self.fullness -= 10
        self.happiness += 20
        cprint(f"{self.name} поиграл", color="yellow")


class Wife(Human):

    def act(self):
        dice_wife = random.randint(1, 2)
        if super().act():
            return
        elif self.house.food <= 100:
            self.shopping()
        elif self.house.bowl_for_cat <= 100:
            self.get_food_to_cat()
        elif self.house.dirt >= 50:
            self.clean_house()
        elif dice_wife == 1:
            self.buy_fur_coat()
        else:
            self.stroking_the_cat()

    def shopping(self):
        if self.house.money <= 10:
            cprint(f"{self.name} пришла без покупок, т.к. денег нет", color="blue")
        else:
            self.house.money -= min(self.house.money, 150)
            self.house.food += min(self.house.money, 150)
            cprint(f"{self.name} сходила в магазин за продуктами", color="blue")
        self.fullness -= 10

    def buy_fur_coat(self):
        if self.house.money < 350:
            cprint(f"{self.name} осталась без щубы, т.к. не хватило денег", color="blue")
        else:
            self.happiness += 60
            self.house.money -= 350
            self.house.buying_fur_coat += 1
            cprint(f"{self.name} купила шубу", color="blue")
        self.fullness -= 10

    def clean_house(self):
        self.fullness -= 10
        self.house.dirt -= min(self.house.dirt, 100)
        cprint(f"{self.name} убралась в доме", color="blue")


class Cat:

    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.house = None

    def __str__(self):
        return f"Я - {self.name}, сытость {self.fullness}"

    def act(self):
        if not self.is_alive:
            cprint(f"{self.name} умер...", color="red")
            return
        dice = random.randint(1, 2)
        if self.fullness <= 20:
            self.eat()
        elif dice == 1:
            self.sleep()
        else:
            self.soil()

    def eat(self):
        if self.house.bowl_for_cat <= 10:
            cprint(f"{self.name} остался голодным, срочно нужна еда", color="yellow")
            self.fullness -= 10
        else:
            self.fullness += 20
            self.house.bowl_for_cat -= 10
            cprint(f"{self.name} поел", color="yellow")

    def sleep(self):
        self.fullness -= 10
        cprint(f"{self.name} поспал", color="yellow")

    def soil(self):
        self.fullness -= 10
        self.house.dirt += 5
        cprint(f"{self.name} подрал обои", color="yellow")

    @property
    def is_alive(self):
        return self.fullness > 0


class Child(Human):

    def act(self):
        if super().act():
            return
        else:
            self.sleep()

    def eat(self):
        if self.house.food < 10:
            cprint(f"Еды нет", color="yellow")
        else:
            self.fullness += 10
            self.house.food -= 10
            self.house.eated_food += 10
            cprint(f"{self.name} поел(а)", color="yellow")

    def sleep(self):
        self.fullness -= 10
        cprint(f"{self.name} поспала", color="yellow")


home = House()
family = [
    Husband(name='Сережа', house=home),
    Wife(name='Маша', house=home),
    Child(name="Мальвина", house=home)
]

cats = [
    Cat(name='Мурзик'),
    Cat(name="Кусик"),
    Cat(name="Басик"),
]


def family_life():
    for cat in cats:
        family[0].get_a_cat(house=home, cat=cat)
    for day in range(1, 366):
        cprint('================== День {} =================='.format(day), color='red')
        if not all(human.is_alive for human in family) or not all(cat.is_alive for cat in cats):
            print("Нельзя жить с трупом в одном доме")
            break
        if day % (365 // 6) == 0:
            home.food = home.food / 2
            cprint("Пропала половина еды!!", color="red")
        if day % (365 // 7) == 0:
            home.money = home.money / 2
            cprint("Пропала половина денег!!", color="red")
        home.dirt += 5
        for human in family:
            human.act()
        for cat in cats:
            cat.act()
        for human in family:
            cprint(human, color='cyan')
        for cat in cats:
            cprint(cat, color='cyan')
        cprint(home, color='cyan')

    print("Заработано денег:", home.earned_money)
    print("Съедено еды:", home.eated_food)
    print("Куплено шуб:", home.buying_fur_coat)


n = 3
while True:
    family_life()
    if not all(human.is_alive for human in family) or not all(cat.is_alive for cat in cats):
        break
    else:
        cats.append(Cat(name=f"Доп. Кот № К00{len(cats) - 2}"))
        n += 1
        home.money = 100
        home.food = 50
        home.dirt = 0
        home.bowl_for_cat = 90
        for human in family:
            human.fullness = 30
            human.happiness = 100
        for cat in cats:
            cat.fullness = 30

print("\nМаксимальное количество котов - ", n - 1)

######################################################## Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов


######################################################## Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)


######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов

#
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')
# зачет!