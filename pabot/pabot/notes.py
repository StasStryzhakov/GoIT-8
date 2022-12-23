from collections import UserDict
import pickle


class Notes(UserDict):
    """
    Об'єкт, що ітерує за атрибутами іншого об'єкта та створює з них словник.
    """
    def __init__(self):
        super().__init__()
        self.load_from_file()

    def add_note(self, name):
        name = name.strip().lower().capitalize()
        self.data[name] = Note(name)
        return "Created a new note.\n"

    def delete_note(self, name):
        name = name.strip().lower().capitalize()
        del self.data[name]
        return "Note has been deleted.\n"

    def show_notes(self):
        tmp = [val for val in self.data.values()]
        return "".join(list(map(lambda x: str(x), tmp)))

    def load_from_file(self):
        try:
            with open('Notes.bin', 'rb') as fr:
                self.data = pickle.load(fr)
        except FileNotFoundError:
            pass

    def save_to_file(self):
        with open('Notes.bin', 'wb') as fw:
            pickle.dump(self.data, fw)

    def iterator(self, n=3):
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

    def finder(self, data: str):  # Пошук за символами
        phrase = data.strip().lower()
        if not phrase:
            return "Insufficient data to look for."
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
            return "No matches found."
        output_str = ""
        for key, val in output.items():
            output_str += f"\n{key}\nDescription: {val.description.value}\nTags: {[i.value for i in val.tags]}\n"
        return output_str


def find_assist(phrase, value_list) -> bool:
    for elem in value_list:
        if phrase in elem.lower():
            return True
    return False


class Note:
    """
    Description
    """
    def __init__(self, name, description=None, tag=None):
        self.name = Name(name.strip().capitalize())
        self.description = Description(description)
        self.tags = [Tag(tag)] if tag else []

    def add_description(self, description):
        if not self.description.value:
            self.description = Description(description)
            return "Description added.\n"
        else:
            return "This note already has a description.\n"

    def del_description(self):
        if self.description.value:
            self.description = Description(None)
            return "Deleted the description.\n"

    def change_description(self, new_description):
        if self.description.value:
            self.description = Description(new_description)
            return "Description changed.\n"
        else:
            return "This note doesn't yet have a description.\n"

    def add_tag(self, tag):
        if not tag:
            return "No tag was given.\n"
        elif tag not in list(map(lambda x: x.value, self.tags)):
            self.tags.append(Tag(tag))
            return f"Tag <{tag}> added to the note.\n"
        else:
            return "Such a tag already exists for this note.\n"

    def del_tag(self, tag):
        if not tag:
            return "No tag was given.\n"
        for i in self.tags:
            if tag == i.value:
                self.tags.remove(i)
                return f"Tag: <{tag}> removed from the note.\n"
        return "Such a tag doesn't exist and can not be removed.\n"

    def __repr__(self):
        return f"{self.name.value}:\nDescription: {self.description.value}\n" \
                f"Tags: {[i.value for i in self.tags]}\n\n"


class Field:  # Батьківський клас для всіх полів
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Description(Field):
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


class Tag(Field):
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
