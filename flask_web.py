#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-18 10:04:17
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-11-18 17:50:38
# -*- coding: utf-8 -*-
from flask import Flask,url_for,Response,request,session,redirect
from database.models import db
from views.user_ctrl import user_ctrl
from views.api.user_api import user_api
from views.api.category_api import category_api
from views.api.project_api import project_api
from views.api.payback_api import payback_api
from views.api.common_api import common_api
from views.api.artist_api import artist_api
from views.api.order_api import order_api
from views.api.beecloud_api import  beecloud_api
from views.admin.admin_ctrl import admin_ctrl
from views.app.project_ctrl import project_ctrl
from views.app.common import common_ctrl
from views.admin.admin_project_ctrl import admin_project_ctrl
from views.admin.admin_user_ctrl import admin_user_ctrl
from logging.handlers import RotatingFileHandler
from logging import Formatter
from flask_assets import Environment, Bundle
from flask_admin import Admin
from views.admin.admin_view_models import UserModelView,ProjectModelView,TokenModelView,PaybackModelView,ArtistProfileModelView,ArtCategoryModelView,ArtistPhotoModelView,ActivityNoticeModelView,ProjectPostModelView,ArtistPostModelView,OrderModelView,NewsModelView
import logging
from flask_babel import Babel
from flask_admin.contrib.fileadmin import FileAdmin
from views.admin import admin_view_models
from views.common.upload_ctrl import upload_ctrl

from views.app.index_ctrl import  index_ctrl
import os.path as op

from views.home.home_ctrl import home_ctrl
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
log_roll_handler=RotatingFileHandler('roll.log',maxBytes=1024*1000*10)
log_roll_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
))
app = Flask(__name__)
# babel = Babel(app)
# @babel.localeselector
# def get_locale():
#    override = request.args.get('lang')
#    if override:
#        session['lang'] = override
#    return session.get('lang', 'zh_CN')
db.init_app(app)
app.config.from_pyfile('app.cfg')
log_roll_handler.setLevel(logging.DEBUG)
app.logger.addHandler(log_roll_handler)
app.register_blueprint(user_ctrl)
app.register_blueprint(admin_ctrl,url_prefix='/admin2')
app.register_blueprint(admin_project_ctrl,url_prefix='/admin2')
app.register_blueprint(admin_user_ctrl,url_prefix='/admin2')
app.register_blueprint(user_api,url_prefix='/api')
app.register_blueprint(category_api,url_prefix='/api')
app.register_blueprint(project_api,url_prefix="/api")
app.register_blueprint(artist_api,url_prefix="/api")
app.register_blueprint(project_ctrl,url_prefix='/project')
app.register_blueprint(common_ctrl, url_prefix='/comm')
app.register_blueprint(payback_api,url_prefix='/api')
app.register_blueprint(common_api,url_prefix='/api')
app.register_blueprint(order_api,url_prefix="/api")
app.register_blueprint(beecloud_api,url_prefix="/api")

app.register_blueprint(index_ctrl)

app.register_blueprint(upload_ctrl)

app.register_blueprint(home_ctrl)
#define static res.
assets = Environment(app)
css_from_less = Bundle(
    'less/style.less',
    filters = 'less',
    output = 'css/style.css',
    depends="less/site/*.less"
)
css_all = Bundle(
    'vendor/simditor/styles/simditor.css'
)
js_all = Bundle(
    'js/common.js',
    'js/dropdown.js',
    'js/limitTextArea.js',
    'js/projects_list.js',
)
js_publish_project = Bundle(
    'vendor/simditor/scripts/module.min.js',
    'vendor/simditor/scripts/hotkeys.min.js',
    'vendor/simditor/scripts/uploader.min.js',
    'vendor/simditor/scripts/simditor.min.js',
    'js/project_publish.js',
    'js/jquery.form.js'
)

css_index=Bundle(
    'css/index.css'
)
home_css_index=Bundle(
    'home/index.css'
)
assets.register('css_from_less', css_from_less)
assets.register('css_all', css_all)
assets.register('js_all', js_all)
assets.register('js_publish_project', js_publish_project)
assets.register("css_index",css_index)
assets.register("home_css_index",home_css_index)
app.config['ASSETS_DEBUG'] = True
#assets end
@app.route("/")
def index():
    return redirect("/project/list")
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint)
            links.append((url, rule.endpoint))
    result=''
    for link in links:
        result=(result+link[0]+'&nbsp : &nbsp'+link[1]+'<br>')
    return Response(result)
path = op.join(op.dirname(__file__), 'static/upload')
admin_view_models.file_path=path
admin = Admin(app, name=u'乐事后台',template_mode='bootstrap3')
admin.add_view(UserModelView(db.session))
admin.add_view(ArtistProfileModelView(db.session))
#admin.add_view(CategoryModelView(db.session))
admin.add_view(ProjectModelView(db.session))
admin.add_view(PaybackModelView(db.session))
admin.add_view(TokenModelView(db.session))
admin.add_view(ArtCategoryModelView())
admin.add_view(ArtistPhotoModelView())
admin.add_view(ActivityNoticeModelView())
admin.add_view(ProjectPostModelView())
admin.add_view(ArtistPostModelView())
admin.add_view(OrderModelView())
admin.add_view(NewsModelView())
admin.add_view(FileAdmin(unicode(path), '/static/upload/', name=u'文件管理'))


@app.before_request
def app_before_request():
    if request.path.startswith('/admin/') and request.path!='/admin2/do_login' and session.get('admin_id',None) is None:
        return redirect('/admin2/login')


def create_app(config=None):
    app = Flask(__name__)
    db.init_app(app)
    app.config.from_pyfile('app.cfg')
    # configure your app...
    return app
if __name__ == '__main__':
    import sys
    reload(sys) 
    sys.setdefaultencoding( "utf-8" )  
    #sys.setrecursionlimit(300) 
    from os import environ
    ##db.create_all(bind='__all__', app=app)
    app.debug=True
    app.run(host='0.0.0.0',port=environ.get("PORT", 5000),processes=1)
    #app.run('0.0.0.0:5050')
