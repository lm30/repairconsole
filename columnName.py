import enum

class ColumnNameMeta(enum.EnumMeta):
	def __contains__(cls, item):
		return item in [v.value for v in cls.__members__.values()]

class ColumnName(enum.Enum, metaclass=ColumnNameMeta):
	# repairnumber = 5
	repairnumber = "Repair number"
	firstname = "First name"
	lastname = "Last name"
	email = "Email"
	phone = "Phone"
	daterecieved = "Date recieved"
	lastupdated = "Last updated"
	repairedby = "Repaired by"
	comments = "Comments"
	typeof = "Type of"
	manufacturer = "Manufacturer"
	model = "Model"
	status = "Status"

	@classmethod
	def has_value(cls, value):
		return value in cls._value2member_map_

	@classmethod
	def isDate(cls, key):
		""" 
		Returns true if the key exists in the enum and if it is a label for a date
		"""
		if key in ColumnName.__members__:
			if "date" in key:
				return True
		return False


# print(ColumnName("repairnumber"))
# print(ColumnName("Repair number"))
# print(ColumnName.isDate("repairnumber"))
# print(ColumnName.isDate("Repair Number"))
# print(ColumnName.isDate("daterecieved"))
# print(ColumnName.isDate("Date Recieved"))
# print(ColumnName.isDate("lastupdated"))
# print(ColumnName.isDate("Last Updated"))
# print(ColumnName['repairnumber'])
# print(ColumnName['repairnumber'].name)
# print(ColumnName['repairnumber'].value)
# print(type(ColumnName['repairnumber'].value))
# print('repairnumber' in ColumnName.__members__)
# print('repairnumbers' in ColumnName.__members__)
# print('Repair number' in ColumnName)
# print('Repair numbers' in ColumnName)	
# print('repairnumber' in ColumnName._member_names_)
# print('repairnumbers' in ColumnName._member_names_)