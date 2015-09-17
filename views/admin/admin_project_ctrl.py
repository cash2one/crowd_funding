#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-16 09:01:25
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-16 10:56:59

from flask import request,render_template,Blueprint
from services import project_service
admin_project_ctrl=Blueprint('admin_project_ctrl',__name__)
@admin_project_ctrl.route('/project/list',methods=['GET','POST'])
def project_list():
    page=request.args.get('page',1)
    page_size=request.args.get('page_size',20)
    title=None
    if request.method=='POST':
        title=request.forms.get('title',None)
    (projects,paginate)=project_service.query_projects_by_page(title)
    return render_template('admin/project/project_list.html',projects=projects,paginate=paginate)


