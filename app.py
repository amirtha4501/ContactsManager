from flask import Flask, render_template, request, redirect
import jinja2
import json
import uuid

app = Flask(__name__)

@app.route('/allcontacts')
def allcontacts():
    with open('contact.json', 'r') as f:
        data = f.read()
    mylist = json.loads(data)
    return render_template('allcontacts.html', contacts=mylist)

@app.route('/newcontact')
def newcontact():
    return render_template('newcontacts.html')

@app.route('/viewcontact/<contact_id>')
def show(contact_id):
    with open('contact.json','r') as fr:
        contacts = json.loads(fr.read())

    mycontact = None
    for contact in contacts:
        if contact['id'] == contact_id:
            mycontact = contact
            break
    # print(mycontact)
    return render_template('viewcontact.html', contact=mycontact)

@app.route('/edit/<contact_id>')
def editit(contact_id):
    with open('contact.json','r') as fe:
        contacts = json.loads(fe.read())
    mycontact = None
    for contact in contacts:
        if contact['id'] == contact_id:
            mycontact = contact
            break
    return render_template('editcontact.html',contact=mycontact)

@app.route('/editcontact/<contact_id>')
def change(contact_id):
    with open('contact.json','r') as fe:
        contacts = json.loads(fe.read())
    index = None
    for i,contact in enumerate(contacts):
        if contact['id']==contact_id:
            index = i
            break
    contacts[index].update(
        {
            'fname' : request.args.get('fname'),
            'lname' : request.args.get('lname'),
            'phone' : request.args.get('phone'),
            'mail' : request.args.get('mail')
        }
    )
    with open('contact.json','w') as fw:
        fw.write(json.dumps(contacts,indent=4))
    return redirect('/viewcontact/{}'.format(contact_id))


@app.route('/create')
def createit():
    with open('contact.json', 'r') as f:
        data = json.loads(f.read())
    a = {
        'fname': request.args.get('fname'),
        'lname': request.args.get('lname'),
        'phone': request.args.get('phone'),
        'mail': request.args.get('mail'),
        'id' : str(uuid.uuid4())
        }
    data.append(dict(a))

    with open('contact.json', 'w') as f:
        f.write(json.dumps(data, indent=4))
    return redirect('/allcontacts')

    # return 'creating'

@app.route('/delete/<contact_id>')
def deleteit(contact_id):
    with open('contact.json','r') as fd:
        contacts = json.loads(fd.read())
    index = None
    for i, contact in enumerate(contacts):
        if contact['id'] == contact_id:
            index = i
            break
    contacts.pop(index)
    with open('contact.json','w') as fd:
        fd.write(json.dumps(contacts,indent=4))
    return redirect('/allcontacts')

app.run(host='0.0.0.0', port=8000, debug=True)

