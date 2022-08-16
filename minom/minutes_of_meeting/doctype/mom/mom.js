// Copyright (c) 2022, efeone Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('MOM', {

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
		else
			frm.clear_table('last_attendees')
			frm.clear_table('last_actions')
	}
});

frappe.ui.form.on('Attendees', {
	user(frm, cdt, cdn) {
		set_filters(frm);
	}
})

let calculate_time = function(frm) {
	let to_time = new Date(frm.doc.to_time)
	let from_time = new Date(frm.doc.from_time)
	let duration = ((to_time.getTime() - from_time.getTime())/1000)/60
	frm.set_value('meeting_duration', duration)
}

let set_filters = function(frm) {
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