from user import *
from movies import *
from playlist import *
from follow import *
from profile import get_user_profile


def main_menu():
    current_user = None
    print("--- Betterboxd ---")
    while True:
        if current_user:
            print(f"\nLogged in as: {current_user}")
            print("1. View profile")
            print("2. Search for movies")
            print("3. Playlists")
            print("4. Search for users (follow/unfollow)")
            print("5. Logout")
            print("6. Exit")
        else:
            print("1. Search for movies")
            print("2. Login")
            print("3. Create account")
            print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if current_user:
            if choice == "1":
                get_user_profile(current_user)

            elif choice == "2":
                while True:
                    print("\n--- Movie Search ---")
                    print("1. Search by title")
                    print("2. Search by cast")
                    print("3. Search by studio")
                    print("4. Search by genre")
                    print("5. Search by release year")
                    print("6. Back")
                    search_choice = input("Choose: ").strip()

                    if search_choice == "1":
                        term = input("Enter title: ").strip()
                        result = search_movie_title(term)
                    elif search_choice == "2":
                        term = input("Enter cast/crew name: ").strip()
                        result = search_movie_cast(term)
                    elif search_choice == "3":
                        term = input("Enter studio name: ").strip()
                        result = search_movie_studio(term)
                    elif search_choice == "4":
                        term = input("Enter genre: ").strip()
                        result = search_movie_genre(term)
                    elif search_choice == "5":
                        year = input("Enter release year (e.g., 2019): ").strip()
                        result = search_movie_release(year)
                    elif search_choice == "6":
                        break
                    else:
                        print("Invalid option.")
                        continue

                    if result:
                        while True:
                            print("\n--- Search Results ---")
                            print("1. Choose a movie")
                            print("2. Sort by Name (Ascending)")
                            print("3. Sort by Name (Descending)")
                            print("4. Sort by Studio (Ascending)")
                            print("5. Sort by Studio (Descending)")
                            print("6. Sort by Genre (Ascending)")
                            print("7. Sort by Genre (Descending)")
                            print("8. Sort by Year (Ascending)")
                            print("9. Sort by Year (Descending)")
                            print("10. Back")
                            inp = input("Enter choice: ").strip()

                            if inp == "1":
                                selected_movie_id = input("Input movie ID: ").strip()
                                if movie_exists(selected_movie_id):
                                    print(f"Current chosen movie id: {selected_movie_id}")
                                    print("1. Rate")
                                    print("2. Mark as Watched")
                                    print("3. Add movie to playlist")
                                    print("4. Go back")

                                    action = input("Choose: ").strip()
                                    if action == "1":
                                        rating = float(input("Enter rating 1 - 5 (intervals of .5): ").strip())
                                        if rating < 1 or rating > 5 or rating % .5 != 0:
                                            print("Invalid rating.")
                                            break
                                        rate_movie(current_user, selected_movie_id, rating)
                                        print(f"Rating entered: {rating} / 5")

                                    elif action == "2":
                                        mark_movie_as_watched(current_user, selected_movie_id)
                                        print("Movie marked as watched")
                                    elif action == "3":
                                        playlist_id = int(input("Enter playlist id: ").strip())
                                        add_movie_to_playlist(current_user, playlist_id, selected_movie_id)
                                        print(f"Added movie to playlist: {selected_movie_id}")
                                    elif action == "4":
                                        continue
                                    else:
                                        print("Invalid option.")
                                else:
                                    print("Movie with chosen ID doesn't exist.")

                            elif inp == "2":
                                sort_movies("title", True)
                            elif inp == "3":
                                sort_movies("title", False)
                            elif inp == "4":
                                sort_movies("studio", True)
                            elif inp == "5":
                                sort_movies("studio", False)
                            elif inp == "6":
                                sort_movies("genre", True)
                            elif inp == "7":
                                sort_movies("genre", False)
                            elif inp == "8":
                                sort_movies("year", True)
                            elif inp == "9":
                                sort_movies("year", False)
                            elif inp == "10":
                                break
                            else:
                                print("Invalid option.")

            elif choice == "3":

                while True:
                    print("\n--- Playlist Menu ---")
                    print("1. Create playlist")
                    print("2. View my playlists")
                    print("3. Add a movie to a playlist")
                    print("4. Remove movie from playlist")
                    print("5. Rename playlist")
                    print("6. Delete playlist")
                    print("7. Watch a playlist")
                    print("8. Back")
                    pl_choice = input("Enter your choice: ").strip()

                    if pl_choice == "1":
                        playlist_name = input("Enter playlist name: ").strip()
                        if not playlist_name:
                            print("Name cannot be empty.")
                            continue
                        create_playlist(current_user, playlist_name)

                    elif pl_choice == "2":
                        view_playlists(current_user)

                    elif pl_choice == "3":
                        playlist_id = input("Enter playlist ID: ").strip()
                        movie_id = input("Enter movie ID: ").strip()
                        if not playlist_id or not movie_id:
                            print("Both playlist ID and movie ID are required.")
                            continue
                        add_movie_to_playlist(current_user, playlist_id, movie_id)

                    elif pl_choice == "4":
                        playlist_id = input("Enter playlist ID: ").strip()
                        movie_id = input("Enter movie ID to remove: ").strip()
                        remove_movie_from_playlist(playlist_id, movie_id)

                    elif pl_choice == "5":
                        playlist_id = input("Enter playlist ID: ").strip()
                        new_name = input("Enter new name: ").strip()
                        rename_playlist(playlist_id, new_name)
                    elif pl_choice == "6":
                        playlist_id = input("Enter playlist ID: ").strip()
                        delete_playlist(playlist_id, current_user)

                    elif pl_choice == "7":
                        playlist_id = input("Enter playlist ID: ").strip()
                        watch_playlist(playlist_id)
                    elif pl_choice == "8":
                        break
                    else:
                        print("Invalid option.")

            elif choice == "4":

                while True:
                    print("\n--- User Search ---")
                    print("1. Search for user by email")
                    print("2. Back")
                    fu_choice = input("Enter choice: ").strip()

                    if fu_choice == "1":
                        email = input("Enter email of user: ").strip()
                        username = search_user(email)
                        if not username:
                            continue

                        if not is_following(current_user, username):
                            print(f"\nUser found: {username}")
                            print("1. Follow user")
                            print("2. Back")
                            act = input("Enter choice: ").strip()
                            if act == "1":
                                follow_user(current_user, username)
                        else:
                            print(f"\nUser found: {username}")
                            print("1. Unfollow user")
                            print("2. Back")
                            act = input("Enter choice: ").strip()
                            if act == "1":
                                unfollow_user(current_user, username)

                    elif fu_choice == "2":
                        break
                    else:
                        print("Invalid option.")

            elif choice == "5":
                print(f"Logged out {current_user}.")
                current_user = None

            elif choice == "6":
                print("Goodbye.")
                break

            else:
                print("Invalid option.")


        else:
            if choice == "1":
                while True:
                    print("\n--- Movie Search (Guest) ---")
                    print("1. Search by title")
                    print("2. Search by cast")
                    print("3. Search by studio")
                    print("4. Search by genre")
                    print("5. Search by release year")
                    print("6. Back")
                    search_choice = input("Choose: ").strip()

                    if search_choice == "1":
                        term = input("Enter title: ").strip()
                        result = search_movie_title(term)
                    elif search_choice == "2":
                        term = input("Enter cast/crew name: ").strip()
                        result = search_movie_cast(term)
                    elif search_choice == "3":
                        term = input("Enter studio name: ").strip()
                        result = search_movie_studio(term)
                    elif search_choice == "4":
                        term = input("Enter genre: ").strip()
                        result = search_movie_genre(term)
                    elif search_choice == "5":
                        year = input("Enter release year (e.g., 2019): ").strip()
                        result = search_movie_release(year)
                    elif search_choice == "6":
                        break
                    else:
                        print("Invalid option.")
                        continue

                    if result:
                        while True:
                            print("\n--- Sort Options ---")
                            print("1. Sort by Name (Ascending)")
                            print("2. Sort by Name (Descending)")
                            print("3. Sort by Studio (Ascending)")
                            print("4. Sort by Studio (Descending)")
                            print("5. Sort by Genre (Ascending)")
                            print("6. Sort by Genre (Descending)")
                            print("7. Sort by Year (Ascending)")
                            print("8. Sort by Year (Descending)")
                            print("9. Back")
                            inp = input("Enter choice: ").strip()

                            if inp == "1":
                                sort_movies("title", True)
                            elif inp == "2":
                                sort_movies("title", False)
                            elif inp == "3":
                                sort_movies("studio", True)
                            elif inp == "4":
                                sort_movies("studio", False)
                            elif inp == "5":
                                sort_movies("genre", True)
                            elif inp == "6":
                                sort_movies("genre", False)
                            elif inp == "7":
                                sort_movies("year", True)
                            elif inp == "8":
                                sort_movies("year", False)
                            elif inp == "9":
                                break
                            else:
                                print("Invalid option.")
                    print("(Log in to rate or add movies to playlists.)")

            elif choice == "2":
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                if login(username, password):
                    current_user = username

            elif choice == "3":
                username = input("Enter your username: ").strip()
                if len(username) > 50:
                    print("Username cannot exceed 50 characters.")
                    continue
                password = input("Enter your password: ").strip()
                first_name = input("Enter your first name: ").strip()
                last_name = input("Enter your last name: ").strip()
                email = input("Enter your email: ").strip()
                create_user(username, password, email, first_name, last_name)

            elif choice == "4":
                print("Goodbye.")
                break

            else:
                print("Invalid option.")


if __name__ == "__main__":
    main_menu()
