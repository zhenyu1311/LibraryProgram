class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

class Library2:
    def __init__(self):
        self.root = TreeNode("Library")
        self.categories = [
            "Fiction",
            "Science Fiction",
            "Mystery",
            "Fantasy",
            "Horror",
            "Biography",
            "History",
            "Non-Fiction",
            "Romance",
            "Thriller",
            "Adventure",
            "Children's"
        ]

    def add_book2(self, book_name, author, category):
        current_node = self.root
        for word in book_name.split() + author.split():
            child = None
            for node in current_node.children:
                if word in node.value:
                    child = node
                    break

            if child is None:
                child = TreeNode(word)
                current_node.add_child(child)
            current_node = child

        current_node.add_child(TreeNode(f"{book_name} - {author} - {category}"))

    def get_recommendation(self, book_name, author):
        category_scores = {category: 0 for category in self.categories}

        book_keywords = book_name.split() + author.split()
        for category in self.categories:
            for keyword in category.split():
                for book_keyword in book_keywords:
                    if keyword in book_keyword:
                        category_scores[category] += 1

        recommended_category = max(category_scores, key=category_scores.get)
        return recommended_category

def build_library_from_list(book_data):
    root = TreeNode("Library")

    for book_info in book_data:
        title = book_info['title']
        author = book_info['author']
        genre = book_info['genre']

        current_node = root

        for word in title.split() + author.split():
            child = None
            for node in current_node.children:
                if word in node.value:
                    child = node
                    break

            if child is None:
                child = TreeNode(word)
                current_node.add_child(child)
            current_node = child

        current_node.add_child(TreeNode(f"{title} - {author} - {genre}"))

    return root

def cosine_similarity(vector1, vector2):
    common_words = set(vector1.keys()) & set(vector2.keys())
    numerator = sum(vector1[word] * vector2[word] for word in common_words)
    sum1 = sum(vector1[word] ** 2 for word in vector1)
    sum2 = sum(vector2[word] ** 2 for word in vector2)

    if sum1 == 0 or sum2 == 0:
        return 0.0

    denominator = (sum1 ** 0.5) * (sum2 ** 0.5)

    if denominator == 0:
        return 0.0

    return numerator / denominator

def vectorize(text):
    words = text.lower().split()
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def flexible_fuzzy_match(node, query):
    results = []

    query_vector = vectorize(query.lower())

    for child in node.children:
        book_info = child.value.lower().split(' - ')
        book_name_vector = vectorize(book_info[0])
        author_vector = vectorize(book_info[1]) if len(book_info) > 1 else {}
        similarity = cosine_similarity(query_vector, book_name_vector) + cosine_similarity(query_vector, author_vector)

        if similarity >= 0.5:
            if len(book_info) > 1:
                results.append(child.value)

        results += flexible_fuzzy_match(child, query)

    return results

seats = {}

def add_seat():
    seat_id = input("Enter your seat id:")
    if seat_id in seats:
        print("The seat already exists")
    else:
        seats[seat_id] = 'vacancy'
        print(f"Seat {seat_id} has been added successfully")

def preview_and_reserve_seat():
    seat_id = input("Enter your seat id:")
    if seat_id in seats:
        if seats[seat_id] == 'vacancy':
            seats[seat_id] = 'Scheduled'
            print(f"Seat {seat_id} has been successfully reserved")
        else:
            print(f"Seat {seat_id} has been reserved, please select a different seat")
    else:
        print("error:Seats do not exist")

def preview_all_seats():
    if not seats:
        print("There are no seats in the library")
    else:
        total_seats = len(seats)
        vacant_seats = sum(1 for status in seats.values() if status == 'vacancy')
        reserved_seats = total_seats - vacant_seats
        print(f"Total number of seats:{total_seats}")
        print(f"Number of vacant seats:{vacant_seats}")
        print(f"The number of seats reserved:{reserved_seats}")

def change_seat_status():
    seat_id = input("Enter your seat id:")
    if seat_id in seats:
        new_status = input("Please enter your new seat status (vacant/booked):")
        if new_status in ['vacancy', 'Scheduled']:
            seats[seat_id] = new_status
            print(f"Seat {seat_id} status updated to {new_status}")
        else:
            print("error")
    else:
        print("error:Seats do not exist")

def initialize_seats(status):
    for seat_id in seats:
        seats[seat_id] = status
    print(f"All seats have been initialized to {status} status")

class Book:
    def __init__(self, id, title, author, genre, remaining):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.remaining = remaining

    def __repr__(self):
        return f"ID: {self.id}, Title: {self.title}, Author: {self.author}, Genre: {self.genre}, Remaining: {self.remaining}"

