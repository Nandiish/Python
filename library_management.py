from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk


# MySQL connection
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='nandiish',
            user='root',
            password=''  # Replace with your MySQL password if needed
        )
        return conn
    except Error as e:
        messagebox.showerror("Database Error", str(e))
        return None


# Creating the main application window
class LibraryApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("1550x800+0+0")

        # Load the original background image
        self.original_image = Image.open("C:\\Users\\Nandiish\\Desktop\\PYTHON\\TKINTER\\4.jpg")

        # Set up the background label
        self.bg_label = Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bind the <Configure> event to dynamically resize the image
        self.bind("<Configure>", self.resize_image)

        self.username = StringVar()
        self.password = StringVar()

        self.login_screen()

    def resize_image(self, event):
        # Resize the image based on the current window size
        new_width = event.width
        new_height = event.height
        resized_image = self.original_image.resize((new_width, new_height),
                                                   Image.Resampling.LANCZOS)  # Use Image.Resampling.LANCZOS or Image.LANCZOS
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.bg_label.config(image=self.bg_image)

    def login_screen(self):
        Label(self, text="Login", font=("Arial", 55, "bold"), bg='lightblue').place(x=680, y=170)
        Label(self, text="Username", font=("Arial", 20), bg='lightblue').place(x=715, y=300)
        Entry(self, textvariable=self.username, width=25).place(x=703, y=355)
        Label(self, text="Password", font=("Arial", 21), bg='lightblue').place(x=715, y=385)
        Entry(self, textvariable=self.password, show='*', width=25).place(x=702, y=435)
        Button(self, text="Login", command=self.check_login, font=10, width=8).place(x=730, y=500)

    def check_login(self):
        user = self.username.get()
        pwd = self.password.get()

        conn = connect_db()  # Calls the connect_db() function
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin WHERE user=%s AND password=%s", (user, pwd))
            result = cursor.fetchone()
            conn.close()

            if result:
                self.main_screen()
            else:
                messagebox.showerror("Login Error", "Invalid Username or Password")
        else:
            messagebox.showerror("Connection Error", "Unable to connect to the database")

    def main_screen(self):
        self.clear_screen()

        self.title("Library Management System")
        Label(self, text="Library Management System", font=("Arial", 44, "bold"), bg='lightblue').place(x=389, y=170)

        Button(self, text="Add Book", font=10, width=12, command=self.add_book_screen).place(x=715, y=300)
        Button(self, text="View Books", font=10, width=12, command=self.view_books_screen).place(x=715, y=360)
        Button(self, text="Remove Book", font=10, width=12, command=self.remove_book_screen).place(x=715, y=420)
        Button(self, text="Logout", font=8, width=10, command=self.logout).place(x=725, y=500)

    def add_book_screen(self):
        self.clear_screen()

        self.book_title = StringVar()
        self.book_author = StringVar()
        self.book_year = StringVar()
        self.book_isbn = StringVar()

        Label(self, text="Add Book", font=("Arial", 35, "bold"), bg='lightblue').pack(pady=20)
        Label(self, text="Title", font=10, width=12, bg='lightblue').pack(pady=5)
        Entry(self, textvariable=self.book_title).pack(pady=5)
        Label(self, text="Author", font=10, width=12, bg='lightblue').pack(pady=5)
        Entry(self, textvariable=self.book_author).pack(pady=5)
        Label(self, text="Year", font=10, width=12, bg='lightblue').pack(pady=5)
        Entry(self, textvariable=self.book_year).pack(pady=5)
        Label(self, text="ISBN", font=10, width=12, bg='lightblue').pack(pady=5)
        Entry(self, textvariable=self.book_isbn).pack(pady=5)
        Button(self, text="Add", width=8, command=self.add_book).pack(pady=20)
        Button(self, text="Back", command=self.main_screen).pack(pady=20)

    def add_book(self):
        title = self.book_title.get()
        author = self.book_author.get()
        year = self.book_year.get()
        isbn = self.book_isbn.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO books (title, author, year, isbn) VALUES (%s, %s, %s, %s)",
                           (title, author, year, isbn))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Book Added Successfully")
            self.clear_screen()
            self.main_screen()
        else:
            messagebox.showerror("Connection Error", "Unable to connect to the database")

    def view_books_screen(self):
        self.clear_screen()
        Label(self, text="Books List", font=("Arial", 24), bg='lightblue').pack(pady=20)

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()
            conn.close()

            for book in books:
                Label(self,
                      text=f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Year: {book[3]} | ISBN: {book[4]}",
                      bg='lightblue').pack(pady=5)

        Button(self, text="Back", command=self.main_screen).pack(pady=20)

    def remove_book_screen(self):
        self.clear_screen()

        self.book_id = StringVar()

        Label(self, text="Remove Book", font=("Arial", 35, "bold"), bg='lightblue').pack(pady=20)
        Label(self, text="Enter Book ID", font=10, width=12, bg='lightblue').pack(pady=5)
        Entry(self, textvariable=self.book_id).pack(pady=5)
        Button(self, text="Remove", width=8, command=self.remove_book).pack(pady=20)
        Button(self, text="Back", width=8, command=self.main_screen).pack(pady=5)

    # def remove_book(self):
    #     book_id = self.book_id.get()
    #
    #     if not book_id:
    #         messagebox.showerror("Input Error", "Please enter a Book ID")
    #         return
    #
    #     conn = connect_db()
    #     if conn:
    #         cursor = conn.cursor()
    #         cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    #         conn.commit()
    #         conn.close()
    #
    #         if cursor.rowcount > 0:
    #             messagebox.showinfo("Success", "Book Removed Successfully")
    #         else:
    #             messagebox.showerror("Error", "Book ID not found")
    #
    #         self.clear_screen()
    #         self.main_screen()

    def remove_book(self):
        book_id = self.book_id.get()
        print(book_id)

        if not book_id:
            messagebox.showerror("Input Error", "Please enter a Book ID")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))

            conn.commit()
            conn.close()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Book Removed Successfully")
            else:
                messagebox.showerror("Error", "Book ID not found")

            self.clear_screen()
            self.main_screen()
        else:
            messagebox.showerror("Connection Error", "Unable to connect to the database")

    def logout(self):
        self.clear_screen()
        self.login_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Re-add the background image after clearing the screen
        self.bg_label = Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Running the application
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
