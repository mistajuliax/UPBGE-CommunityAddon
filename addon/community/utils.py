import json, sys, os

project_data = None
project_path = None

def loadProjectFile(path):
	global project_data, project_path
	try:
		with open(path) as json_file: project_data = json.load(json_file)
		project_path=os.path.dirname(path) + os.sep
		com_path = project_path + "project" + os.sep + "core" + os.sep + "com"
		sys.path.append(com_path)
		
	except Exception as e: 
		print("LOAD ERROR")
		print(str(e))
		
	env_path = os.getenv("PYTHONPATH")
	if env_path:
		if not com_path in env_path:
			os.environ["PYTHONPATH"] += os.pathsep + com_path
	else:
		os.environ["PYTHONPATH"] = com_path
		
def reloadProjectFile():
	global project_data
	if project_path==None: raise Exception("Project File not ever loaded")
	
	try:
		with open(project_path + "project.json") as json_file: project_data = json.load(json_file)
	except Exception as e: 
		print(str(e))
		
def saveProjectFile():
	with open(project_path + "project.json", 'w') as json_file:
		json_file.write(json.dumps(project_data))


def checkProjectFile():
	if project_data == None:
		path = os.path.dirname(bpy.data.filepath) + os.sep +  '../project.json'
		if os.path.isfile(path):
			loadProjectFile(path)
			if project_data == None: return False
		else: return False
	return True
		
import bpy, os
from bpy.app.handlers import persistent
		
@persistent
def checkForLaunch(dummy):
	if not checkProjectFile(): return
			
	lscene = bpy.context.screen.scene
	lobj = bpy.context.scene.objects.active
	for scene in bpy.data.scenes:
		to_make=True
		for object in scene.objects:
			if object.name.startswith("__LOOP__"): to_make=False 

		if to_make:
			
			bpy.context.screen.scene = scene
			bpy.ops.object.add()
			o=bpy.context.active_object
			o.name = '__LOOP__'
			bpy.ops.logic.sensor_add(type='ALWAYS', object=o.name)
			bpy.ops.logic.controller_add(type='PYTHON', object=o.name)
			
			sensor = o.game.sensors[-1]
			controller = o.game.controllers[-1]
			
			sensor.link(controller)
			sensor.use_pulse_true_level=True
			
			controller.mode='MODULE'
			controller.module="core.__init__.loop"
			
			o.hide=True
			o.hide_select=True
			o.select=False
			
	bpy.context.screen.scene = lscene
	bpy.context.scene.objects.active = lobj
	
	
	
