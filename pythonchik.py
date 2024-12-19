from datetime import datetime, date

def bold_text(text):
    return '\033[1m' + text + '\033[0m'

def italic_text(text):
    return '\033[3m' + text + '\033[0m'

def check_valid():

    while True:
        print ("Введите имя, фамилию, номер телефона, дату рождения контакта в формате \"Имя;Фамилия;Номер телефона;Дата рождения\"\nИмя и фамилия могут содержать только буквы латинского алфавита, пробелы, цифры, первая буква - заглавная; Номер телефона должен содержать 11 цифр без знака \"+\"; Если не хотите вводить дату рождения, то строку можно оставить пустой, но если вводите, то она должна быть полной в формате День-Месяц-Год\nПример: Ivan;Ivanov;89040658901;09-12-2000:")
        arr=input()
        c=arr.count(";")
        arr=arr.split(";")
        if len(arr[0])==0:
            print (bold_text("Имя не может быть пустым"))
            continue

        if arr[0][0].islower():
            arr[0]=arr[0].title()


        for i in range (len(arr[0])):
            if (not arr[0][i].isalnum() and not arr[0][i].isspace()):
                print (bold_text("Имя может содержать только буквы латинского алфавита, цифры или пробел"))
                break
        if i<len(arr[0])-1:
            continue
        try:
            if arr[1][0].islower():
                arr[1]=arr[1].title()
        except(IndexError):
            print (bold_text("Фамилия не может быть пустой"))
            continue

        for j in range (len(arr[1])):
            if (not arr[1][j].isalnum() and not arr[1][j].isspace()):
                print (bold_text("Фамилия может содержать только буквы латинского алфавита, цифры или пробел"))
                break
        if j<len(arr[1])-1:
            continue
        try:
            if arr[2][0]!="8" and (arr[2][0]!="+" and arr[2][1]!="7"):
                print (bold_text("Номер может начинаться только с \"8\" или с \"+7\""))
                continue
            elif (arr[2][0]=="8"):
                if (len(arr[2])!=11):
                    print (bold_text("Номер телефона должен содержать строго 11 цифр"))
                    continue
            elif (arr[2][0]=="+" and arr[2][1]=="7"):
                arr[2]=arr[2].replace("+7", "8")
                if (len(arr[2])!=11):
                    print (bold_text("Номер телефона должен содержать строго 11 цифр и один знак \"+\" в начале"))
                    continue
        except(IndexError):
            print (bold_text("Вы не ввели номер"))
            continue
        for k in range (len(arr[2])):
            if not arr[2][k].isdigit():
                print (bold_text("Номер телефона может содержать только цифры"))
                continue
        if c==3:
            try:
                datetime.strptime(arr[3], "%d-%m-%Y")
            except ValueError:
                print (bold_text("Дата введена некорректно"))
                continue
        break
    return arr

def age(tod_date):
    today=date.today()
    birth= datetime.strptime(tod_date, '%d-%m-%Y').date()
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    print (italic_text("Данному контакту "),end="")
    if age%10==0 or age%10>=5 or (age%100>=11 and age%100<=19):
        print (age, italic_text("лет"))
    elif age%10==1:
        print (age, italic_text("год"))
    else:
        print (age, italic_text("года"))
    return age

def finding_line(name, surname, file_path, flag):
    with open(file_path, "r") as file:
        c=0
        for line in file:
            if line!="\n":
                part=line.split(";")
                if part[0]==name and part[1]==surname:
                    if (flag=="just_finding"):
                        print (";".join(part), end="")
                    if (flag=="age"):
                        try:
                            age(part[3][:-1])
                        except (IndexError):
                            print(bold_text("У этого контакта нет даты рождения"))
                            return
                    return c
            c+=1
        return -1

def finding_on_name(name, file_path):

    with open(file_path, "r") as file:
        flag=0
        for line in file:
            if line!="\n":
                part=line.split(";")
                if part[0]==name:
                    print (";".join(part), end="")
                    flag=1
        if flag==0:
            return -1

