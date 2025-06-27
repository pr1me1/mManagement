from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.dispatch import receiver, Signal
from django.utils.timezone import now

from apps.projects.models import Tasks
from apps.users.utils import send_notification_to_email

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
		f"direct_{user.username.split('@')[0]}",
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

	send_notification_to_email(project.name, [user.email],
							   f"You have been added to project: <<{project.name}>> by {promoter}")


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
		f"direct_{user.username.split('@')[0]}",
		private_message_data
	)

	print(f"direct_{user.username.split('@')[0]}")

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

	send_notification_to_email(project.name, [user.email],
							   f"You have been kicked from project: <<{project.name}>> by {manager}")


assigned_dev_to_task = Signal()


@receiver(assigned_dev_to_task)
def handle_high_priority_task_created(sender, *args, **kwargs):
	task = kwargs.get('task')
	project = kwargs.get('project')
	devs = kwargs.get('devs')

	channel_layer = get_channel_layer()

	if task.priority == Tasks.TaskPriority.High:
		email = []

		for dev in devs:
			email.append(dev.email)
		send_notification_to_email(project.name, email,
								   f"You have been assigned as developer to the task named {task.name} in the {project.name} project.")

	private_message = {
		"type": "send_message",
		"data": {
			"message": f"You have benn assigned as developer for the task named {task.name} in the project that called {project.name}",
			"sent_at": f"{now()}"
		}
	}

	for dev in devs:
		async_to_sync(channel_layer.group_send)(
			f"direct_{dev.username.split('@')[0]}",
			private_message
		)

	project_message = {
		"type": "send_message",
		"data": {
			"message": "New developers was assigned to the task",
			"sent_at": f"{now()}"
		}
	}

	async_to_sync(channel_layer.group_send)(
		f"project_{project.uuid}",
		project_message
	)


new_task_created = Signal()


@receiver(new_task_created)
def handle_new_task_created(sender, *args, **kwargs):
	task = kwargs.get('task')
	project = kwargs.get('project')

	channel_layer = get_channel_layer()

	if task.priority == Tasks.TaskPriority.High:
		email = []

		for dev in project.tester.all():
			email.append(dev.email)
		send_notification_to_email(project.name, email,
								   f"New task {task.name} was created in the {project.name} project.")

	private_message = {
		"type": "send_message",
		"data": {
			"message": f"New task {task.name} was created in the {project.name} project.",
			"sent_at": f"{now()}"
		}
	}

	for dev in project.tester.all():
		async_to_sync(channel_layer.group_send)(
			f"direct_{dev.username.split('@')[0]}",
			private_message
		)

	project_message = {
		"type": "send_message",
		"data": {
			"message": f"New task {task.name} was created in the {project.name} project.",
			"sent_at": f"{now()}"
		}
	}

	async_to_sync(channel_layer.group_send)(
		f"project_{project.uuid}",
		project_message
	)


task_priority_changed = Signal()


@receiver(task_priority_changed)
def handle_task_priority_changed(sender, *args, **kwargs):
	task = kwargs.get('task')
	project = kwargs.get('project')

	channel_layer = get_channel_layer()

	if task.priority == Tasks.TaskPriority.High:
		email = []

		for dev in project.tester.all():
			email.append(dev.email)
		send_notification_to_email(project.name, email,
								   f"The task {task.name}'s priority was changed to high in the {project.name} project.")

	private_message = {
		"type": "send_message",
		"data": {
			"message": f"The task {task.name}'s priority was changed to high in the {project.name} project.",
			"sent_at": f"{now()}"
		}
	}

	for dev in project.tester.all():
		async_to_sync(channel_layer.group_send)(
			f"direct_{dev.username.split('@')[0]}",
			private_message
		)

	project_message = {
		"type": "send_message",
		"data": {
			"message": f"The task {task.name}'s priority was changed to high in the {project.name} project.",
			"sent_at": f"{now()}"
		}
	}

	async_to_sync(channel_layer.group_send)(
		f"project_{project.uuid}",
		project_message
	)
