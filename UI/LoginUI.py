import sys
import customtkinter as ctk
from classes.user import User
from database.UserDB import UserDB
from UI.widgets import WarningMessage
sys.path.append('../Library-Management-System')

FONT_FAM = "Comfortaa"


class SignUpUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initial
        self.title("Sign-Up")
        self.geometry("350x500")
        self.resizable(False, False)

        self.__email = None
        self.__password = None

        self.CreateUI()

    def GetEmail(self):
        return self.__email

    def GetPassword(self):
        return self.__password

    def SetEmail(self, email):
        self.__email = email

    def SetPassword(self, passwd):
        self.__password = passwd

    def CreateUI(self):
        # Title
        ctk.CTkLabel(
            self, text="Sign-Up to Library System",
            font=(FONT_FAM, 25, "bold"), pady=25).pack()

        # User entry
        ctk.CTkLabel(self, text="E-mail:", font=(FONT_FAM, 15)).pack(pady=20)
        self.email_entry = ctk.CTkEntry(
            self, placeholder_text="email@example.com")

        self.email_entry.pack()

        ctk.CTkLabel(self, text="Password:", font=(FONT_FAM, 15)).pack(pady=20)
        self.password_entry = ctk.CTkEntry(
            self, placeholder_text="*****", show='*')

        self.password_entry.pack()

        # Submit button
        ctk.CTkButton(
            self, text="Sign-Up",
            command=lambda: (self.SignUp())
            ).pack(pady=50)

    def SignUp(self):
        self.SetEmail(self.email_entry.get())
        self.SetPassword(self.password_entry.get())

        if not (self.GetEmail() and self.GetPassword()):
            WarningMessage("Please enter email and password")
            return

        if not User.ValidateEmail(self.GetEmail()):
            WarningMessage(
                "Please enter a valid e-mail\n\nExample: email@example.com")
            return

        # Debug Section
        user = User(self.GetEmail(), self.GetPassword())
        userDB = UserDB(':memory:')

        # Database check not working properly
        db_check = userDB.SearchByArg("email", self.GetEmail())
        print("db_check: ", db_check)
        if db_check:
            WarningMessage("This email already exists.")
            return

        userDB.AddUser(user)

        print(f"Sign-up, email {self.GetEmail()}, passwd: {self.GetPassword()}")
        print("\nUsers:")
        users = userDB.GetUsers()
        for user in users:
            print(user)
        # End of Debug

        return True


class LoginUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")

        # Initial
        self.title("Log-in")
        self.geometry("600x500")
        self.resizable(False, False)

        self.__email = None
        self.__password = None

        self.CreateUI()

    def GetEmail(self):
        return self.__email

    def GetPassword(self):
        return self.__password

    def SetEmail(self, email):
        self.__email = email

    def SetPassword(self, passwd):
        self.__password = passwd

    def CreateUI(self):
        # Title
        ctk.CTkLabel(
            self, text="Library Book Matching System\nLogin Page",
            font=(FONT_FAM, 25, "bold"), pady=25).pack()

        # User entry
        ctk.CTkLabel(
            self, text="E-mail:", font=(FONT_FAM, 15)
        ).place(x=190, y=125)

        self.email_entry = ctk.CTkEntry(
            self, placeholder_text="email@example.com")
        self.email_entry.place(x=275, y=125)

        ctk.CTkLabel(
            self, text="Password:", font=(FONT_FAM, 15)
        ).place(x=180, y=175)

        self.password_entry = ctk.CTkEntry(
            self, placeholder_text="*****", show='*')
        self.password_entry.place(x=275, y=175)

        # Submit button
        ctk.CTkButton(
            self, text="Login", command=lambda: (self.Login())
        ).place(x=275, y=225)

        # Sign-up button
        ctk.CTkButton(
            self, text="Sign-Up", command=lambda: (self.InitSignUp())
            ).place(x=275, y=275)

    def InitSignUp(self):
        signUpApp = SignUpUI()
        signUpApp.mainloop()

    def Login(self):
        self.SetEmail(self.email_entry.get())
        self.SetPassword(self.password_entry.get())

        if not (self.GetEmail() and self.GetPassword()):
            WarningMessage("Please enter email and password")
            return

        if not User.ValidateEmail(self.GetEmail()):
            WarningMessage(
                "Please enter a valid e-mail\n\nExample: email@example.com")
            return

        # Debug Section
        userDB = UserDB(':memory:')

        # This search not working properly
        user = userDB.SearchByArg("email", self.GetEmail())

        if not user:
            WarningMessage("User not found.")
            return

        # This part need to change
        if user[2] == self.GetPassword():
            # login
            print(f"Login, email {self.GetEmail()}, passwd: {self.GetPassword()}")  # Debug
        # End of Debug


if __name__ == "__main__":
    app = LoginUI()
    app.mainloop()
