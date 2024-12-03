import json
import os
from tkinter import messagebox

class DBCommunicate:
    def __init__(self):
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
        hassed_pswd = {}
        try:
            with open(self.__file_path, "r") as pf:
                hassed_pswd = json.load(pf)

        except FileNotFoundError:
            messagebox.showerror("Error", "No password file loaded")

        except json.JSONDecodeError:
            messagebox.showerror("Error", "Password file is corrupted")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            return hassed_pswd.copy()

    def save_hashed_pswd(self, hassed_pswd: dict):
        try:
            with open(self.__file_path, "w") as pf:
                json.dump(hassed_pswd, pf, indent=4) #type: ignore

        except Exception as e:
            raise e

    def reinitialise_database(self):
        try:
            with open(self.__file_path, "w") as pf:
                json.dump({}, pf) # type: ignore

        except Exception as e:
            raise e
