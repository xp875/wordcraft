import items

class Inventory(items.Storage):
	def __init__(self):
		super().__init__(1000000)
		self.inventory = {
			"storage": self.storage, 
			"weapon": None,
			"tool": None,
			"armour": None
		}


	def print(self):
		print("\n --- INVENTORY ---\n")
		for s in self.inventory["storage"]:
			s.print()
		if len(self.inventory["storage"]) == 0:
			print("(Empty)")

		print("\n-- WEAPON --")
		if self.inventory["weapon"] == None:
			print("Nothing")
		else:
			self.inventory["weapon"].print()

		print("\n-- TOOL --")
		if self.inventory["tool"] == None:
			print("Nothing")
		else:
			self.inventory["tool"].print()
			
		print("\n-- ARMOUR --")
		if self.inventory["armour"] == None:
			print("Nothing")
		else:
			self.inventory["armour"].print()
	

	def get_power(self, usage):
		if usage == "weapon":
			if self.inventory[usage] == None:
				return 1.0
			return self.inventory[usage].power()
		if usage == "tool":
			if self.inventory[usage] == None:
				return 0.0
			return self.inventory[usage].power()
		if usage == "armour": 
			if self.inventory[usage] == None:
				return 0.0
			return self.inventory[usage].power()


	def confirm_ust_item(self, type):
		print("")
		s = []
		for i in self.inventory["storage"]:
			if i.type == type:
				i.print()
				s.append(i)
		if len(s) == 0:
			print("You do not have", type, "\n")
			return -1
		
		if len(s) > 1:
			for i in range(len(s)):
				print(i, end=": ")
				s[i].print()
				
			x = input("Choice: ")
			try:
				i = int(x)
				if i >= len(s) or i<0:
					print("Out of range\n")
					return -1
				return s[i]
			except:
				print("Expected number\n")
				return -1
		else:
			return s[0]


	def print_equipment(self, usage, e="\n"):
		print(usage.upper()+":", end=" ")
		if self.inventory[usage] == None:
			print("Nothing", end=e)
		else:
			self.inventory[usage].print(e)
		

	def update_item(self, i):
		if not i.type in items.item_list or not items.is_ust(i.type):
			return 
		x = input("Use "+i.type+"? (Y/N): ")
		if x.upper() == "Y":
			if self.inventory[i.usage()] != None:
				self.add_ust_item(self.inventory[i.usage()])
			self.inventory[i.usage()] = i
			print("You are now using", end=" ")
			i.print()
			self.remove_ust_item(i.name)
		else:
			print("You are not using this")


	def update_equipment(self):
		for i, j in self.inventory.items():
			if i == "storage":
				continue
			if j == None:
				continue
			if j.durability <= 0:
				print(j.name, "broke!")
				self.inventory[i] = None


	def change_equipment(self, usage):
		print("")
		y = input("Change? (Y/N): ")
		print("")
		if y.upper() != "Y":
			return -1
		s = [None]

		for i in self.inventory["storage"]:
			if items.is_ust(i.type) and i.usage() == usage:
				s.append(i)
		
		if len(s) == 1 and self.inventory[usage] == None:
			print("You don't have any", usage, "to change to\n")
			return -1
		
		for i in range(len(s)):		
			print(i, end=": ")
			if s[i] == None:
				print("Nothing")
			else:
				s[i].print()

		x = input("\nChoice: ")
		try:
			i = int(x)
			if i < 0 or i >= len(s):
				print("Out of range\n")
				return -1

			if self.inventory[usage] != None:
				self.add_ust_item(self.inventory[usage])
			item = s[i]
			self.inventory[usage] = item
			self.remove_ust_item(item.name)
			if item == None:
				print("You are now not using any", usage, "\n")
			else:
				print("You are now using", end=" ")
				item.print("\n\n")
			
		except:
			print("Expected number\n")
			return -1
			