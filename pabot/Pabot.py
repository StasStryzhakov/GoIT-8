from pabot.AdressBook import AdressBook, Record
from pabot.Sort import sort_files
from pabot.Notes import Notes
from pabot.Message import (AddContactMessage,
                     AddContactBirthdayMessage,
                     ChangeContacPhonetMessage,
                     DaysToBirthdayMessage,
                     DeleteContactMessage,
                     DeletePhoneMessage,
                     GreetingMessage,
                     HelpMessage,
                     StopMessage,
                     ValueErrorMessage,
                     BirthdaysAfterDaysMessage,
                     AddContactEmaiMessage)
import re

# книга контактів і нотатки
CONTACTS = AdressBook()
NOTES = Notes()


# вивід інструкції
def get_help():
    return HelpMessage.get_message()


# обробляє помилки
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except KeyError:
            return 'This contact doesnt exist, please try again.'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contac cannot be added, it exists already'
        except TypeError:
            return 'Unknown command or parametrs, please try again.'

    return inner


# привітальне повідомлення
def greeting():
    return GreetingMessage.get_message()


# прощальне повідомлення
def stop_bot():
    return StopMessage.get_message()


# додати контакт, спочатку формуєся сам контакт, а потім додається у книгу
def add_contact(data):

    name, phones = get_data_from_user(data)

    if name in [i.lower() for i in CONTACTS]:
        raise ValueError('This contact already exist.')

    record = Record(name.capitalize())

    for phone in phones:
        record.add_phone(phone)

    CONTACTS.add_record(record)

    return AddContactMessage.get_message(name.capitalize())


# змінити номер(и) контакту
def change_contact(data):

    name, phones = get_data_from_user(data)
    record = CONTACTS[name.capitalize()]
    record.change_phone(phones)

    return ChangeContacPhonetMessage.get_message(name.capitalize())


# пошук контакту
def show_contact_phone(data: str):
    return CONTACTS.search(data.strip().lower()).get_info()


# вивід інформації по всім контактам
def show_all_contacts(*data):
    result = [record.get_info() for page in CONTACTS.iterator() for record in page]
    return '\n'.join(result)


# видалити телефон
def del_phone(data):
    name, phone = data.strip().split(' ')
    name = name.capitalize()
    record = CONTACTS[name]
    return DeletePhoneMessage.get_message(record.delete_phone(phone), name, phone)


# видалити контакт
def del_contact(data):
    name = data.strip().capitalize()
    CONTACTS.remove_record(name)
    return DeleteContactMessage.get_message(name)


# додати email
def add_email(data, flag=True):
    name, email = data.strip().split(' ')
    name = name.capitalize()
    record = CONTACTS[name]
    
    if record.email and flag:
        raise ValueError('This contact already have email.')
    
    record.add_contact_email(email)
    
    return AddContactEmaiMessage.get_message(name, email)


def change_email(data):
    return add_email(data, False)
    

# додати дату народження
def add_birth(data):
    name, birthday = data.strip().split(' ')
    name = name.capitalize()
    record = CONTACTS[name]
    record.add_birthday(birthday)
    return AddContactBirthdayMessage.get_message(name, birthday)


# виводить кількість днів до дня народження контакту
def days_to_birthday(data: str):
    record = CONTACTS[data.strip().capitalize()]
    name = record.name.value
    return DaysToBirthdayMessage.get_message(name, record.day_to_bithday())


# виводить дні народження за задану кількість днів
def birthdays_after_days(data):
    try:
        result = []
        days = int(data.strip())
        for name, record in CONTACTS.items():
            if record.birthday and int(record.day_to_bithday()) <= days:
                result.append(f'{name} - {record.birthday.value}')
        return BirthdaysAfterDaysMessage.get_message(result)
    except ValueError:
        return ValueErrorMessage
        

# Додати описання нотатку
def add_note_description(data: str):
    data = data.strip().split(' ')
    name = data.pop(0).lower()
    data = ' '.join(data)
    if not data:
        return "A valid description must contain something.\n"
    if name in [i.lower() for i in NOTES.data.keys()]:
        return NOTES.data[name.capitalize()].add_description(data)
    else:
        raise KeyError


# Видалити описання нотатку
def del_note_description(data: str):
    data = data.strip().split(' ')
    name = data.pop(0).lower()
    if name in [i.lower() for i in NOTES.data.keys()]:
        return NOTES.data[name.capitalize()].del_description()
    else:
        raise KeyError


# Замінити описання нотатку на інше
def change_note_description(data: str):
    data = data.strip().split(' ')
    name = data.pop(0).lower()
    data = ' '.join(data)
    if not data:
        return "A valid description must contain something.\n"
    if name in [i.lower() for i in NOTES.data.keys()]:
        return NOTES.data[name.capitalize()].change_description(data)
    else:
        return NOTES.data[name.capitalize()].change_description(None)


# Додати тег до нотатку
def add_note_tag(data: str):
    data = data.strip().split(' ')
    name = data.pop(0).lower()
    if name in [i.lower() for i in NOTES.data.keys()]:
        return NOTES.data[name.capitalize()].add_tag(' '.join(data))
    else:
        return NOTES.data[name.capitalize()].add_tag(None)


# Видалити тег нотатка за назвою
def del_note_tag(data: str):
    data = data.strip().split(' ')
    name = data.pop(0).lower()
    if name in [i.lower() for i in NOTES.data.keys()]:
        return NOTES.data[name.capitalize()].del_tag(' '.join(data))
    else:
        return NOTES.data[name.capitalize()].del_tag(None)


