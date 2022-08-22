// Copyright (c) 2022, efeone Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('MOM Followup', {
	
	onload: function (frm){
		if(!frm.doc.user){
			frm.set_value( 'user', frappe.session.user ); //setting value for user field as current user
		};
	}
});
