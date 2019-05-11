import boto3
import botocore
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):		# a helper function to return our instances
	instances = []

	if project:
		filters = [{'Name':'tag:Project', 'Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()

	return instances

@click.group()						# Create a main group for nesting the other groups
def cli():
	"""Shotty manages snapshots"""

@cli.group('snapshots')				# Create a group called volumes
def snapshots():
		"""Commands for snapshots"""

@snapshots.command('list')  		 # give the group the name "list"
@click.option('--project', default=None,
	help="Only snapshots for project (tag Project:<name>)")
def list_snapshots(project):
	"List EC2 snapshots"				# doc string (python feature)

	instances = filter_instances(project)

	for i in instances:
		for v in i.volumes.all():
			for s in v.snapshots.all():
				print(", ".join((
					s.id,
					v.id,
	        		i.id,
	        		s.state,
					s.progress,
					s.start_time.strftime("%c")
	        	)))
	return

@cli.group('volumes')				# Create a group called volumes
def volumes():
		"""Commands for volumes"""

@volumes.command('list')  		 # give the group the name "list"
@click.option('--project', default=None,
	help="Only volumes for project (tag Project:<name>)")
def list_volumes(project):
	"List EC2 volumes"				# doc string (python feature)

	instances = filter_instances(project)

	for i in instances:
		for v in i.volumes.all():
			print(", ".join((
				v.id,
        		i.id,
        		v.state,
        		str(v.size) + "GB",
        		v.encrypted and "Encrypted" or "Not Encrypted"
        	)))

	return

@cli.group('instances')					# Create a group called instances
def instances():
		"""Commands for instances"""

@instances.command('snapshot',   		# give the group the name "snapshot"
	help="Create snapshots of all volumes")
@click.option('--project', default=None,
	help="Only instances for project (tag Project:<name>)")
def create_snapshots(project):
	"create snapshots for EC2 instances"

	instances = filter_instances(project)

	for i in instances:
		print("Stopping {0}...".format(i.id))

		i.stop()
		i.wait_until_stopped()

		for v in i.volumes.all():
			print("   creating snaphot of {0}".format(v.id))
			v.create_snapshot(Description="Created by SnapshotAlyzer 30000")

		print("Starting {0}...".format(i.id))

		i.start()
		i.wait_until_running()

	print("Job's done!")
	return

@instances.command('list')   			# give the group the name "list"
@click.option('--project', default=None,
	help="Only instances for project (tag Project:<name>)")
def list_instances(project):
	"List EC2 instances"				# doc string (python feature)

	instances = filter_instances(project)

	for i in instances:
		tags = { t['Key']: t['Value'] for t in i.tags or [] }
		print(', '.join((
			i.id,
			i.instance_type,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name,
			tags.get('Project', '<no project>'))))
	return

@instances.command('stop')
@click.option('--project', default=None, help='Only instances for project')
def stop_instances(project):
	"Stop EC2 instances"

	instances = filter_instances(project)

	for i in instances:
		print("Stopping {0}...".format(i.id))
		try:
			i.stop()
		except botocore.exceptions.ClientError as e:
			print(" Could not stop {0}.  ".format(i.id) + str(e))
			continue		# technical not required but is good pratice

	return

@instances.command('start')
@click.option('--project', default=None, help='Only instances for project')
def start_instances(project):
	"Start EC2 instances"

	instances = filter_instances(project)

	for i in instances:
		print("Starting {0}...".format(i.id))
		try:
			i.start()
		except botocore.exceptions.ClientError as e:
			print(" Could not start {0}.  ".format(i.id) + str(e))
			continue		# technical not required but is good pratice

	return

if __name__ == '__main__':
	cli()
