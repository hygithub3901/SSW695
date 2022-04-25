from flask import Flask,render_template,g,session
def creat_app():
    app = Flask(__name__,template_folder="templates",static_folder="static",static_url_path="/backend/static")
    from . import main
    app.register_blueprint(main.main)
    app.debug = True
    return app
