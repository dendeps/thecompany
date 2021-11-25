from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('departments', __name__)


@bp.route('/departments')
def index():
    db = get_db()
    departments = db.execute(
        'SELECT p.id, department'
        ' FROM department p '
        ' ORDER BY department DESC'
    ).fetchall()
    return render_template('departments/index.html', departments=departments)


@bp.route('/department', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        department = request.form['department']
        error = None

        if not department:
            error = 'Department is required.'

        if error is None:
            try:
                db = get_db()
                db.execute(
                    'INSERT INTO department (department)'
                    ' VALUES (?)',
                    (department,)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Department {department} already exists."
            else:
                return redirect(url_for('departments.index'))
        flash(error)

    return render_template('departments/create.html')


def get_dept(id):
    dept = get_db().execute(
        'SELECT p.id, department'
        ' FROM department d JOIN user u ON d.department = u.department'
        ' WHERE d.id = ?',
        (id,)
    ).fetchone()

    if dept is None:
        abort(404, f"Department id {id} doesn't exist.")

    return dept


@bp.route('/departments/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    dept = get_dept(id)

    if request.method == 'POST':
        title = request.form['title']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE department SET title = ?'
                ' WHERE id = ?',
                (title, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', dept=dept)


@bp.route('/departments/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    get_dept(id)
    db = get_db()
    db.execute('DELETE FROM department WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('department.index'))
