# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MOM(Document):
	pass


@frappe.whitelist()
def get_pending_actions(project):
	'''getting uncompleted tasks
	   output : list of uncompleted tasks according to the project
	'''
	return frappe.get_all('Task', filters = {'project': project, 'status': ['!=' , 'Completed']}, fields = ['subject', 'priority', 'description'])
	
	