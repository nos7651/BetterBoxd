from queries import create_user, login
from playlist import create_playlist, view_playlists

def main_menu():
    current_user = None

    while True:
        if current_user:
            print(f"\nLogged in as: {current_user}")
            print("1. Search for movies")
            print("2. Log out")
            print("3. Create playlist")
            print("4. View playlist")
            print("5. Exit")
        else:
            print("1. Search for movies")
            print("2. Login")
            print("3. Create account")
            print("4. Exit")

        choice = input("Enter your choice: ").strip()


        if current_user:
            if choice == "1":
                print("Nothing yet")

            elif choice == "2":
                print(f"Logged out {current_user}.")
                current_user = None

            elif choice == "3":
                playlist_name = input("Enter playlist name: ")
                create_playlist(current_user, playlist_name)

            elif choice == "4":
                view_playlists(current_user)

            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid option.")

        else:
            if choice == "1":
                print("nothing yet")

            elif choice == "2":
                username = input("Username: ")
                password = input("Password: ")
                if login(username, password):
                    current_user = username

            elif choice == "3":
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                first_name = input("Enter your first name: ")
                last_name = input("Enter your last name: ")
                email = input("Enter your email: ")
                create_user(username, password, email, first_name, last_name)

            elif choice == "4":
                print("Goodbye!")
                break

            else:
                print("Invalid option.")

if __name__ == "__main__":
    main_menu()
