from collections import UserDict
import pickle


class Notes(UserDict):
    """
        Словник, значеннями якого виступають об'єкти класу Note.
    """
    def __init__(self):
        super().__init__()
        self.load_from_file()

    def add_note(self, name):  # Додати нотаток
        name = name.strip().capitalize()
        if " " in name or not name:
            return "The name of the note can not have whitespace characters.\n"
        if name not in self.data.keys():
            self.data[name] = Note(name)
            return "Created a new note.\n"
        return "This note already exists.\n"

    def delete_note(self, name):  # Видалити нотаток
        name = name.strip().capitalize()
        del self.data[name]
        return "Note has been deleted.\n"

    def show_notes(self, *args):  # Повертає репрезентацію всього словника для виведення на екран
        tmp = [val for val in self.data.values()]
        return "".join(list(map(lambda x: str(x), tmp)))

    def load_from_file(self):  # Завантаження з диска
        try:
            with open('Notes.bin', 'rb') as fr:
                self.data = pickle.load(fr)
        except FileNotFoundError:
            pass

    def save_to_file(self):  # Збереження на диск
        with open('Notes.bin', 'wb') as fw:
            pickle.dump(self.data, fw)

    def iterator(self, n=3):  # Не використаний (може і не буде використаний) ітератор
        output = []
        i = 0

        for elem in self.data.values():
            output.append(elem)
            i += 1
            if i == n:
                yield output
                output = []
                i = 0
        if output:
            yield output

    def notes_sort(self, data: str):  # Пошук та сортування за введеними символами
        phrase = data.strip().lower()

        def sort_help(tag):
            tag_output = []
            for i in tag[1]:
                if i.value == phrase:
                    tag_output.append('a')
                else:
                    tag_output.append(i.value[0])
            if tag_output:
                return sorted(tag_output)[0]
            return "y"
        if not phrase:
            return "Insufficient data to look for.\n"

        match = {}
        non_match = {}
        for note, info in self.data.items():
            if find_assist(phrase, [i.value for i in info.tags]):
                match[note] = info.tags
            else:
                non_match[note] = info.tags
        match = sorted(match.items(), key=sort_help)
        non_match = sorted(non_match.items(), key=lambda item: sorted(i.value for i in item[1]))
        output_str = "\nMatched results:\n"
        for elem in match:
            output_str += f"\n{elem[0]}\nTags: {[i.value for i in elem[1]]}\n"
        output_str += "\nUnmatched results:\n"
        for elem in non_match:
            output_str += f"\n{elem[0]}\nTags: {[i.value for i in elem[1]]}\n"
        return output_str

    def finder(self, data: str):  # Пошук за символами
        phrase = data.strip().lower()
        if not phrase:
            return "Insufficient data to look for.\n"
        output = {}
        for note, info in self.data.items():
            if note in output.keys():
                continue
            if phrase in note.lower():
                output[note] = info
            elif phrase in info.description.value.lower():
                output[note] = info
            elif find_assist(phrase, [i.value for i in info.tags]):
                output[note] = info

        if not output:
            return "No matches found.\n"
        output_str = "\nSearch results:\n"
        for key, val in output.items():
            output_str += f"\n{key}\nDescription: {val.description.value}\nTags: {[i.value for i in val.tags]}\n"
        return output_str


def find_assist(phrase, value_list) -> bool:  # Хелпер-функція для finder-методу (^^^)
    for elem in value_list:
        if phrase in elem.lower():
            return True
    return False


class Note:
    """
        Клас нотатків. Має обов'язковий атрибут ім'я і 2 необов'язкових - опис і теги.
    """
    def __init__(self, name, description='', tag=None):
        self.name = Name(name.strip().capitalize())
        self.description = Description(description)
        self.tags = [Tag(tag)] if tag else []

    def add_description(self, description):  # Додати опис
        if not self.description.value:
            self.description = Description(description)
            return "Description added.\n"
        else:
            return "This note already has a description.\n"

    def del_description(self, *args):  # Видалити опис
        if self.description.value:
            self.description = Description('')
            return "Deleted the description.\n"
        return "No description recorded.\n"

    def change_description(self, new_description):  # Змінити опис
        if self.description.value:
            self.description = Description(new_description)
            return "Description changed.\n"
        else:
            return "This note doesn't yet have a description.\n"

    def add_tag(self, tag):  # Додати тег
        if not tag:
            return "No tag was given.\n"
        elif tag not in list(map(lambda x: x.value, self.tags)):
            self.tags.append(Tag(tag))
            return f"Tag <{tag}> added to the note.\n"
        else:
            return "Such a tag already exists for this note.\n"

    def del_tag(self, tag):  # Видалити тег
        if not tag:
            return "No tag was given.\n"
        for i in self.tags:
            if tag == i.value:
                self.tags.remove(i)
                return f"Tag: <{tag}> removed from the note.\n"
        return "Such a tag doesn't exist and can not be removed.\n"

    def __repr__(self):  # Репрезентація класу для виклику str()
        return f"{self.name.value}:\nDescription: {self.description.value}\n" \
                f"Tags: {[i.value for i in self.tags]}\n\n"


class Field:  # Батьківський клас для всіх полів
    def __init__(self, value):
        self.value = value


class Name(Field):  # Обов'язкове поле з ім'ям
    pass


class Description(Field):  # Поле з описом
    def __init__(self, value):
        super().__init__(value)
        self.__value = ''
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Tag(Field):  # Поле з тегом
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value
