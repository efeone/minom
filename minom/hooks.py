from . import __version__ as app_version

app_name = "minom"
app_title = "MINutes Of Meeting"
app_publisher = "efeone Pvt. Ltd."
app_description = "Frappe App to Enhancement of Events and Utility to mark Minutes of Meeting and it\'s follow-up"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@efeone.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/minom/css/minom.css"
# app_include_js = "/assets/minom/js/minom.js"

# include js, css files in header of web template
# web_include_css = "/assets/minom/css/minom.css"
# web_include_js = "/assets/minom/js/minom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "minom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Event" : "public/js/event.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "minom.install.before_install"
# after_install = "minom.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "minom.uninstall.before_uninstall"
# after_uninstall = "minom.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "minom.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Event": {
		"onload": "minom.minutes_of_meeting.utils.get_mom_linked_with_event"
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"minom.tasks.all"
	# ],
	# "daily": [
	# 	"minom.tasks.daily"
	# ],
	# "hourly": [
	# 	"minom.minutes_of_meeting.utils.send_mom_followup_notif"
	# ]
	# "weekly": [
	# 	"minom.tasks.weekly"
	# ],
	# "monthly": [
	# 	"minom.tasks.monthly"
	# ]
	"cron": {
        "0 8 * * *": [
            "minom.minutes_of_meeting.utils.send_mom_followup_notif"
        ]
    }
}

fixtures = ["MOM Settings"]

# Testing
# -------

# before_tests = "minom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "minom.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "minom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"minom.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