class Library:
    def __init__(self, book_data):
        self.books = [Book(**book) for book in book_data]
        self.book_data = book_data
    def list_books(self):
        for book in self.books:
            print(book)

    def find_book_by_id(self, book_id):
        for book in self.books:
            if book.id == book_id:
                return book
        return "Book not found."

    def list_all_titles(self):
        for book in self.books:
            print(f"ID: {book.id}, Title: {book.title}")

    def add_book(self, book_data):
        new_book = Book(**book_data)
        self.books.append(new_book)
        print(f"Added book: {new_book}")

    def modify_book(self, book_id):
        book = self.find_book_by_id(book_id)
        if book != "Book not found.":
            print("Enter the new details for the book.")
            book.title = input("Title: ")
            book.author = input("Author: ")
            book.genre = input("Genre: ")
            book.remaining = int(input("Remaining: "))
            print(f"Book ID {book_id} has been updated.")
        else:
            print(book)

    def delete_book(self, book_id):
        book_to_delete = self.find_book_by_id(book_id)
        if book_to_delete != "Book not found.":
            self.books = [book for book in self.books if book.id != book_id]
            print(f"Book ID {book_id} has been deleted.")
        else:
            print(book_to_delete)


    def find_specific_librarys(self, keyword):
      librar_with_keyword = []
      for library in self.book_data:
        for col in library.keys():
          if type(library[col]) is list or type(library[col]) is str:
            if keyword in library[col]:
              librar_with_keyword.append(library)
              break
          else:
            if keyword == library[col]:
              librar_with_keyword.append(library)
              break
      res=[Book(**book) for book in librar_with_keyword]
      for book in res:
        print(book)

    def bucketize(self, category):
      #print(self.book_data)
      buckets = {}
      for library in self.book_data:
        if type(library[category]) is list:
          for j in library[category]:
            if j not in buckets:
              buckets[j] = [library]
            else:
              buckets[j].append(library)
        else:
          if library[category] not in buckets:
            buckets[library[category]] = [library]
          else:
            buckets[library[category]].append(library)
      for i in buckets:
        print(category+' '+str(i))
        res=[Book(**book) for book in buckets[i]]
        for book in res:
            print(book)


class User:
    def __init__(self, user_id, name, id_number, book_id, return_date, banned, seat_id, appointment_time):
        self.user_id = user_id
        self.name = name
        self.id_number = id_number
        self.book_id = book_id
        self.return_date = return_date
        self.banned = banned
        self.seat_id = seat_id
        self.appointment_time = appointment_time

    def __repr__(self):
        return f"User ID: {self.user_id}, Name: {self.name}, ID Number: {self.id_number}, Book ID: {self.book_id}, Return Date: {self.return_date}, Banned: {self.banned}, Seat ID: {self.seat_id}, Appointment Time: {self.appointment_time}"


