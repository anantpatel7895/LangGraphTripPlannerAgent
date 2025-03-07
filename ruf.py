print("\033[31mThis is red text\033[0m")

print("\033[32mThis is green text\033[0m")

from rich import print

print("[bold red]This is bold red text[/bold red]")
print("[green]This is green text[/green]")
print("[blue on yellow]Blue text on yellow background[/blue on yellow]")
# data = {
#     "name": "Alice",
#     "age": 25,
#     "hobbies": ["Reading", "Cycling", "Gaming"],
#     "location": {"city": "New York", "country": "USA"}
# }

# from rich import print
# import json


# def print_beatifully(messages):
#     print("[32mToolNode Result")  # ✅ Standard print
#     print(json.dumps(messages, indent=4))  # ✅ Rich print for beautification

# # Example usage
# data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
# print_beatifully(data)