import csv
import pandas as pd
from datetime import datetime
import re
import matplotlib.pyplot as plt


DATE_REGEX = re.compile(r'(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/((19|20)\d\d)')
DATE_REGEX_RANGE = re.compile(r'((19|20)\d\d)-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])')
CATEGORY = 'Category'
DATE = 'Date'
AMOUNT = 'Amount'

class BudgetCalculator:
    def __init__(self, file_name):
        self.file_name = file_name

    def write_to_file(self):
        print('Введите категорию расхода:')
        cat = input()
        while True:
            print('Введите дату, когда был совершён расход (в формате день/месяц/год):')
            date = input()
            if DATE_REGEX.match(date):
                date = datetime.strptime(date, "%d/%m/%Y")
                break
            else:
                print('Неверный формат даты, повторите ввод!')
        print('Введите сумму, которую вы потратили:')
        amount = input()
        data_spending = [cat, date, amount]
        with open(self.file_name, 'a', newline="", encoding='UTF-8') as csv_file:
            csv.writer(csv_file).writerow(data_spending)
        print('Расход успешно добавлен!')

    @staticmethod
    def expenses_all_time(df):
        print(df)

    @staticmethod
    def expenses_categories(df):
        print('По какой категории вы бы хотели посмотреть расходы?')
        cat = input()
        print(df.loc[df[CATEGORY] == cat])

    @staticmethod
    def expenses_time_period(df, diag=False):
        while True:
            print('Введите начало периода в формате год-месяц-день')
            start = input()
            if DATE_REGEX_RANGE.match(start):
                print('Введите конец периода в формате год-месяц-день')
                end = input()
                if DATE_REGEX_RANGE.match(end):
                    break
                else:
                    print('Неверный формат даты, повторите ввод!')
            else:
                print('Неверный формат даты, повторите ввод!')
        if diag:
            df2 = df[(df[DATE] >= start) & (df[DATE] <= end)].sort_values(by=[DATE, CATEGORY])
            labels = df2[CATEGORY].unique()
            df2 = df2.groupby(CATEGORY)[AMOUNT].agg('sum').tolist()
            sizes = [i for i in df2]
            print(sizes)
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
            ax1.axis('equal')
            plt.show()
        else:
            print(df[(df[DATE] >= start) & (df[DATE] <= end)].sort_values(by=[DATE, CATEGORY]))

    def show_diagram(self, df):
        print('Выберите:')
        print("1. Показать диаграмму расходов за всё время")
        print("2. Показать диаграмму расходов за период времени")
        action = int(input())
        if action == 1:
            labels = df[CATEGORY].unique()
            df2 = df.groupby(CATEGORY)[AMOUNT].agg('sum').tolist()
            sizes = [i for i in df2]
            print(sizes)
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
            ax1.axis('equal')
            plt.show()
        if action == 2:
            self.expenses_time_period(df, diag=True)

    def view_expenses_general(self, df):
        print('Введите цифру в зависимости от того, какие расходы вы хотите увидеть:')
        print('1. Посмотреть расходы за всё время')
        print('2. Посмотреть расходы по категории')
        print('3. Посмотреть расходы за период времени')
        action = int(input())
        if action == 1:
            self.expenses_all_time(df)
        if action == 2:
            self.expenses_categories(df)
        if action == 3:
            self.expenses_time_period(df)

    def run(self):
        while True:
            df = pd.read_csv(self.file_name, header=None, names=[CATEGORY, DATE, AMOUNT])
            df['Date'] = df['Date'].astype('datetime64[ns]')
            print('Введите цифру в зависимости от того, что хотите сделать:')
            print('1. Добавить расход')
            print('2. Посмотреть расходы')
            print('3. Посмотреть расходы в виде диаграммы')
            print('4. Выйти')
            action = int(input())
            if action == 1:
                self.write_to_file()
            if action == 2:
                self.view_expenses_general(df)
            if action == 3:
                self.show_diagram(df)
            if action == 4:
                break


a = BudgetCalculator('data.csv')
a.run()
