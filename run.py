from app import create_app, db
from app.models import Png
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Png=Png)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()