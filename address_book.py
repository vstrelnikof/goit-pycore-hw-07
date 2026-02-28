from collections import UserDict
from datetime import datetime
from record import Record

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = {}
        for record in self.data.values():
            if record.birthday:
                bday_this_year = record.birthday.value.replace(year=today.year)
                delta = (bday_this_year - today).days
                if 0 <= delta < 7:
                    day = bday_this_year.strftime("%A")
                    upcoming.setdefault(day, []).append(record.name.value)
        return upcoming
