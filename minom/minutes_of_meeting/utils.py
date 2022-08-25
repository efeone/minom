import frappe
from datetime import datetime
from frappe.utils import time_diff


@frappe.whitelist()
def send_mom_followup_notif():
    '''
        getting notification from creation of MOM Followup
        output: get notification from MOM Followup
    '''
    mom_settings = frappe.get_doc('MOM Settings')
    mom_follow_ups = frappe.db.get_all(
        'MOM Followup', fields=['name', 'date', 'status_of_followup', 'user', 'supervisor'])
    for mom_followup in mom_follow_ups:
        followup_date = mom_followup.date
        now = datetime.now()
        if (mom_followup.status_of_followup == 'Pending'):
            if (time_diff(now, followup_date).days >= 1):
                create_momf_pending_notification(mom_followup.name, mom_followup.user)
                create_momf_pending_notification(mom_followup.name, mom_followup.supervisor)
        if(mom_followup.status_of_followup != 'Cancelled'):
            mom_settings_time = mom_settings.notification_time_duration_for_mom_followup
            difference_in_hours = int(time_diff(now, followup_date).total_seconds()/3600)
            if(time_diff(now, followup_date).days >= 1  or  difference_in_hours >= mom_settings_time):
                create_momf_pending_notification(mom_followup.name, mom_followup.supervisor)
                 

@frappe.whitelist()
def create_momf_pending_notification(mom_followup_id, recepient):
    mom_followup = frappe.get_doc('MOM Followup', mom_followup_id)
    notification_log = frappe.new_doc('Notification Log')
    notification_log.type = 'Alert'
    notification_log.document_type = mom_followup.doctype
    notification_log.document_name = mom_followup.name
    notification_log.for_user = recepient
    if (mom_followup.status_of_followup == 'Pending'):
        notification_log.subject = mom_followup.name + ' is Pending'
        notification_log.email_content = 'MOM Followup with id ' + mom_followup.name + ' of ' + mom_followup.mom + ' is still Pending. Take actions to Complete it ASAP.'
    if (mom_followup.status_of_followup != 'Cancelled'):
        notification_log.subject = mom_followup.name + ' is created'
        notification_log.email_content = 'MOM Followup with id ' + mom_followup.name + ' of ' + mom_followup.mom + ' is created. Please check it!.'
    notification_log.save(ignore_permissions=True)
