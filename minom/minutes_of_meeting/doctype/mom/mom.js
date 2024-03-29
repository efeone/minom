// Copyright (c) 2022, efeone Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.ui.form.on('MOM', {
	
	refresh: function (frm) {
		var name;
		var value;
		add_custom_button_for_attendees( frm, name = 'Uncheck All', value = 0 );
		add_custom_button_for_attendees( frm, name = 'Check All', value = 1 );
	},

	before_submit: function (frm) {
		if(!frm.doc.to_time) {
			set_to_time(frm);
		}
	},

	pending_actions: function (frm) {
		if (!frm.doc.project) {
			frappe.msgprint({
				title: __('Notification'),
				indicator: 'red',
				message: __('Select a project to show pending actions')
			});
		}
		else if (frm.doc.project) {
			show_pending_actions(frm);
		}
	},

	review_last_mom: function (frm) {
		if (frm.doc.review_last_mom) {
			if (frm.doc.project) {
				frappe.db.get_list('MOM', {
					filters: {
						project: frm.doc.project
					}
				}).then(records => {
					if (records && records.length) {
						show_last_mom_details(frm);
					}
					else {
						frappe.msgprint({
							title: __('Notification'),
							indicator: 'blue',
							message: __('The selected project has no MOMs')
						});
						frm.set_value('review_last_mom', 0);
					}
				})
			}
			else {
				frappe.msgprint({
					title: __('Notification'),
					indicator: 'blue',
					message: __('Select a Project to show it\'s last MOM details')
				});
				frm.set_value('review_last_mom', 0);
			}
		}
		else {
			frm.clear_table('last_attendees');
			frm.clear_table('last_actions');
		}
	},

	project: function (frm) {
		frm.set_df_property('pending_actions', 'hidden', 0)
		frm.clear_table('actions');
		frm.clear_table('last_attendees');
		frm.clear_table('last_actions');
		frm.set_value('review_last_mom', 0);
		frm.clear_table('attendees');
		frm.set_value( 'follow_up_needed', 0)
		frm.refresh_fields('attendees');
		frm.refresh_fields('actions');

	},

	from_time: function (frm) {
		if (frm.doc.to_time)
			calculate_time(frm);
	},

	to_time: function (frm) {
		if (frm.doc.from_time)
			calculate_time(frm);
	},
	get_user: function(frm){
		if (!frm.doc.project) {
			frappe.msgprint({
				title: __('Notification'),
				indicator: 'red',
				message: __('Select a project to proceed')
			});
		}
		else{ 
			show_users(frm);
		}
	},

	follow_up_needed: function (frm){
		if(!frm.doc.user){
			frm.set_value( 'user', frappe.session.user ); //setting value for user field as current user
		};
	}
});

frappe.ui.form.on('Actions Taken', {
	need_follow_up: function (frm, cdt, cdn) {
		mom_follow_up(frm, cdt, cdn);
	}
});

frappe.ui.form.on('Attendees', {
	user(frm, cdt, cdn) {
		let attendees;
		attendees = attendees_list(frm);
		set_filters(frm, attendees);
	},

	before_attendees_remove (frm, cdt, cdn){
		let d = locals[cdt][cdn];
		let attendees;
		attendees = attendees_list(frm);
		set_filters(frm, attendees = attendees.replace(d.user,''));
	}
})

let calculate_time = function (frm) {
	/*
		to calculate meeting duration
		output : meeting duration in minutes in meeting_duration field
	*/
	let to_time = new Date(frm.doc.to_time)
	let from_time = new Date(frm.doc.from_time)
	if (to_time < from_time) {
		frm.set_value('from_time','')
		frm.set_value('to_time','')
		frm.set_value('meeting_duration', 0)
		frappe.throw('From time should be less than To time')
	}
	let duration = ((to_time - from_time) / 1000) / 60
	frm.set_value('meeting_duration', duration)	
}

let attendees_list = function (frm){
	/* listing the users of attendees*/
	let attendees = '';
	frm.doc.attendees.forEach(function (attendee, i) {
		if(attendee.user){
				attendees += attendee.user + ', ';
		}
	});
	return attendees;
} 

