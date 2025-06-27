from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.dispatch import receiver, Signal

added_to_project = Signal()


@receiver(added_to_project)
def handle_be_added_to_project(sender, *args, **kwargs):
	user = kwargs.get("user")
	promoter = kwargs.get('promoter')
	project = kwargs.get("project")
	role = kwargs.get("role")

	channel_layer = get_channel_layer()

	private_message_data = {
		"type": "send_message_from_django",
		"data": {
			"message": f"You have been added to project: <<{project.name}>> by {promoter}",
			"send_at": f"{project.created_at}"
		}
	}

	async_to_sync(channel_layer.group_send)(
		f"direct_{user.username}",
		private_message_data
	)

	project_message_data = {
		"type": "send_message_from_django",
		"data": {
			"message": f"{promoter} added {user.username} to the project <<{project.name}>> as {role}",
			"send_at": f"{project.created_at}"
		}
	}

	async_to_sync(channel_layer.group_send)(
		f"project_{project.uuid}",
		project_message_data
	)


kicked_from_project = Signal()


@receiver(kicked_from_project)
def handle_be_kicked_from_project(sender, *args, **kwargs):
	user = kwargs.get("user")
	manager = kwargs.get('manager')
	project = kwargs.get("project")

	channel_layer = get_channel_layer()

	private_message_data = {
		"type": "send_message_from_django",
		"data": {
			"message": f"You have been kicked from project: <<{project.name}>> by {manager}",
			"send_at": f"{project.created_at}"
		}
	}

	async_to_sync(channel_layer.group_send)(
		f"direct_{user.username}",
		private_message_data
	)

	project_message_data = {
		"type": "send_message_from_django",
		"data": {
			"message": f"{manager} kicked {user.username} from the project <<{project.name}>> ",
			"send_at": f"{project.created_at}"
		}
	}

	async_to_sync(channel_layer.group_send)(
		f"project_{project.uuid}",
		project_message_data
	)


high_priority_task_created = Signal()


@receiver(high_priority_task_created)
def handle_high_priority_task_created(sender, *args, **kwargs):
	task = kwargs.get('task')
	project = kwargs.get('project')

	channel= get_channel_layer()



