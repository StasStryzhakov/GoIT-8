from AdressBook import AdressBook, Record
from sort import sort_files
from notes import Notes, Note
from Message import (AddContactMessage,
                     AddContactBirthdayMessage,
                     ChangeContacPhonetMessage,
                     DaysToBirthdayMessage,
                     DeleteContactMessage,
                     DeletePhoneMessage,
                     GreetingMessage,
                     HelpMessage,
                     StopMessage)

# книга контактів
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

    if name in CONTACTS:
        raise ValueError('This contact already exist.')

    record = Record(name)

    for phone in phones:
        record.add_phone(phone)

    CONTACTS.add_record(record)

    return AddContactMessage.get_message(name)

# змінити номер(и) контакту
def change_contact(data):

    name, phones = get_data_from_user(data)
    record = CONTACTS[name]
    record.change_phone(phones)

    return ChangeContacPhonetMessage.get_message(name)

# пошук контакту
def show_contact_phone(data: str):
    return CONTACTS.search(data.strip()).get_info()

# вивід інформації по всім контактам
def show_all_contacts():

    result = [record.get_info() for page in CONTACTS.iterator() for record in page]
    return '\n'.join(result)

# видалити телефон
def del_phone(data):

    name, phone = data.strip().split(' ')
    record = CONTACTS[name]
    return DeletePhoneMessage.get_message(record.delete_phone(phone), name, phone)

# видалити контакт
def del_contact(data):

    name = data.strip()
    CONTACTS.remove_record(name)
    return DeleteContactMessage.get_message(name)

# додати дату народження
def add_birth(data):

    name, birthday = data.strip().split(' ')
    record = CONTACTS[name]
    record.add_birthday(birthday)
    return AddContactBirthdayMessage.get_message(name, birthday)

# виводить кількість днів до дня народження контакту
def days_to_birthday(data: str):

    record = CONTACTS[data.strip()]
    name = record.name.value
    return  DaysToBirthdayMessage.get_message(name, record.day_to_bithday())


def add_note_description(data: str):
    data = data.strip().split(' ')
    name = data.pop(0).lower()
    if name in [i.lower() for i in NOTES.data.keys()]:
        return NOTES.data[name.capitalize()].add_description(' '.join(data))


def del_note_description(data: str):
    data = data.strip().split(' ')
    name = data.pop(0).lower()
    if name in [i.lower() for i in NOTES.data.keys()]:
        return NOTES.data[name.capitalize()].del_description()


def change_note_description(data: str):
    data = data.strip().split(' ')
    name = data.pop(0).lower()
    if name in [i.lower() for i in NOTES.data.keys()]:
        return NOTES.data[name.capitalize()].change_description(' '.join(data))


def add_note_tag(data: str):
    data = data.strip().split(' ')
    name = data.pop(0).lower()
    if name in [i.lower() for i in NOTES.data.keys()]:
        return NOTES.data[name.capitalize()].add_tag(' '.join(data))


def del_note_tag(data: str):
    data = data.strip().split(' ')
    name = data.pop(0).lower()
    if name in [i.lower() for i in NOTES.data.keys()]:
        return NOTES.data[name.capitalize()].del_tag(' '.join(data))


# список команд боту
COMMANDS = {'hello': greeting,
            'help': get_help,
            'add': add_contact,
            'change': change_contact,
            'phone': show_contact_phone,
            'show all': show_all_contacts,
            'good bye': stop_bot,
            'close': stop_bot,
            'exit': stop_bot,
            'delete phone': del_phone,
            'delete': del_contact,
            'birthday': add_birth,
            'days to birthday': days_to_birthday,
            'create note': NOTES.add_note,
            'remove note': NOTES.delete_note,
            'describe note': add_note_description,
            'delete description': del_note_description,
            'alter description': change_note_description,
            'tag': add_note_tag,
            'untag': del_note_tag,
            'search notes': NOTES.finder,
            'notes': NOTES.show_notes,
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
        if user_input.strip().lower().startswith(key):
            command = key
            data = user_input[len(key):]
            break

    if data:
        return get_command(command)(data)
    return get_command(command)()





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