# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MOM(Document):

	@frappe.whitelist()
	def get_last_mom(self):
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
				frappe.msgprint('There are no MOMs for the Selected Project')
				self.review_last_mom = 0
		else:
			frappe.msgprint('Select a project to fetch it\'s last MOM')
			self.review_last_mom = 0