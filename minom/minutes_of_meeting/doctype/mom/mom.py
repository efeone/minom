# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

from tabnanny import check
import frappe
from frappe import _
from frappe.model.document import Document


class MOM(Document):
	def validate(self):
		no_attend = True
		for attendee in self.attendees:
				if attendee.attended:
					no_attend = False
		if no_attend:
			frappe.throw('Please Check Attendance of Users')

	def on_submit(self):
		self.create_task()
		self.create_follow_up()

	def create_task(self):
		if self.project:#create task aginst subject while submitting MOM
			flag = False
			for actions_list in self.actions:
				if not actions_list.task:
					mom_doc = frappe.new_doc('Task')
					mom_doc.project = self.project
					mom_doc.subject = actions_list.subject
					mom_doc.priority = actions_list.priority
					mom_doc.description = actions_list.description
					flag = True
					mom_doc.save()
			if flag == True:
				frappe.msgprint(_('Task is created'), alert = True )
	def create_follow_up(self):
		'''
		creating MOM Follow Up while submitting MOM 
		output: new MOM Follow Up with selected tasks
		'''
		if self.follow_up_needed:
			mom_follow_up_doc = frappe.new_doc('MOM Followup')
			mom_follow_up_doc.mom = self.name
			mom_follow_up_doc.date = self.to_time
			mom_follow_up_doc.user = self.user
			mom_follow_up_doc.remarks = self.remarks
			mom_follow_up_doc.reason_for_followup = self.reason_for_followup
			if self.actions:
				for task in self.actions:
					if task.need_follow_up:
						mom_follow_up_doc.append('actions_on_followup', {
							'task': task.task,
							'subject': task.subject,
							'priority': task.priority,
							'description': task.description
							})										
			mom_follow_up_doc.save()
			frappe.msgprint(_('MOM Follow Up is created'), alert = True)

@frappe.whitelist()
def get_last_mom(project):
    '''
            getting the last mom of the selected project
            output: last mom document
    '''
    last_mom = frappe.get_last_doc('MOM', filters={'project': project}, order_by='creation desc')

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


