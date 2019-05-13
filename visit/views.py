from visit import *



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        kerberos = request.form['kerberos']
        student_id = request.form['student_id']
        dorm = request.form['dorm']

        insert_into_database(firstname, lastname, kerberos, student_id, dorm)

        # Putting yourself on your guest list
        host_kerb = request.form['kerberos']
        host = check_login(host_kerb)[0]
        insert_into_connections(host, host)
        #
        return redirect(url_for('index'))


    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = check_login(request.form['kerberos'])
        if(str(user[4]) == request.form['student_id']):
            session['logged_in'] = True
            session['kerberos'] = request.form['kerberos']
            return redirect(url_for('dashboard'))
        else:
            return 'Incorrect information.'

    return render_template('login.html')
@app.route('/dashboard')
@login_required
def dashboard():
    guest_list = []
    your_kerberos = session['kerberos']
    get_guests_of_user(your_kerberos, guest_list)




    return render_template('dashboard.html', guest_list=guest_list)

@app.route('/guest-list-entry', methods=['GET', 'POST'])
@login_required
def guest_list_entry():
    your_kerberos = session['kerberos']

    if request.method == 'POST':
        friend_kerberos = request.form['friend_kerberos']
        you = check_login(your_kerberos)[0]
        them = check_login(friend_kerberos)[0]
        insert_into_connections(you, them)

        return redirect(url_for('dashboard'))

    return render_template('guest_entry.html')

@app.route('/edit-information', methods=['GET', 'POST'])
@login_required
def edit_information():

    your_kerberos = session['kerberos']


    if request.method == 'POST':
        dorm = request.form['dorm']

        update_dorm_info(your_kerberos, dorm)

        return redirect(url_for('dashboard'))




    you = fetch_user_by_kerb(your_kerberos)


    dorm = you[5]

    return render_template('edit_information.html', dorm=dorm)



@app.route('/access', methods=['GET', 'POST'])
def access():


    if request.method == 'POST':

        studentID = request.form.get('studentID')
        dorm = request.form.get('dorm')



        requesting_student = fetch_user(studentID)

        insert_into_attempts(studentID, requesting_student[1], requesting_student[2], student[3])
        if not requesting_student:
            return 'Not a valid student in the database'
        requesting_student_id = requesting_student[0]
        conns = []
        get_conns_of_user(requesting_student_id, conns)
        granted_access = False
        for c in conns:
            if fetch_user_by_id(c[1])[5] == dorm:
                granted_access = True


        return str(granted_access)


@app.route('/delete/<guest_id>', methods=['GET', 'POST'])
def delete_guest(guest_id):
    your_kerberos = session['kerberos']
    user = fetch_user_by_kerb(your_kerberos)
    your_id = user[0]

    remove_a_guest(your_id, guest_id)

    return redirect(url_for('dashboard'))




@app.route('/guest-worker', methods=['GET', 'POST'])
def guest_worker():

    return render_template('guest_worker.html')





@app.route('/all')
def get_all():
    studs = []
    lookup_database(studs)
    return str(studs)

@app.route('/all-connections')
def get_all_connections():
    conns = []
    lookup_connections(conns)
    return str(conns)
