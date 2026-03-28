from pathlib import Path
import json

class Expense:
    DATABASE = "data.json"

    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        try:
            if Path(self.DATABASE).exists():
                with open(self.DATABASE, "r") as fs:
                    return json.load(fs)
            return []
        except Exception as err:
            print(f"Database Not Found : {err}")
            return []

    def __update(self):
        with open(self.DATABASE, 'w') as fs:
            fs.write(json.dumps(self.data, indent=4))

    def find_user(self, name, passw):
        userdata = [i for i in self.data if i['UserName'] == name and i['Password'] == passw]
        if not userdata:
            return None
        return userdata[0]

    def createNew(self, name, passw):
        # Check if user already exists to prevent duplicates
        if any(u['UserName'] == name for u in self.data):
            return False 
            
        user = {
            "UserName": name,
            "Password": passw,
            "expenses": []
        }
        self.data.append(user)
        self.__update()
        return True

    def newExpense(self, name, passw, date, category, description, amount):
        user = self.find_user(name, passw)
        if user:
            l = {
                "date": date,
                "category": category,
                "description": description,
                "amount": int(amount)
            }
            user["expenses"].append(l)
            self.__update()
            return True
        return False

    def showExpense(self, name, passw):
        user = self.find_user(name, passw)
        if user:
            return user["expenses"]
        return []

    def totalSpend(self, name, passw):
        user = self.find_user(name, passw)
        if user:
            expense = user["expenses"]
            total = 0
            for i in range(len(expense)):
                total += expense[i]["amount"]
            return total
        return 0