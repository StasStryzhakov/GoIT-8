# GoIT-8


# Установка 

Виконайте послідовно в терміналі:


1. cd pabot
2. python setup.py install

#### АБО

1. git clone https://github.com/StasStryzhakov/GoIT-8.git
2. cd GoIT-8
3. python setup.py install


# Використання

## Запуск

**_Програма запускається командою: `pabot`_**

## Команди

Після запуску вам будуть доступні команди:

> `hello` - greetings
 
> `help` - show commands list

### Робота з контактами

#### Ім`я та телефон

> `add contact` - add new contact in storage 
>>Example: `add contact` "name (only letters without spaces)" "phone number (only digits without spaces)"

> `change` - change existing contact 
>>Example: `change` "exist contact name (only letters without spaces)" "new phone number (only digits without spaces)"

#### Дата народження

> `birthday` - add birthday date to the contact 
>>Example: `birthday` "name" "date"(yyyy-mm-dd) ~~(dd-mm-yyyy)~~ ~~(mm-dd-yyyy)~~

> `days to birthday` - show how much days left to the contact birthday 
>>Example: `days to birthday` name

#### Email

> `add email` - add email to the contact
>> Example: `add email` "name" "email"

> `change email` - change contact`s email
>> Example: `change email` "name" "new_email"

#### Видалення даних

> `delete` - remove contact
>>Example: `delete` "name (only letters without spaces)"

> `delete phone` - remove entered phone from contact 
>>Example: `delete phone` "name (only letters without spaces)" "phone number (only digits without spaces)"

### Функції пошуку

>`phone` - shows all users with given phone for search
>> Example: phone 0951234567

> `show all` - show all existing contacts

> `notes` - shows all recorded notes

>`birthdays after days` - shows all users whose birthday is in a given number of days
>>Example: `birthdays after days` "number of days"

> `search notes` - searches all notes for a match, prints out all matching notes
### Робота з нотатками 

> `create note` - creates a new note 
>>Example: `create note` "name (only letters without spaces)"

> `remove note` - deletes a note by name 
>>Example: `remove note` "name"

> `describe note` - adds description to a note 
>>Example: `describe note` "name" "description"

> `alter description` - changes the description of a note, if it exists

> `delete description` - deletes the description of a note

### Робота з тегами

> `tag` - add a tag to the note 
>>Example: `tag` "name" "tag"

> `untag` - deletes a tag from a note, if it exists 
>>Example: `untag` "name" "tag"

> `sort by tag` - performs an alphabetical sorting of notes, based on matches in their tags
>> Example: `sort by tag` "phrase"
### Сортування директорій

> `sort directory` - just what it says 
>>Example: `sort directory` D:\\stuff\\python_projects\n

### Завершення роботи

>`good bye`/`close`/`exit` - bye bye

