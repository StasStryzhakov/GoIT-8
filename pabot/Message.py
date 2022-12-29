from abc import abstractmethod, ABC

# у цьомі классі зібрані усі меседжі які будуть виводитися користувачу при роботі з командами

class Message(ABC):
    
    @abstractmethod
    def get_message():
        pass
    
    
    

class HelpMessage(Message):
    
    @staticmethod
    def get_message():
        return '''Command to execute: 
>>> hello
>>> help - show commands list
>>> add contact - add new contact in storage Example: add contact "name (only letters without spaces)" "phone number (only digits without spaces)"
>>> add email - add email to the contact Example: add email "name" "email"
>>> add birthday - add birthday date to the contact Example: birthday name date(yyyy-mm-dd)
>>> change phone - change existing contact Example: change "exist contact name (only letters without spaces)" "new phone number (only digits without spaces)"
>>> change email - change contact`s email Example: change email "name" "new_email"
>>> phone - shows all users with given phone for search. Example: phone +380951234567
>>> days to birthday - show how much days left to the contact birthday Example: days to birthday name
>>> show all - show all existing contacts
>>> delete phone - remove entered phone from contact Example: delete phone "name (only letters without spaces)" "phone number (only digits without spaces)"
>>> delete contact - remove contact Example: delete "name (only letters without spaces)" 
>>> create note - creates a new note Example: create note "name (only letters without spaces)"
>>> remove note - deletes a note by name Example: remove note "name"
>>> describe note - adds description to a note Example: describe note "name" "description"
>>> remove description - deletes the description of a note 
>>> alter description - changes the description of a note, if it exists
>>> tag - add a tag to the note Example: tag "name" "tag"
>>> untag - deletes a tag from a note, if it exists Example: untag "name" "tag"
>>> search notes - searches all notes for a match, prints out all matching notes
>>> show notes - shows all recorded notes
>>> sort by tag - performs an alphabetical sorting of notes, based on matches in their tags
>>> sort directory - just what it says Example: sort directory D:\\stuff\\python_projects
>>> good bye/close/exit - bye bye\n
'''

class GreetingMessage(Message):
        
    @staticmethod
    def get_message():
        return 'How can I help you?'
    
class StopMessage(Message):
    
    @staticmethod
    def get_message():
        return 'Good bye!'
    
class AddContactMessage(Message):
    
    @staticmethod
    def get_message(name):
        return f'contact {name} was added'

class ChangeContacPhonetMessage(Message):
    
    @staticmethod
    def get_message(name):
        return f'contact {name} was updated'   
     
class DeletePhoneMessage(Message):
    
    @staticmethod
    def get_message(flag, name, phone):
        if flag:
            return f'Phone {phone} for {name} contact deleted.'
        return f'{name} contact does not have this number'
    
class DeleteContactMessage(Message):
    
    @staticmethod
    def get_message(name):
        return f'Contact {name} was deleted' 
    
class AddContactBirthdayMessage(Message):
    
    @staticmethod
    def get_message(name, birthday):
        return f'For {name} you add Birthday {birthday}' 
    
class AddContactEmaiMessage(Message):
    
    @staticmethod
    def get_message(name, email):
        return f'For {name} you add email {email}'    
    
class DaysToBirthdayMessage(Message):
    
    @staticmethod
    def get_message(name, days):
        return f'{days} left for the contact birthday {name}'


class BirthdaysAfterDaysMessage(Message):

    @staticmethod
    def get_message(result: list):
        if not result:
            print('No birthdays for this days')
        return '\n'.join(result)

class ValueErrorMessage(Message):

    @staticmethod
    def get_message():
        return print('The number of days must be a numeric value')
