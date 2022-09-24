frappe.ui.form.on('Event', {

  refresh:function(frm){
    if (frm.doc.__onload ) {
      if (frm.doc.__onload.mom) { // checking __onload contains name of mom
        frm.add_custom_button('Show MOM', () => {
            frappe.set_route('Form', 'MOM', frm.doc.__onload.mom);
        })
      }
    }
    else {
      frm.add_custom_button('Create MOM', () => {
          frappe.model.open_mapped_doc({
  					method: 'minom.minutes_of_meeting.utils.create_mom',
  					frm: cur_frm,
  				})
      })
    }
  }

})
