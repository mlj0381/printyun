from flask import Blueprint, render_template
from flask_login import current_user
import os
from app.forms import Print1
import datetime

test = Blueprint('test', __name__)


@test.route('/select_pay', methods=['GET', 'POST'])
def test_select():
    form = Print1()
    datetimes = datetime.datetime.now()
    now = str(datetimes.year) + "-" + str(datetimes.month) + "-" + str(datetimes.day) + "_" + str(
        datetimes.hour) + "-" + str(datetimes.minute) + "-" + str(datetimes.second)
    if form.validate_on_submit():
        print_file = form.print_file.data
        new_filename = str(current_user.Tel_Number) + '_' + now + str(print_file.filename)
        basepath = os.path.abspath(os.path.dirname(__file__))  # 当前文件所在目录
        parentdir = os.path.dirname(basepath)  # 父级目录
        upload_path = os.path.join(parentdir, 'static/Upload_Files', new_filename)
        # upload_path = os.path.join(basepath, 'uploads', random_filename(print_file.filename))
        print_file.save(upload_path)
    return render_template('select1.html', now=now, form=form)
