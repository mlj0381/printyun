from flask import Blueprint, request, render_template
from flask_login import login_required

admin = Blueprint(
    'admin',
    __name__
)


@admin.route("/look_pdf/<media>")
@login_required
def look_media(media):
    return render_template('use_templates/viewer.html')


@admin.route("/look_picture/<string:picture>")
@login_required
def look_picture(picture):  
    return render_template('use_templates/view.html', picture=picture)


@admin.route("/data")
@login_required
def query_data():
    return render_template('use_templates/layui_orderInquiry.html')


@admin.route("/query")
@login_required
def inded_query():
    return render_template('use_templates/layui_index_query.html')


@admin.route("/people")
@login_required
def inded_people():
    return render_template('use_templates/layui_index_people.html')


@admin.route("/select")
@login_required
def inded_select():
    return render_template('use_templates/layui_index_select.html')


@admin.route('/check')
@login_required
def check():
    agent = request.environ.get('HTTP_USER_AGENT', '')
    if ('AppleWebKit' in agent and 'Mobile' in agent):
        return 'mobile'
    else:
        return 'computer'