from flask import render_template, request, redirect, url_for, session, flash, jsonify
from application.utils.date import tdate as date, day
from application.utils.quotes import quotelist
from application.data.models import Users, Boards, Lists, Tasks, BoardMembership
from main import db, app


@app.route('/', methods=["GET", "POST"])
def login():

    if request.method == "GET":
        if "uid" in session:
            session.pop("uid", None)
        return render_template('login.html')

    if request.method == "POST":

        uname = request.form['uname']
        password = request.form['pass']
        user = Users.query.filter_by(Username=uname).first()

        if user == None:
            flash("User not found")
            return render_template('login.html')

        if user.Password == password:
            session["uid"] = user.UserID
            return redirect(url_for("myboards"))
        else:
            flash("Incorrect Username/Password")
            return render_template('login.html')


@app.route('/logout')
def logout():
    if "uid" in session:
        session.pop("uid", None)
        flash("Logged Out")
        return redirect(url_for("login"))
    else:
        flash("Already Logged Out")
        return redirect(url_for("login"))


@app.route('/myboards', methods=["GET", "POST"])
def myboards():
    if "uid" in session:
        uid = session["uid"]
        if request.method == "GET":
            my_boards = Boards.query.filter_by(CreatedBy=uid).all()
            return render_template("boards.html",
                                   my_boards=my_boards,
                                   date=date,
                                   day=day)
    else:
        return redirect(url_for("login"))


@app.route('/createboard', methods=["GET", "POST"])
def createboard():
    if "uid" in session:
        uid = session["uid"]
        if request.method == "GET":
            return render_template('createboard.html')
        if request.method == "POST":
            bname = request.form['bname']
            new_board = Boards(BoardName=bname, CreatedBy=uid)
            db.session.add(new_board)
            db.session.commit()
            return redirect(url_for("myboards"))
    else:
        return redirect(url_for("login"))


@app.route('/viewboard/<int:bid>', methods=["GET", "POST", "PUT", "DELETE"])
def viewboard(bid):
    if "uid" in session:
        uid = session["uid"]
        if request.method == "GET":
            myboard = Boards.query.filter_by(BoardID=bid).first()
            board_lists = Lists.query.filter_by(BoardID=bid).all()
            board_tasks = Tasks.query.join(Lists, Tasks.ListID == Lists.ListID).filter(Lists.BoardID == bid).all()
            board_data = {}
            for list in board_lists:
                board_data[list.ListName] = []
            for task in board_tasks:
                list_name = Lists.query.filter_by(
                    ListID=task.ListID).first().ListName
                board_data[list_name].append(task)
            return render_template("board.html",
                                   board=myboard,
                                   date=date,
                                   day=day)
        if request.method == "POST":
            board_lists = Lists.query.filter_by(BoardID=bid).all()
            board_data = []
            for board_list in board_lists:
                board_data.append({
                    "id": board_list.ListID,
                    "name": board_list.ListName,
                    "tasks": Tasks.query.filter_by(ListID=board_list.ListID).all()
                })
            return jsonify({
                "board_data": board_data,
            })
    else:
        return redirect(url_for("login"))
    
@app.route('/boardoptions/<int:bid>', methods=['GET', 'POST'])
def boardoptions(bid):
    if "uid" in session:
        myboard = Boards.query.filter_by(BoardID = bid).first()
        if request.method == "GET":
            return render_template('boardoptions.html',board=myboard)
        if request.method == "POST":
            board_name = request.form['bname']
            myboard.BoardName = board_name
            db.session.add(myboard)
            db.session.commit()
            return render_template('boardoptions.html',board=myboard)
    else:
        return redirect(url_for("login"))

@app.route('/deleteboard/<int:bid>', methods=['GET'])
def deleteboard(bid):
    if "uid" in session:
        myboard = Boards.query.filter_by(BoardID = bid).first()
        #Deleting board lists
        board_lists = Lists.query.filter_by(BoardID=bid).all()
        for list in board_lists:
            db.session.delete(list)
            db.session.commit()
        #Deleting board tasks
        board_tasks = Tasks.query.join(Lists, Tasks.ListID == Lists.ListID).filter(Lists.BoardID == bid).all()
        for task in board_tasks:
            db.session.delete(task)
            db.session.commit()
        #Deleting board
        db.session.delete(myboard)
        db.session.commit()
        flash("Board Deleted")
        return redirect(url_for("myboards"))
    else:
        return redirect(url_for("login"))


