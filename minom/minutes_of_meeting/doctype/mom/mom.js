// Copyright (c) 2022, efeone Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('MOM', {
	review_pending_actions:function(frm){
		if(frm.doc.review_pending_actions && frm.doc.project){
			show_pending_actions(frm);
		}
		else{
			frm.clear_table('pending_actions');
		}
	},
	project:function(frm){
		frm.clear_table('pending_actions');
		frm.set_value('review_pending_actions', 0)
	}
});

let show_pending_actions = function (frm){
	/*  to show pending tasks
		output: appending pending_actions child table with uncompleted tasks 
	*/
	frappe.call({
		method: 'minom.minutes_of_meeting.doctype.mom.mom.get_pending_actions',
		args:{
			'project' : frm.doc.project,
		},
		callback:function(r){
			r.message.forEach(function(i){
				frm.add_child('pending_actions', {
					subject: i.subject,
					priority: i.priority,
					description: i.description.replace(/(<([^>]+)>)/gi, '')
				})
				frm.refresh_fields();
			})
		}
	})
}