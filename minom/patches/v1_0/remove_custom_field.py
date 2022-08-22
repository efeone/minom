from __future__ import unicode_literals
import frappe

def execute():
    frappe.enqueue(remove_custom_fields, queue = 'short')

def remove_custom_fields():
    '''removing custom field named supervisor from project'''
    if frappe.db.exists('Custom Field', { 'dt': 'Project', 'fieldname': 'supervisor', 'fieldtype': 'Data' }):
        custom_field_list = frappe.db.get_list( 'Custom Field', filters = { 'dt': 'Project', 'fieldname': 'supervisor', 'fieldtype': 'Data' })
        for custom_field in custom_field_list:
            custom_field_doc = frappe.get_doc( 'Custom Field', custom_field.name)
            custom_field_doc.delete()
        frappe.db.commit()