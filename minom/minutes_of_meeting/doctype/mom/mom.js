// Copyright (c) 2022, efeone Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('MOM', {

	review_pending_actions:function(frm){
		if(frm.doc.review_pending_actions && !frm.doc.project){
			frappe.msgprint({
				title: __('Notification'),
				indicator: 'red',
				message: __('Select a project to show pending actions')
			});
		}
		else if(frm.doc.review_pending_actions && frm.doc.project){
			show_pending_actions(frm);
		}
		else{
			frm.clear_table('pending_actions');
		}
	},

	project:function(frm){
		frm.clear_table('pending_actions');
		frm.clear_table('last_attendees');
		frm.clear_table('last_actions');
		frm.set_value('review_pending_actions', 0);
		frm.set_value('review_last_mom', 0);
	},

	from_time:function(frm) {
		if(frm.doc.to_time)
			calculate_time(frm);
	},

	to_time: function(frm) {
		if(frm.doc.from_time) 	
			calculate_time(frm);
	},

	review_last_mom: function (frm) {
		if (frm.doc.review_last_mom == 1) {
			frm.call('get_last_mom')
		}
		else{
			frm.clear_table('last_attendees');
			frm.clear_table('last_actions');
		}
	}

});


frappe.ui.form.on('Attendees', {
	user(frm, cdt, cdn) {
		set_filters(frm);
	}
})

let calculate_time = function(frm) {
	/*
		to calculate meeting duration
		output : meeting duration in minutes in meeting_duration field
	*/
	let to_time = new Date(frm.doc.to_time)
	let from_time = new Date(frm.doc.from_time)
	let duration = ((to_time.getTime() - from_time.getTime())/1000)/60
	frm.set_value('meeting_duration', duration)
}

let set_filters = function(frm) {
	/*	setting filter for user field in attendees child table	*/
	if (frm.doc.attendees) {
		var attendees = '';
		frm.doc.attendees.forEach(function (attendee, i) {
			if (i === 0) {
				attendees += attendee.user;
			}
			else {
				attendees += ', ' + attendee.user;
			}
		});
		frm.set_query('user', 'attendees', function (doc, cdt, cdn) {
			return {
				filters: {
					name: ['not in', attendees]
				}
			}
		});
	}
}

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
					task: i.name,
					priority: i.priority,
					description: i.description.replace(/(<([^>]+)>)/gi, '')
				})
				frm.refresh_fields();
			})
		}
	})
}