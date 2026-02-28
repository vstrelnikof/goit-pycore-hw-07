from address_book import AddressBook
from cli_bot import add_contact, change_contact, parse_input, show_all, show_phone

book = AddressBook()
print("Welcome to the assistant bot!")

commands = {
    "hello": lambda args: "How can I help you?",
    "add": lambda args: add_contact(args, contacts),
    "change": lambda args: change_contact(args, contacts),
    "phone": lambda args: show_phone(args, contacts),
    "all": lambda args: show_all(contacts),
    "exit": lambda args: "Good bye!",
    "close": lambda args: "Good bye!",
}

while True:
    user_input = input("Enter a command: ")
    command, *args = parse_input(user_input)
    handler = commands.get(command)
    if not handler:
        print("Invalid command.")
        continue
    result = handler(args)
    print(result)
    if command in ("exit", "close"):
        break