// Copyright (c) 2022, efeone Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('MOM', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Attendees', {
	user(frm,cdt,cdn) {
		set_filters(frm);
	}
})

let set_filters = function (frm) {
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