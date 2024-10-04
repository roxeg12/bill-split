
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
    
    def get_item_price(self, name):
        item, found = self.get_item(name)
        return item[1], found
    
    def get_item_quantity(self, name):
        item, found = self.get_item(name)
        return item[2], found

    def get_total(self):
        return self.total
    
    def get_subtotal(self):
        return self.subtotal

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
            self.equal = False
            self.percentage = False
            self.byitem = False
        
        def __str__(self) -> str:
            pass

        def split_equal(self, people):
            share = self.bill.get_total() / len(people)
            shares = {}
            for person in people:
                shares[person] = share
            return shares, True

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
        
        def reset_split_method(self):
            self.equal = False
            self.percentage = False
            self.byitem = False
            self.persons = {}
            self.items = {}


        def set_split_method(self, method, data):
            self.reset_split_method()
            if method == "equal":
                self.equal = True
                self.people = data
                return True
            elif method == "percentage":
                self.percentage = True
                self.persons = data["persons"]
                
                return True
            elif method == "by item":
                self.byitem = True
                self.persons = data["persons"]
                self.items = data["items"]
                return True
            else:
                return False
            
        def split_percentage(self):
            bill_total = self.bill.get_total()
            shares = {}
            for person in self.persons.keys():
                percent = self.persons[person]
                shares[person] = bill_total * percent
            return shares
        
        def split_items(self):
            bill_difference = self.bill.get_total() - self.bill.get_subtotal()
            equal_share = bill_difference / len(self.persons)
            shares = {}
            item_shares = {}
            for item in self.items.keys():
                if self.bill.find_item(item):
                    item_price, found = self.bill.get_item_price(item)
                    item_share = item_price / self.items[item]
                    item_shares[item] = item_share
                else:
                    return {}, False
            
            
            for person in self.persons.keys():
                
                share = 0
                item_list = self.persons[person]
                for item in item_list:
                    if item in item_shares:
                        share += item_shares[item]
                    else:
                        return {}, False
                shares[person] = share + equal_share

            return shares, True

        
         #method 1: split by person - each person picks what they ate from, each of those items is split evenly among the people that
         #          picked it, each person pays the total of their shares of the items they picked
         #method 2: split by percentage - each person is assigned a percentage of the meal to pay, the total is split according to
         #          that ratio
