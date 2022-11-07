import frappe
from datetime import datetime
from frappe.utils import time_diff
from frappe.model.mapper import get_mapped_doc
from frappe.email.doctype.notification.notification import get_context


@frappe.whitelist()
def send_mom_followup_notif():
    '''
        getting notification from creation of MOM Followup
        output: get notification from MOM Followup
    '''
    mom_settings = frappe.get_doc('MOM Settings')
    mom_follow_ups = frappe.db.get_list('MOM Followup', fields=['name','date'], filters={'status_of_followup':'Pending'})
    for mom_followup in mom_follow_ups:
        now = datetime.now()
        diff_in_time = time_diff(now, mom_followup.date).days
        notif_interval = mom_settings.notification_interval or 1
        if (diff_in_time >= notif_interval):
            mom_followup_doc = frappe.get_doc('MOM Followup',mom_followup.name)
            subject = mom_followup_doc.name + ' is Pending'
            if mom_settings.notification_content_pending_momf:
                context = get_context(mom_followup_doc)
                content = frappe.render_template(mom_settings.notification_content_pending_momf, context)
            else:
                content = 'MOM Followup with id ' + mom_followup_doc.name + ' of ' + mom_followup_doc.mom + ' is still Pending. Take actions to Complete it ASAP.'
            create_notification_log(
                mom_followup_doc,
                mom_followup_doc.user,
                subject,
                content
                )
            create_notification_log(
                mom_followup_doc,
                mom_followup_doc.supervisor,
                subject,
                content
                )


def create_notification_log(doc, recipient, subject, content):
    ''' method is used to create notification log
        args:
            doc: document object
            recipient: notification receiving user
            subject: subject of notification log '''
    notification_log = frappe.new_doc('Notification Log')
    notification_log.type = 'Mention'
    notification_log.document_type = doc.doctype
    notification_log.document_name = doc.name
    notification_log.for_user = recipient
    notification_log.subject = subject
    notification_log.email_content = content
    notification_log.save(ignore_permissions = True)

@frappe.whitelist()
def create_mom(source_name, target_doc = None):
	doc = get_mapped_doc(
		'Event',
		source_name,
		{
			'Event': {
				'doctype': 'MOM',
				'field_map': [
					['starts_on', 'from_time'],
                    ['ends_on', 'to_time'],
                    ['subject', 'discussion_topic']
				],
			}
		}
	)
	return doc

@frappe.whitelist()
def get_mom_linked_with_event(doc, method):
    """ method used to get mom name and set it to __onload """
    if frappe.db.exists('MOM', {'event': doc.name}):
        mom = frappe.db.get_value("MOM", {"event": doc.name}, "name") or ""
        doc.set_onload("mom", mom)
