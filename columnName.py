# from enum import Enum
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