@app.route('/user', methods=["GET", "POST", "PUT", "DELETE"])
def user():

    if request.method == "GET":
        return render_template('createaccount.html')

    if request.method == "POST":
        uname = request.form['uname']
        password = request.form['pass']
        cpass = request.form['cpass']
        existing_users = Users.query.filter_by(Username=uname).all()
        if len(existing_users) > 0:
            flash("Username already taken")
            return render_template('createaccount.html')
        if password == cpass and len(uname.split(" ")) == 1:
            new_user = Users(Username=uname, Password=password)
            db.session.add(new_user)
            db.session.commit()
            session["uid"] = new_user.UserID

            new_board = Boards(BoardName="Personal Tasks",
                               CreatedBy=new_user.UserID)
            db.session.add(new_board)
            db.session.commit()

            new_list = Lists(BoardID=new_board.BoardID, ListName="To-Do")
            db.session.add(new_list)
            db.session.commit()

            flash("Welcome!")
            return redirect(url_for("myboards"))
        if password != cpass:
            flash("Passwords do not match")
            return render_template('createaccount.html')
        if len(uname.split(" ")) != 1:
            flash("Username cannot have spaces")
            return render_template('createaccount.html')


@app.route('/list', methods=["POST", "PATCH", "DELETE"])
def list():
   
        if request.method == "POST":
            list_name = request.form['list_name']
            board_id = request.form['board_id']
            myboard = Boards.query.filter_by(BoardID=board_id).first()
            new_list = Lists(BoardID=board_id, ListName=list_name)
            db.session.add(new_list)
            db.session.commit()
            return jsonify({
                "listId": new_list.ListID
            })
        if request.method == "PATCH":
            list_id = request.form['list_id']
            list_name = request.form['list_name']
            edit_list = Lists.query.filter_by(ListID=list_id).first()
            edit_list.ListName = list_name
            db.session.add(edit_list)
            db.session.commit()
            return jsonify({
                "alert": "List Edited"
            })
        if request.method == "DELETE":
            list_id = request.form['list_id']
            list_tasks = Tasks.query.filter_by(ListID=list_id).all()
            for delete_task in list_tasks:
                db.session.delete(delete_task)
                db.session.commit()
            delete_list = Lists.query.filter_by(ListID=list_id).first()
            db.session.delete(delete_list)
            db.session.commit()
            return jsonify({
                "alert": "List Deleted"
            })
    
        


@app.route('/task', methods=["POST", "PATCH", "PUT", "DELETE"])
def task():
    if "uid" in session:
        uid = session["uid"]
        if request.method == "GET":
            task_id = request.form['task_id']
            get_task = Tasks.filter_by(TaskID=task_id).first()
            return jsonify(get_task)
        if request.method == "POST":
            list_id = request.form['list_id']
            mylist = Lists.query.filter_by(ListID=list_id).first()
            task_name = request.form['task_name']
            task_description = request.form['task_description']
            task_deadline = request.form['task_deadline']
            new_task = Tasks(ListID=list_id,
                             TaskName=task_name,
                             Description=task_description,
                             Deadline=task_deadline,
                             Status=0,
                             CreatedBy=uid)
            db.session.add(new_task)
            db.session.commit()
            return jsonify({
                "alert": task_name+" Added To "+mylist.ListName
            })
        if request.method == "PATCH":
            task_id = request.form['task_id']
            task_name = request.form['task_name']
            task_description = request.form['task_description']
            task_deadline = request.form['task_deadline']
            my_task = Tasks.query.filter_by(TaskID=task_id).first()
            my_task.TaskName = task_name
            my_task.Description = task_description
            my_task.Deadline = task_deadline
            db.session.add(my_task)
            db.session.commit()
            return jsonify({
                "alert": task_name+" Edited"
            })
        if request.method == "PUT":
            task_id = request.form['task_id']
            list_id = request.form['list_id']
            my_task = Tasks.query.filter_by(TaskID=task_id).first()
            my_task.ListID = list_id
            db.session.add(my_task)
            db.session.commit()
            return jsonify({
                "alert": my_task.TaskName+" Moved"
            })
        if request.method == "DELETE":
            task_id = request.form['task_id']
            delete_task = Tasks.query.filter_by(TaskID=task_id).first()
            db.session.delete(delete_task)
            db.session.commit()
            return jsonify({
                "alert": "Task Deleted"
            })
    else:
        return redirect(url_for("login"))
