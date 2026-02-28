from collections import UserDict
from datetime import datetime
from record import Record

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError, TypeError) as e:
            return f"Error: {e}"
    return inner

class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> (Record | None):
        return self.data.get(name)

    @input_error
    def add_contact(self, name: str, phone: str) -> str:
        record: Record | None = self.find(name)
        if not record:
            record = Record(name)
            self.add_record(record)
            message = "Contact added."
        else:
            message = "Contact updated."
        record.add_phone(phone)
        return message

    @input_error
    def change_contact(self, name: str, old_phone: str, new_phone: str) -> str:
        record: Record | None = self.find(name)
        if not record:
            raise KeyError(f"No contacts found: {name}")
        if record.edit_phone(old_phone, new_phone):
            return "Phone updated."
        else:
            return "Old phone not found."

    @input_error
    def show_phone(self, name: str) -> str:
        record: Record | None = self.find(name)
        if not record or not record.phones:
            return "Phones not found."
        return f"{name}: {', '.join(p.value for p in record.phones)}"

    @input_error
    def show_all(self) -> str:
        if not self.data:
            return "No contacts saved."
        return "\n".join(str(record) for record in self.data.values())

    @input_error
    def add_birthday(self, name: str, date: str) -> str:
        record: Record | None = self.find(name)
        if not record:
            raise KeyError(f"No contacts found: {name}")
        record.add_birthday(date)
        return "Birthday added."

    @input_error
    def show_birthday(self, name: str) -> str:
        record: Record | None = self.find(name)
        if not record or not record.birthday:
            return "Birthday not found."
        return f"{name}: {record.birthday.value.strftime('%d.%m.%Y')}"

    @input_error
    def show_upcoming_birthdays(self) -> str:
        today = datetime.today().date()
        upcoming = {}
        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value
                bday_this_year = bday.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                delta = (bday_this_year - today).days
                if 0 <= delta < 7:
                    day = bday_this_year.strftime("%A")
                    upcoming.setdefault(day, []).append(record.name.value)
        if not upcoming:
            return "No birthdays in the next week."
        return "\n".join(f"{day}: {', '.join(names)}" for day, names in upcoming.items())
