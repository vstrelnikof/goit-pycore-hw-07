from address_book import AddressBook

def input_error(func):
    """Декоратор для обробки помилок введення користувача."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return f"Contact not found: {e}"
        except ValueError as e:
            return f"Invalid input: {e}"
        except IndexError as e:
            return f"Missing argument: {e}"
        except TypeError as e:
            return f"Type error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"
    return inner

def parse_input(user_input: str) -> tuple[str, list[str]]:
    """Розбирає введений рядок на команду та аргументи"""
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args

@input_error
def add_contact(args, contacts: dict) -> str:
    """Додає новий контакт"""
    if len(args) != 2:
        raise ValueError("You must provide exactly 2 arguments: name and phone.")
    name, phone = args
    contacts[name] = phone
    return f"Contact '{name}' added."

@input_error
def change_contact(args, contacts: dict) -> str:
    """Змінює номер телефону існуючого контакту"""
    if len(args) != 2:
        raise ValueError("You must provide exactly 2 arguments: name and new phone.")
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return f"Contact '{name}' updated."
    else:
        raise KeyError(name)

@input_error
def show_phone(args, contacts: dict) -> str:
    """Показує номер телефону за ім'ям."""
    if len(args) != 1:
        raise IndexError("You must provide exactly 1 argument: name.")
    name = args[0]
    if name in contacts:
        return f"{name}: {contacts[name]}"
    else:
        raise KeyError(name)

@input_error
def show_all(contacts: dict) -> str:
    """Виводить усі контакти"""
    if not contacts:
        return "No contacts saved."
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

@input_error
def add_birthday(args, book: AddressBook):
    name, date = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.add_birthday(date)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    name, = args
    record = book.find(name)
    if not record or not record.birthday:
        return "Birthday not found."
    return f"{name}: {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next week."
    result = []
    for day, names in upcoming.items():
        result.append(f"{day}: {', '.join(names)}")
    return "\n".join(result)
