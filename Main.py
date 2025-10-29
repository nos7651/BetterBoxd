from queries import create_user

def main_menu():
    while True:
        print("\n===== Movie Database =====")
        print("1. Create new user")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")
            email = input("Enter your email: ")
            create_user(username, password, email, first_name, last_name)
        elif choice == "2":
            print("Vamoose!")
            break
        else:
            print("Invalid Option gangy")

if __name__ == "__main__":
    main_menu()