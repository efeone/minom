# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MOM(Document):
	@frappe.whitelist()
	def get_last_mom(self):
		'''
			getting last MOM doc of the selected project
		   	output : Attendees and Actions taken in the last meeting
		'''
		if self.project:
			check = frappe.db.exists('MOM', { 'project': self.project})
			if check:
				last_mom = frappe.get_last_doc('MOM')
				for i in last_mom.attendees:
					if(i.attended == 1):
						self.append('last_attendees', {
							'user': i.user,
							'full_name': i.full_name,
							'attended': i.attended
						})
				
				for i in last_mom.actions:
					self.append('last_actions', {
						'subject': i.subject,
						'priority': i.priority,
						'description': i.description
					})			
			else:
				frappe.msgprint(
					msg = 'There are no MOMs for the Selected Project',
					title = 'Notification'
				)
				self.review_last_mom = 0
		else:
			frappe.msgprint(
					msg = 'Select a Project to fetch it\'s last MOM',
					title = 'Notification'
				)
			self.review_last_mom = 0


@frappe.whitelist()
def get_pending_actions(project):
	'''getting uncompleted tasks
	   output : list of uncompleted tasks according to the project
	'''
	return frappe.get_all('Task', filters = {'project': project, 'status': ['!=' , 'Completed']}, fields = ['name', 'subject', 'priority', 'description'])