let set_filters = function (frm ,attendees) {
	/*	setting filter for user field in attendees child table	*/
		frm.set_query('user', 'attendees', function (doc, cdt, cdn) {
			return {
				filters: {
					name: ['not in', attendees]
				}
			}
		});
}

let show_pending_actions = function (frm) {
	/*  to show pending tasks
		output: appending pending_actions child table with uncompleted tasks 
	*/
	var description = '';
	frappe.call({
		method: 'minom.minutes_of_meeting.doctype.mom.mom.get_pending_actions',
		args: {
			'project': frm.doc.project,
		},
		callback: function (r) {
			if(r.message && r.message.length){
				r.message.forEach(function (i) {
					if (i.description){
						description = i.description.replace(/(<([^>]+)>)/gi, '')
					}	
					frm.add_child('actions', {
						subject: i.subject,
						task: i.name,
						priority: i.priority,
						description: description
					})
				})
				frm.refresh_fields('actions');
				frm.set_df_property('pending_actions', 'hidden', 1)
			}
			else{
				frappe.msgprint({
					title: __('Notification'),
					indicator: 'orange',
					message: __(' There is no pending task ')
				});
			}	
		}
	})
}

let show_last_mom_details = function (frm) {
	/*
		to show last mom details of the selected project
		output: details of last attendees and actions taken in the last mom
	*/
	frappe.call({
		method: 'minom.minutes_of_meeting.doctype.mom.mom.get_last_mom',
		args: {
			'project': frm.doc.project,
		},
		callback: function (r) {
			let last_mom = r.message
			last_mom.attendees.forEach(function (i) {
				if (i.attended) {
					frm.add_child('last_attendees', {
						user: i.user,
						full_name: i.full_name,
						attended: i.attended
					})
				}
			})
			last_mom.actions.forEach(function (i) {
				frm.add_child('last_actions', {
					subject: i.subject,
					priority: i.priority,
					description: i.description
				})
			})
			frm.refresh_field('last_attendees');
			frm.refresh_field('last_actions');
		}
	})
}
let show_users = function (frm) {
	/*
		to show users from the project
		output: get users from the project
	*/
	frappe.call({
		method: 'minom.minutes_of_meeting.doctype.mom.mom.get_users',
		args: {
			'project': frm.doc.project,
		},
		callback: function (r) {
			let get_user = r.message
			if(get_user.users.length){
				let attendees = '';
				get_user.users.forEach(function (i) {
					frm.add_child('attendees', {
						user: i.user,
						full_name: i.full_name
					})
				attendees += i.user + ','; //adding user into attendees list
				})
				frm.refresh_field('attendees');
				set_filters(frm, attendees);
			}
			else{
				frappe.msgprint({
					title: __('Notification'),
					indicator: 'red',
					message: __(' There is no user in {0}' ,[frm.doc.project])
				});

			}
		}
	})
	frm.clear_table('attendees');
}

let set_to_time = function (frm) {
	/*
		gets the current time and set it as 'To Time'
	*/
	let time = frappe.datetime.now_datetime()
	frm.set_value('to_time', time)
}

let add_custom_button_for_attendees = function (frm, name, value ) {
	/*
	adding custom button for attendees child table
	name : name of the button
	value : boolean value
	output : checking/unchecking the checkbox attended in the attendees child table
	*/
	frm.fields_dict['attendees'].grid.add_custom_button(__( name ),
		function () {
			if (frm.doc.attendees && frm.doc.attendees.length) {
				frm.doc.attendees.forEach(function (i) {
					frappe.model.set_value(i.doctype, i.name, 'attended', value);
				})
			}
		});
	frm.fields_dict['attendees'].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn btn-xs btn-secondary grid-add-row');
} 

let mom_follow_up = function (frm, cdt, cdn){
	/*
	showing/hiding follow up section
	output: checking/unchecking follow_up_needed field
	 */
	let d = locals[cdt][cdn];
	if ( d.need_follow_up ){
		frm.set_value( 'follow_up_needed', 1);//ticking follow_up_needed
	}
	else{
		let flag = false;
		frm.doc.actions.forEach(function(i){
			if(i.need_follow_up){
				flag = true;
			}
		})
		if (flag == false){
			frm.set_value( 'follow_up_needed', 0)
		}
	}
}