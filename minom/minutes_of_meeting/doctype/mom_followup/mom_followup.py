# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.desk.doctype.notification_settings.notification_settings import (
	is_email_notifications_enabled_for_type,
	is_notifications_enabled,
	set_seen_value,)
from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification
from email.utils import formataddr

class MOMFollowup(Document):
	def validate(self):
		mom_settings = frappe.get_doc('MOM Settings')
		notification_log = frappe.new_doc('Notification Log')
		notification_log.subject = self.name +  ' MOM Followup is created'
		notification_log.email_content = frappe.render_template(mom_settings.notification_content, {'mom_followup':self.name,'mom':self.mom})
		notification_log.document_type = self.doctype
		notification_log.document_name = self.name
		notification_log.for_user = self.supervisor
		notification_log.save(ignore_permissions=True)
