from User import create_user, login
from Movies import *
from queries import create_user, login
from playlist import create_playlist, view_playlists, add_movie_to_playlist, remove_movie_from_playlist, rename_playlist

def main_menu():
    current_user = None

    while True:
        if current_user:
            print(f"\nLogged in as: {current_user}")
            print("1. Search for movies")
            print("2. Log out")
            print("3. Create playlist")
            print("4. View playlist")
            print("5. Add movie to playlist")
            print("6. Remove movie from playlist")
            print("7. Change playlist name")
            print("8. Exit")
        else:
            print("1. Search for movies")
            print("2. Login")
            print("3. Create account")
            print("4. Exit")

        choice = input("Enter your choice: ").strip()


        if current_user:
            if choice == "1":
                while True:
                    print("\n=== Movie Search ===")
                    print("1. Search by title")
                    print("2. Search by cast")
                    print("3. Search by studio")
                    print("4. Search by genre")
                    print("5. Search by release year")
                    print("6. Back")

                    choice = input("Choose: ").strip()

                    if choice == "1":
                        term = input("Enter title: ").strip()
                        search_movie_title(term)

                    elif choice == "2":
                        term = input("Enter cast/crew name: ").strip()
                        search_movie_cast(term)

                    elif choice == "3":
                        term = input("Enter studio name: ").strip()
                        search_movie_studio(term)
                    elif choice == "4":
                        term = input("Enter genre: ").strip()
                        search_movie_genre(term)

                    elif choice == "5":
                        year = input("Enter release year (e.g., 2019): ").strip()
                        search_movie_release(year)


                    elif choice == "6":
                        return
                    else:
                        print("Invalid option.")

            elif choice == "2":
                print(f"Logged out {current_user}.")
                current_user = None

            elif choice == "3":
                playlist_name = input("Enter playlist name: ")
                create_playlist(current_user, playlist_name)

            elif choice == "4":
                view_playlists(current_user)

            elif choice == "5":
                playlist_id = input("Enter the playlist ID: ").strip()
                movie_id = input("Enter the movie ID: ").strip()
                add_movie_to_playlist(current_user, playlist_id, movie_id)

            elif choice == "6":
                playlist_id = input("Enter the playlist ID: ").strip()
                movie_id = input("Enter the movie ID to remove: ").strip()
                remove_movie_from_playlist(playlist_id, movie_id)

            elif choice == "7":
                playlist_id = input("Enter the playlist ID to rename: ").strip()
                new_name = input("Enter the new name: ").strip()
                rename_playlist(playlist_id, new_name)

            elif choice == "8":
                print("Goodbye!")
                break

            else:
                print("Invalid option.")

        else:
            if choice == "1":
                while True:
                    print("\n=== Movie Search ===")
                    print("1. Search by title")
                    print("2. Search by cast")
                    print("3. Search by studio")
                    print("4. Search by genre")
                    print("5. Search by release year")
                    print("6. Back")

                    choice = input("Choose: ").strip()

                    if choice == "1":
                        term = input("Enter title: ").strip()
                        search_movie_title(term)

                    elif choice == "2":
                        term = input("Enter cast/crew name: ").strip()
                        search_movie_cast(term)

                    elif choice == "3":
                        term = input("Enter studio name: ").strip()
                        search_movie_studio(term)
                    elif choice == "4":
                        term = input("Enter genre: ").strip()
                        search_movie_genre(term)

                    elif choice == "5":
                        year = input("Enter release year (e.g., 2019): ").strip()
                        search_movie_release(year)


                    elif choice == "6":
                        break
                    else:
                        print("Invalid option.")


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
