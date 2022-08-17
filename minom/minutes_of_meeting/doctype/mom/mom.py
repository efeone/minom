# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

from tabnanny import check
import frappe
from frappe.model.document import Document


class MOM(Document):
	def on_submit(self):
		if self.project:#create task against project
			mom_doc = frappe.new_doc('Task')
			mom_doc.subject = self.project_name
			mom_doc.project = self.project
			mom_doc.save()


@frappe.whitelist()
def get_last_mom(project):
    '''
            getting the last mom of the selected project
            output: last mom document
    '''
    last_mom = frappe.get_last_doc('MOM', filters={'project': project})
    return last_mom


@frappe.whitelist()
def get_pending_actions(project):
    '''getting uncompleted tasks
       output : list of uncompleted tasks according to the project
    '''
    return frappe.get_all('Task', filters={'project': project, 'status': ['!=', 'Completed']}, fields=['name', 'subject', 'priority', 'description'])
