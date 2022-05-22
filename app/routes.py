from flask import render_template, request, url_for,redirect
from flaskext.mysql import MySQL
from app import app
from app.frm_entry import EntryForm

# Koneksi Database
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] ='opansan63'
app.config['MYSQL_DATABASE_DB'] = 'akhmad'
app.config['MYSQL_PORT'] = '3306'
mysql=MySQL(app)
mysql.init_app(app)
    
@app.route("/")
@app.route("/index")
def index():
    user={"username":"Burhanudin"}
    return render_template("index.html", title="Home",user=user)
    

@app.route("/frm_entry",methods=["GET","POST"])
def frm_entry():        
    # Menampung nilai yang diinput dari form
    xnilai_1=0
    xnilai_2=0
    xoperator=""
    ket=""
    hasil=""
    
    if request.method=="POST":
       details=request.form
       xnilai_1=details["nilai_1"]
       xnilai_2=details["nilai_2"]
       xoperator=details["operatornya"]       
    
       # Memproses hasil    
       if xoperator=="+":
          hasil=int(xnilai_1)+int(xnilai_2)
       elif xoperator=="-":
          hasil=int(xnilai_1)-int(xnilai_2)
       elif xoperator=="/":
          hasil=int(xnilai_1)/int(xnilai_2)
       elif xoperator=="*":
          hasil=int(xnilai_1)*int(xnilai_2)
       else:
          hasil=0
       
       # Memproses keterangan, genap atau ganjil
       if hasil % 2==0:
          ket="Genap"
       else:
          ket="Ganjil"
    
       cur= mysql.connect().cursor()
       cur.execute("insert into penjumlahan(value_1,value_2,operator,result,remark) values (%s,%s,%s,%s,%s)",((xnilai_1,xnilai_2,xoperator,hasil,ket)))
       cur.connection.commit()
       cur.close()
       
    form=EntryForm()
    return render_template("frm_entry.html",title="Nilai",form=form, 
                           ketnya=ket, hasilnya=hasil)

@app.route("/frm_tampil")
def frm_tampil():    
    cur=mysql.connect().cursor()
    cur.execute("select * from penjumlahan")
    hasilnya=cur.fetchall()    
    return render_template("tampil_data.html", title="Tampil Data",hasilnya=hasilnya,no=1)
    
@app.route("/frm_edit_data/<id>",methods=["GET","POST"])
def frm_edit_data(id):
    cur=mysql.connect().cursor()
    form=EntryForm()
    cur.execute("select * from penjumlahan where id='"+id+"'")
    hasilnya=cur.fetchall()    
    for rows in hasilnya:
        xnilai_1=rows[1]
        xnilai_2=rows[2]
        xoperator=rows[3]
        xhasil=rows[4]
        xremark=rows[5]
    
    hasil=""
    ket=""
    
    if request.method=="POST":       
       
       details=request.form
       xnilai_1=details["nilai_1"]
       xnilai_2=details["nilai_2"]
       xoperator=details["operatornya"]
       
       # Memproses hasil    
       if xoperator=="+":
          xhasil=float(xnilai_1)+float(xnilai_2)
       elif xoperator=="-":
          xhasil=float(xnilai_1)-float(xnilai_2)
       elif xoperator=="/":
          xhasil=float(xnilai_1)/float(xnilai_2)
       elif xoperator=="*":
           xhasil=float(xnilai_1)*float(xnilai_2)
       else:
           xhasil=0
        
       # Menentukan Ganjil atau Genap
       if xhasil % 2 ==0:
          xremark="Genap"
       elif xhasil % 2==1:
          xremark="Ganjil"
       else:
          xremark="Nol"   
       
       cur=mysql.connect().cursor()
       #cur.execute("update penjumlahan set value_1='"+xnilai_1+"'"+
       #            ",value_2='"+xnilai_2+"'"+",operator='"+xoperator+"'"+
       #            ",result='"+hasil+"'"+",remark='"+xremark+"'"+"where id='"+id+"'")
       
       cur.execute ("update penjumlahan set value_1=%s,value_2=%s,operator=%s,result=%s,remark=%s where id= %s",
                    ((xnilai_1,xnilai_2,xoperator,xhasil,xremark,id)))
       cur.connection.commit()
       cur.close()
    else:   
       form.nilai_1.data=xnilai_1    
       form.nilai_2.data=xnilai_2
       form.operatornya.data=xoperator   
       
    
    return render_template("frm_edit.html", title="Edit Data",znilai_1=xnilai_1,form=form,
                           ketnya=xremark,hasilnya=xhasil)    

@app.route("/hapus_data/<id>", methods=["GET","POST"])
def hapus_data(id):
    cur=mysql.connect().cursor()
    cur.execute("delete from penjumlahan where id='"+id+"'")
    cur.connection.commit()
    cur.close()    
    return redirect(url_for("frm_tampil"))
    
    