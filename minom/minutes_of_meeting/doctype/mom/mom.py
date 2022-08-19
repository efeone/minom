# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

from tabnanny import check
import frappe
from frappe import _
from frappe.model.document import Document


class MOM(Document):
	def on_submit(self):
		if self.project:#create task aginst subject while submitting MOM
			for actions_list in self.actions:
				mom_doc = frappe.new_doc('Task')
				mom_doc.project = self.project
				mom_doc.subject = actions_list.subject
				mom_doc.priority = actions_list.priority
				mom_doc.description = actions_list.description
				mom_doc.save()
			frappe.msgprint(_('Task is created'), alert=True)


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

@frappe.whitelist()
def get_users(project):
	'''getting users from project
		output : get users from that project
	'''
	get_user = frappe.get_doc('Project', project)
	return get_user


