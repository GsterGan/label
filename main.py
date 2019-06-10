import os
from flask import Flask,render_template,jsonify,request,redirect,url_for,session,abort,flash
from werkzeug.utils import secure_filename
from datetime import timedelta
import hashlib
from model import sql

SECRET_KEY = 'development key'
USERNAME = 'aaa'
walk = os.walk(r"E:\毕设\虹膜分析\label\static\images\label")
file_list = []
for root,dirs,files in walk:
    for file in files:
        file_list.append(file.replace(".jpg",""))
pic_location = 0

def write_label(dat):
    ringId = dat[0]
    x1 = str(dat[1])
    y1 = str(dat[2])
    h = str(dat[3])
    w = str(dat[4])
    data = ringId + '.jpg ' + x1 + ' '+ y1 + ' ' + h + ' ' + w + '\n'
    f = open('static/images/label/location.txt','a')
    f.write(data)
    f.close()

app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)   
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=1) 
app.config.from_object(__name__)

def isNameExist(username):
    a = sql.findName(username)
    if len(a):
        return True
    else:
        return False 

def isCheckCode(checkcode):
    if checkcode == '20190604':
        return True
    else:
        return False

@app.route('/')
def gotoIndex():
    return render_template('pages/index.html')

@app.route('/login',methods=['GET','POST'])
def gotoLogin():
    error = None
    if request.method == 'POST':
        username = request.form['username'] 
        pwd_temp = hashlib.md5(request.form['password'].encode("utf-8"))
        password = pwd_temp.hexdigest()
        if not isNameExist(username):
            error = '你这个用户不存在'
            session['logged_in'] = False
            return render_template('pages/login.html/',error=error)
        elif password != sql.findPassword(username)[0][0]:
            error = '你丫的密码错了'
            session['logged_in'] = False
            return render_template('pages/login.html/',error=error)
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('gotoLabel'))
    else:
        if not session.get('logged_in'):
            return render_template('pages/login.html/',error=error)
        else:
            return redirect(url_for('gotoLabel'))


def setNewUser(username, password):
    sql.addUser(username,password)

@app.route('/registe',methods=['GET','POST'])
def gotoRegite():
    error = None
    if request.method == 'GET': 
        return render_template('pages/registe.html',error = error) 
    if request.method == 'POST':  
        username = request.form['username'] 
        pwd_temp = hashlib.md5(request.form['password'].encode("utf-8"))
        password = pwd_temp.hexdigest()
        checkcode = request.form.get('checkcode') 
        if isNameExist(username):
            error =  '此用户名已存在' 
            return render_template('pages/registe.html',error = error) 
        elif not isCheckCode(checkcode):
            error = '邀请码错误' 
            return render_template('pages/registe.html',error = error) 
        else: 
            setNewUser(username, password)
            flash('----------------------------------------------------------------')
            return redirect(url_for('gotoLogin'))

@app.route('/quit')
def quit():
    session.pop('logged_in', None)
    flash('You were logged out')
    return render_template('pages/index.html')

@app.route('/label',methods=['GET','POST'])
def gotoLabel():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        old_dat = []    
        old_dat.append(request.form.get('ringId')) 
        old_dat.append(request.form.get('x1'))     
        old_dat.append(request.form.get('y1'))     
        old_dat.append(request.form.get('h'))     
        old_dat.append(request.form.get('w')) 
        print(old_dat,'------------------------------')
        write_label(old_dat)
        global pic_location
        print(file_list[pic_location])
        data,pic_location = file_list[pic_location],pic_location
        pic_location += 1
        #print(i,file_list[i])
        #print(data)
        #logOpration(i)
        print(pic_location)
        return render_template('pages/label.html',img_src='/static/images/label/%s.jpg'%file_list[pic_location],ringId='%s'%file_list[pic_location],sex='%s'%data[1],featherColor='%s'%data[2],iris='%s'%data[3],url='%s'%data[4])
    return render_template('pages/label.html',img_src='/static/images/label/16.jpg',ringId='14-03391',sex='',featherColor='',bloodline='',iris='',url='')

@app.route('/compare', methods = ['GET','POST'])
def gotoCompare():
    print(sql.findAll())
    if request.method == 'POST':
        f1 = request.files['file1']
        f2 = request.files['file2']
        upimg1 = "static\\images\\upload\\"+f1.filename
        upimg2 = "static\\images\\upload\\"+f2.filename
        upload_path1 = basedir + upimg1 #
        upload_path2 = basedir + upimg2 #
        f1.save(upload_path1)
        f2.save(upload_path2)
        #loss = modelLoad.get_out(upimg1,upimg2)
        #xinxi = get_xinxi(loss)
        loss = '他们的差距为：'+str(loss)
        return render_template('pages/compare.html/',img1 = upimg1,img2 = upimg2,xinxi = loss,result = xinxi)
    return render_template('pages/compare.html/',img1 = '/static/images/background.png',img2 = '/static/images/background.png')

@app.route('/find', methods = ['GET','POST'])
def gotoFind():
    if request.method == 'POST':
        f = request.files['file']
        upimg = "static\\images\\upload\\"+f.filename
        upload_path = basedir + upimg #
        f.save(upload_path)
        #img = search.get_imgs(upimg)
        #a,b,c,d = index.get_four(upimg)
        a,b,c,d = a.replace('pkl','jpg'),b.replace('pkl','jpg'),c.replace('pkl','jpg'),d.replace('pkl','jpg'),
        print(a,b,c,d)
        return render_template('pages/find.html/',img0 = upimg,img1=a,img2=b,img3=c,img4=d)
    return render_template('pages/find.html/',img0 = '/static/images/background.png',img1="/static/images/defultEye.png",img2="/static/images/defultEye.png",img3="/static/images/defultEye.png",img4="/static/images/defultEye.png")

def docate(cate1):
    cate1 = cate1[::-1]
    cate1 = cate1[4:cate1.find('/')]
    cate1 = cate1[::-1]
    return cate1
    
app.add_template_filter(docate,"cate")

@app.errorhandler(401)
def uerNotLogin(e):
    return '你还没有登录，请登录后进入此页面'
 

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True)
 