def finding_on_surname(surname, file_path):
    with open(file_path, "r") as file:
        flag=0
        for line in file:
            if line!="\n":
                part=line.split(";")
                if part[1]==surname:
                    print (";".join(part), end="")
                    flag=1
        if (flag==0):
            return -1

def replace_contact(index, new_contact, file_path):
    with open(file_path, "r") as file:
        lines=file.readlines()
    lines[index] = new_contact
    with open(file_path, "w") as file:
        file.writelines(lines)
    print (italic_text("Контакт удачно перезаписан"))

def add_record(file_path):
    arr=check_valid()
    with open(file_path, "a") as file:
        id=finding_line(arr[0], arr[1], file_path, "add")
        line=";".join(arr) + "\n"
        if id==-1:
            file.write(line)
            print (italic_text("Контакт добавлен"))
        else:
            print(bold_text("Такой контакт уже существует. Выберите, что вы хотите сделать:\n1.Вернуться\n2.Заменить контакт"))
            m=int(input("Введите номер команды: "))
            if m==1:
                return
            else:
                replace_contact(id, line, file_path)

def print_records(file_path):
    print(italic_text("Весь список контактов:\n"))
    with open(file_path, "r") as file:
        for line in file:
            if line!="\n":
                print (line, end="")

def remove_line(file_path):
    name, surname=input("Введите имя и фамилию, разделяя по \";\" контакта, который нужно удалить: ").split(";")
    index=finding_line(name, surname, file_path, "remove")
    if index==-1:
        print (bold_text("Такого контакта не существует"))
        return
    with open(file_path, "r") as file:
        lines=file.readlines()
    del lines[index]
    with open (file_path, "w") as file:
        file.writelines(lines)
    print (italic_text("Контакт был успешно удалён"))

while True:
    try:
        print ("Пожалуйста, выберите команду, которую хотите выполнить и укажите её номер:\n1.Добавить новую запись\n2.Вывести список всех контактов\n3.Найти контакт(ы)\n4.Удалить контакт\n5.Изменить контакт\n6.Вывести возраст контакта\nЕсли хотите завершить выполнение программы напишите \"Выйти\"")
        n=input("Пожалуйста, введите номер команды: ")
        file_path="phone_directory.txt"
        if n=="Выйти":
            quit()
        n=int(n)
        if n<1 or n>6:
            print (bold_text("Номер команды может быть только целым числом от 1 до 6"))
            continue
        if n==1:
            add_record(file_path)
        elif n==2:
            print_records(file_path)
        elif n==3:
            m=int(input("Как вы хотите осуществить поиск?\n1.По имени\n2.По фамилии\n3.По имени и фамилии\nВведите номер команды: "))
            if m<1 or m>3:
                print(bold_text("Номер команды может быть только целым числом от 1 до 3"))
                continue
            if m==1:
                name=input("Введите имя: ")
                if finding_on_name(name.title(), file_path)==-1:
                    print (bold_text("Контакта с таким именем не существует"))
                
            elif m==2:
                surname=input("Введите фамилию: ")
                if finding_on_surname(surname.title(), file_path)==-1:
                    print(bold_text("Контакта с такой фамилией не существует"))
                
            else:
                name, surname=input("Введите имя и фамилию, разделяя их \";\": ").split(";")
                if finding_line(name.title(), surname.title(), file_path, "just_finding")==-1:
                    print (bold_text("Такого контакта не существует"))
        elif n==4:
            remove_line(file_path)
        elif n==5:
            name, surname=input("Введите имя и фамилию контакта, который вы хотите изменить, разделяя по \";\": ").split(";")
            id=finding_line(name.title(), surname.title(), file_path, "just_finding")
            if id==-1:
                print (bold_text("Такого контакта не существует"))
                continue
            new_contact=check_valid()
            replace_contact(id, ";".join(new_contact) + "\n", file_path)
        elif  n==6:
            name, surname=input("Введите имя и фамилию контакта, чей возраст вы хотите узнать, разделяя по \";\": ").split(";")
            id=finding_line(name.title(), surname.title(), file_path, "age")
    except (ValueError):
        print (bold_text("Вы неверно ввели команду"))
        continue
        
        
    
    

