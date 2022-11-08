# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MOMFollowup(Document):
	def after_insert(self):
		self.send_new_mom_notif()

	def send_new_mom_notif(self):
		"""method to send a notification when a new MOM Followup is created"""
		notification_log = frappe.new_doc('Notification Log')
		notification_log.subject = 'New MOM Followup'
		notification_log.email_content = 'An MOM Followup with ID ' + self.name + ' against ' + self.mom + ' has been created.'
		notification_log.document_type = self.doctype
		notification_log.document_name = self.name
		notification_log.for_user = self.supervisor
		notification_log.save(ignore_permissions=True)
