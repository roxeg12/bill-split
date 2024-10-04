
class Bill:
    def __init__(self) -> None:
        self.total = None
        self.name = None
        self.data = []
        self.subtotal = None
        
    def __str__(self) -> str:
        pass

    """
    Method that will initialize the Bill object's data
    params:
    - name: the user given name of the bill as a string
    - data: a 2D list of data with the format: [[Good, price, quantity]]
    """
    def set_bill(self, name, data):
        self.name = name
        self.total = data["Total"]
        self.data = data["Items"]
        counter = 0
        for item in data:
            counter += item[1]
        self.subtotal = counter
    
    def get_bill(self):
        return {"Bill": self.name, "Data": self.data, "Total": self.total}
    
    def find_item(self, name):
        for item in self.data:
            if item[0] == name:
                return True
        return False
    
    def get_item(self, name):
        
        for item in self.data:
            if item[0] == name:
                return item, True
        return None, False
    
    def get_total(self):
        return self.total

    def add_item(self, item):
        if not self.find_item(item[0]): 
            self.data.append(item)
            return True
        else:
            return False
    
    def create_item(self, name, price, quantity):
        item = [name, price, quantity]
        return self.add_item(item)

    def force_add_item(self, item):
        self.data.append(item)

    def force_create_item(self, name, price, quantity):
        item = [name, price, quantity]
        self.force_add_item(item)
    
    def delete_item(self, name):
        for item in self.data:
            if item[0] == name:
                self.data.remove(item)
                return True
        return False
    
    def update_item(self, item):
        found = self.delete_item(item[0])
        if not found:
            return False
        else:
            self.add_item(item)
            return True
    #make: delete, update

    class BillSplitter:
        def __init__(self, Bill) -> None:
            self.bill = Bill
            self.people = []
            self.items = {}
            self.persons = {}
        
        def __str__(self) -> str:
            pass

        def split_equal(self, num_people):
            return self.bill.get_total() / num_people

        def add_person(self, name):
            if name not in self.people:
                self.people.append(name)

                return True
            return False
        
        def remove_person(self, name):
            if name in self.people:
                self.people.remove()
                return True
            return False
         

         #method 1: split by person - each person picks what they ate from, each of those items is split evenly among the people that
         #          picked it, each person pays the total of their shares of the items they picked
         #method 2: split by percentage - each person is assigned a percentage of the meal to pay, the total is split according to
         #          that ratio
