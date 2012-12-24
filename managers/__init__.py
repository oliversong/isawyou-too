from flask.ext.script import Manager
from isy import app
manager = Manager(app)

# import and register manager commands here
from managers.post import PostManager
manager.add_command('post', PostManager())
