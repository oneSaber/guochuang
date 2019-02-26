from App import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from App import app
from App.route import set_route

app = create_app('testing')
manager = Manager(app)
migrate = Migrate(app, db)

# 建立路由信息
api = Api(app)



def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command("runserver", Server())

manager.add_command('db', MigrateCommand)

set_route(api)

if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0')

    manager.run()
