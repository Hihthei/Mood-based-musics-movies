import json
import os
from tkinter import messagebox

class DBCommunicate:
    def __init__(self):
        self.__hassed_pswd = {}
        self.__file_path = "../Security/tmp_psd_base.json"
        self.__check_database()

    def __check_database(self):
        try:
            if not os.path.exists(self.__file_path) or os.stat(self.__file_path).st_size == 0:
                with open(self.__file_path, "w") as pf:
                    json.dump({}, pf) # type: ignore

        except json.JSONDecodeError:
            with open(self.__file_path, "w") as pf:
                json.dump({}, pf) # type: ignore

        except Exception as e:
            raise e

    def load_hashed_pswd(self):
        try:
            with open(self.__file_path, "r") as pf:
                self.hassed_pswd = json.load(pf)

        except FileNotFoundError:
            self.hassed_pswd = {}
            messagebox.showerror("Error", "No password file loaded")

        except json.JSONDecodeError:
            self.hassed_pswd = {}
            messagebox.showerror("Error", "Password file is corrupted")

        except Exception as e:
            self.hassed_pswd = {}
            messagebox.showerror("Error", str(e))

        finally:
            return self.hassed_pswd.copy()

    def save_hashed_pswd(self, hassed_pswd: dict):
        self.hassed_pswd = hassed_pswd
        try:
            with open(self.__file_path, "w") as pf:
                json.dump(self.hassed_pswd, pf, indent=4) #type: ignore

        except Exception as e:
            raise e

    def reinitialise_database(self):
        try:
            with open(self.__file_path, "w") as pf:
                json.dump({}, pf) # type: ignore

        except Exception as e:
            raise e