# список команд боту
COMMANDS = {'hello': greeting,
            'help': get_help,
            'add contact': add_contact,
            'change phone': change_contact,
            'search phone': show_contact_phone,
            'show all': show_all_contacts,
            'good bye': stop_bot,
            'close': stop_bot,
            'exit': stop_bot,
            'delete phone': del_phone,
            'delete contact': del_contact,
            'add birthday': add_birth,
            'days to birthday': days_to_birthday,
            'birthdays after days': birthdays_after_days,
            'create note': NOTES.add_note,
            'remove note': NOTES.delete_note,
            'describe note': add_note_description,
            'remove description': del_note_description,
            'alter description': change_note_description,
            'tag': add_note_tag,
            'untag': del_note_tag,
            'search notes': NOTES.finder,
            'show notes': NOTES.show_notes,
            'add email': add_email,
            'change email': change_email,
            'sort by tag': NOTES.notes_sort,
            'sort directory': sort_files}


# стоп функція
def break_func():
    return 'Wrong enter'


# обробка данних введених користувачем
def get_data_from_user(data: str):
    name, *phones = data.lower().strip().split(' ')

    return name, phones


# вибір команди, якщо такої нема, то буде виконана стоп функція
def get_command(command):
    return COMMANDS.get(command, break_func)


# обробка запиту користувача
@input_error
def get_user_request(user_input: str):
    command = ''
    data = ''

    for key in COMMANDS:
        # if bool(re.search(fr'{key}\b', user_input, flags=re.IGNORECASE)):
        #     command = key
        #     data = user_input.strip().lower()[len(key):]
        #     break
        if user_input.strip().lower().startswith(key):
            command = key
            data = user_input.strip().lower()[len(key):]
            break
    
    if not command:
        result = gess_what(user_input)
        command = result[0]
        data = result[1] 
   
    if data:
        return get_command(command)(data)
    return get_command(command)()


def gess_what(user_input):
    """"
    Функція намагається підібрати бажану опцію, якщо є опечатка при введені команди.
    Словник dict_result - своєрідна турнірна таблиця, де ключі - можливі команди 
    боту, а значення словника - бали.
    Бот запропонує користувачу команду, що набере найбільше балів в ході аналізу.
    """
    dict_result = {
            'hello': 0,
            'help': 0,
            'search phone': 0, 
            'show all': 0,
            'good bye': 0,
            'close': 0,
            'exit': 0,
            'delete contact': 0, 
            'days to birthday': 0, 
            'birthdays after days': 0,
            'create note': 0,
            'remove note': 0,
            'describe note': 0,
            'remove description': 0,
            'alter description': 0,
            'tag': 0,
            'untag': 0,
            'search notes': 0,
            'show notes': 0,
            'sort directory': 0,
            'sort by tag': 0,
            'add email': 0, 
            'change email': 0, 
            'add contact': 0, 
            'change phone': 0, 
            'delete phone': 0, 
            'add birthday': 0, 
            } 

    # для конвертації символів
    conv = {
            'й': 'q',
            'ц': 'w',
            'у': 'e',
            'к': 'r',
            'е': 't',
            'н': 'y',
            'г': 'u',
            'ш': 'i',
            'щ': 'o',
            'з': 'p',
            'ф': 'a',
            'ы': 's',
            'і': 's',
            'в': 'd',
            'а': 'f',
            'п': 'g',
            'р': 'h',
            'о': 'j',
            'л': 'k',
            'д': 'l',
            'я': 'z',
            'ч': 'x',
            'с': 'c',
            'м': 'v',
            'и': 'b',
            'т': 'n',
            'ь': 'm'
            }

    text = user_input.strip().lower()
    # переведення введеного тексту на латиницю
    if bool(re.search(r"[а-я]*", text)):
        for letter in text:
            text = text.replace(letter,conv.get(letter, letter))
   
    text_words = text.split(" ") # список слів введених користувачем

    # порівняння слів у введеному тексті та слів існуючої команди i присвоєння балів 
    n = 0
    while n < 2:
        
        for command in dict_result.keys():
            command_words = command.split(" ") 
            data_compare = list(zip(text_words, command_words)) 
            try:
                item = data_compare[n]
            except:
                continue
            # порівняння слів за довжиною
            if len(item[0]) < len(item[1]): 
                diff = len(item[0]) - len(item[1])
            else:
                diff = len(item[1]) - len(item[0])
            dict_result[command] += diff  
            # порівняння слів за складом букв
            word = item[1] 
            for char in item[0]: 
                if char in word:
                    word = word.replace(char, "") # для врахування букв, що повторюються
                    dict_result[command] += 2     
        n += 1

        # визначення найбільш вірогідної команди
        for key, value in dict_result.items(): 
            if value == max(dict_result.values()):
                command_result = key       

    answer = input(f'Did you mean "{command_result}" command to execute?(Y/N):')
    
    if answer == "Y" or answer == "y":
        data_result = " ".join(text_words[len(command_result.split(" ")):])
        result = (command_result, data_result)
        return result


# головна функція
def main():
    try:
        
        print(get_help())
        while True:
            
            user_request = input('Wait for your command master: ')
            result = get_user_request(user_request)
            print(result)
            
            if result == 'Good bye!':
                break
    finally:
        CONTACTS.save_to_file()
        NOTES.save_to_file()
    

if __name__ == '__main__':
    main()