class UserBase:
    def __init__(self, user_data):
        self.users = [User(**user) for user in user_data]
        self.user_data = user_data

    def user_add(self, new_user):
        self.users.append(new_user)
        print(f"User '{new_user.name}' added successfully.")

    def user_delete(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                self.users.remove(user)
                print(f"User with ID '{user_id}' deleted successfully.")
                return
        print(f"User with ID '{user_id}' does not exist in the system.")

    def user_modify(self, user_id, new_info):
        for user in self.users:
            if user.user_id == user_id:
                self.users.remove(user)
                self.users.append(new_info)
                print(f"User with ID '{user_id}' information updated successfully.")
                return
        print(f"User with ID '{user_id}' does not exist in the system.")

    def user_search(self, search_criteria, search_value):
        found_users = []

        for user in self.users:
            if search_criteria == 'name' and user.name == search_value:
                found_users.append(user)
            elif search_criteria == 'id number' and user.id_number == search_value:
                found_users.append(user)
            elif search_criteria == 'user_id' and user.user_id == search_value:
                found_users.append(user)
            elif search_criteria == 'banned' and user.banned == (search_value.lower() == 'yes'):
                found_users.append(user)

        return found_users

    def check_appointment_overlap(self, new_appointment_time):
        for user in self.users:
            if user.appointment_time == new_appointment_time:
                return True  # Overlapping appointment time found
        return False


def main():

    user_data = [
        {'user_id': '001', 'name': 'John Doe', 'id_number': '123456789', 'book_id': '101', 'return_date': '2023-12-01',
         'banned': False, 'seat_id': 'A1', 'appointment_time': '09:00 AM'},
        {'user_id': '002', 'name': 'Jane Smith', 'id_number': '987654321', 'book_id': '102', 'return_date': '2023-12-15',
         'banned': True, 'seat_id': 'B2', 'appointment_time': '02:30 PM'},
        # 先随便写两个
    ]

    book_data = [
        {'id': 1, 'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'genre': 'Fiction', 'remaining': 5},
        {'id': 2, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'genre': 'Fiction', 'remaining': 4},
        {'id': 3, 'title': '1984', 'author': 'George Orwell', 'genre': 'Science Fiction', 'remaining': 6},
        {'id': 4, 'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'genre': 'Fiction', 'remaining': 3},
        {'id': 5, 'title': 'The Da Vinci Code', 'author': 'Dan Brown', 'genre': 'Mystery', 'remaining': 7},
        {'id': 6, 'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'genre': 'Fantasy', 'remaining': 5},
        {'id': 7, 'title': 'A Game of Thrones', 'author': 'George R.R. Martin', 'genre': 'Fantasy', 'remaining': 4},
        {'id': 8, 'title': 'The Shining', 'author': 'Stephen King', 'genre': 'Horror', 'remaining': 4},
        {'id': 9, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'genre': 'Fiction', 'remaining': 3},
        {'id': 10, 'title': 'Harry Potter and the Sorcerer’s Stone', 'author': 'J.K. Rowling', 'genre': 'Fantasy', 'remaining': 8},
        {'id': 11, 'title': 'The Alchemist', 'author': 'Paulo Coelho', 'genre': 'Fiction', 'remaining': 6},
        {'id': 12, 'title': 'Sherlock Holmes: A Study in Scarlet', 'author': 'Arthur Conan Doyle', 'genre': 'Mystery', 'remaining': 5},
        {'id': 13, 'title': 'The Girl on the Train', 'author': 'Paula Hawkins', 'genre': 'Mystery', 'remaining': 7},
        {'id': 14, 'title': 'Gone Girl', 'author': 'Gillian Flynn', 'genre': 'Mystery', 'remaining': 5},
        {'id': 15, 'title': 'The Martian', 'author': 'Andy Weir', 'genre': 'Science Fiction', 'remaining': 5},
        {'id': 16, 'title': 'Educated', 'author': 'Tara Westover', 'genre': 'Biography', 'remaining': 4},
        {'id': 17, 'title': 'War and Peace', 'author': 'Leo Tolstoy', 'genre': 'History', 'remaining': 3},
        {'id': 18, 'title': 'Anna Karenina', 'author': 'Leo Tolstoy', 'genre': 'Fiction', 'remaining': 3},
        {'id': 19, 'title': 'Crime and Punishment', 'author': 'Fyodor Dostoevsky', 'genre': 'Fiction', 'remaining': 4},
        {'id': 20, 'title': 'The Brothers Karamazov', 'author': 'Fyodor Dostoevsky', 'genre': 'Fiction', 'remaining': 2},
        {'id': 21, 'title': 'The Lord of the Rings: The Fellowship of the Ring', 'author': 'J.R.R. Tolkien', 'genre': 'Fantasy', 'remaining': 3},
        {'id': 22, 'title': 'The Hunger Games', 'author': 'Suzanne Collins', 'genre': 'Science Fiction', 'remaining': 7},
        {'id': 23, 'title': 'The Catcher in the Rye: Study Guide', 'author': 'J.D. Salinger', 'genre': 'Non-Fiction', 'remaining': 2},
        {'id': 24, 'title': 'Harry Potter and the Chamber of Secrets', 'author': 'J.K. Rowling', 'genre': 'Fantasy', 'remaining': 8},
        {'id': 25, 'title': 'The Catcher in the Rye: Cliff’s Notes', 'author': 'J.D. Salinger', 'genre': 'Non-Fiction', 'remaining': 8}
    ]

    user_base = UserBase(user_data)
    library_instance = Library(book_data)
    library_root = build_library_from_list(book_data)
    library = Library2()

    while True:
        print("\nLibraNexus Main Menu:")
        print("1. Add user")
        print("2. Delete user")
        print("3. Modify user")
        print("4. User search")
        print("5. List all books")
        print("6. List all book titles and IDs")
        print("7. Find book by ID")
        print("8. Add a new book")
        print("9. Modify an existing book")
        print("10. Delete a book")
        print("11. Specific Search")
        print("12. Classification Search")
        print("13. Fuzzy match")
        print("14. Add a Book")
        print("15. Add a seat")
        print("16. Preview your seat and reserve it")
        print("17. Preview all seat counts and operate them in one place")
        print("18. Change the status of your reserved seat")
        print("Q. Exit")

        option = input("Enter option: ")
        
        if option == '1':
            while True:
                # Input user information
                user_id = input("Enter User ID: ")
        
                # Check if the user ID is already in use
                if any(user.user_id == user_id for user in user_base.users):
                    print("User ID is not unique. Please choose a different one.")
                else:
                    name = input("Enter Name: ")
                    id_number = input("Enter ID Number: ")
                    book_id = input("Enter Book ID: ")
                    return_date = input("Enter Return Date: ")
        
                    banned_input = input("Is the user banned? (yes/no): ").lower()
                    banned = True if banned_input == 'yes' else False
        
                    seat_id = input("Enter Seat ID: ")
                    appointment_time = input("Enter Appointment Time: ")
        
                    # Check for appointment time overlap
                    if user_base.check_appointment_overlap(appointment_time):
                        print("Appointment time overlaps with an existing user. Please choose a different time.")
                    else:
                        new_user = User(user_id, name, id_number, book_id, return_date, banned, seat_id, appointment_time)
                        user_base.user_add(new_user)
                        break
        
        elif option == '2':
            user_id_to_delete = input("Enter the User ID to delete: ")
            user_base.user_delete(user_id_to_delete)
        
        elif option == '3':
            user_id_to_modify = input("Enter the User ID to modify: ")
            user_to_modify = None
        
            for user in user_base.users:
                if user.user_id == user_id_to_modify:
                    user_to_modify = user
                    break
        
            if user_to_modify is not None:
                while True:
                    new_user_id = input("Enter new User ID: ")
        
                    # Check if the new User ID is already in use
                    if new_user_id != user_id_to_modify and any(user.user_id == new_user_id for user in user_base.users):
                        print("User ID is not unique. Please choose a different one.")
                    else:
                        name = input("Enter new Name: ")
                        id_number = input("Enter new ID Number: ")
                        book_id = input("Enter new Book ID: ")
                        return_date = input("Enter new Return Date: ")
        
                        banned_input = input("Is the user banned? (yes/no): ").lower()
                        banned = True if banned_input == 'yes' else False
        
                        seat_id = input("Enter new Seat ID: ")
                        appointment_time = input("Enter new Appointment Time: ")
        
                        # Check for appointment time overlap
                        if appointment_time != user_to_modify.appointment_time and user_base.check_appointment_overlap(
                                appointment_time):
                            print("Appointment time overlaps with an existing user. Please choose a different time.")
                        else:
                            new_info = User(new_user_id, name, id_number, book_id, return_date, banned, seat_id,
                                            appointment_time)
                            user_base.user_modify(user_id_to_modify, new_info)
                            break
            else:
                print(f"User with User ID {user_id_to_modify} not found.")
        
        elif option == '4':
            search_criteria = input("Enter a search criteria (e.g., user_id, id_number, banned): ")
            search_value = input(f"Enter the {search_criteria} to search for: ")
            found_users = user_base.user_search(search_criteria, search_value)
        
            if found_users:
                print("Found Users:")
                for found_user in found_users:
                    print(found_user)
            else:
                print(f"No users found based on the criteria: {search_criteria} = {search_value}")
        elif option == '5':
            library_instance.list_books()
        elif option == '6':
            library_instance.list_all_titles()
        elif option == '7':
            book_id = int(input("Enter book ID: "))
            print(library_instance.find_book_by_id(book_id))
        elif option == '8':
            book_data = {
                'id': int(input("ID: ")),
                'title': input("Title: "),
                'author': input("Author: "),
                'genre': input("Genre: "),
                'remaining': int(input("Remaining: "))
            }
            library_instance.add_book(book_data)
        elif option == '9':
            book_id = int(input("Enter the ID of the book you want to modify: "))
            library_instance.modify_book(book_id)
        elif option == '10':
            book_id = int(input("Enter the ID of the book you want to delete: "))
            library_instance.delete_book(book_id)
        elif option == '11':
          keyword=input('Enter the keyword you want to query:')
          library_instance.find_specific_librarys(keyword)
        elif option == '12':
          category=input('Enter the category you want to query:')
          library_instance.bucketize(category)
        elif option == '13':
            query = input("Please enter the title, title keyword, author name, or related words:")
            matches = flexible_fuzzy_match(library_root, query)

            if matches:
                print(f"The result for '{query}' is/are:")
                for match in matches:
                    print(match)
            else:
                print(f"No result was found matching '{query}'.")
        elif option == '14':
            book_name = input("Enter the book title:")
            author = input("Enter the author name:")
            category = library.get_recommendation(book_name, author)
            library.add_book2(book_name, author, category)
            print(f"Book '{book_name}' by {author} recommended to added to '{category}'.")

        elif option == '15':
            add_seat()
        elif option == '16':
            preview_and_reserve_seat()
        elif option == '17':
            preview_all_seats()
            init_choice = input("1--Initialize all seats as vacant\n2--Initialize all seats as booked\nSelect (1/2):")
            if init_choice == '1':
                initialize_seats('vacancy')
            elif init_choice == '2':
                initialize_seats('Scheduled')
            else:
                print("error")
        elif option == '18':
            change_seat_status()
        elif option == 'Q':
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please try again.")
            
main()
        
        
