from flask import Flask, render_template, request,redirect, session, flash, send_from_directory
from flask_bootstrap import Bootstrap
from flask_bootstrap.nav import *
from prueba import Nav
from prueba.elements import *
from dominate.tags import img
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from flask_paginate import Pagination, get_page_args
from bd import conn, sch
import pyodbc
import urllib.parse 
import sys
import os
# import win32api
# import win32security
from cryptography.fernet import Fernet
from functools import wraps
from passlib.hash import sha256_crypt
import json
import requests

from models.reportconfig import ReportConfig
from models.embedtoken import EmbedToken
from models.embedconfig import EmbedConfig
from models.embedtokenrequestbody import EmbedTokenRequestBody
from flask import current_app as abort
import msal

from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
import pandas as pd
import re
import time
from inicio import all_workshop2,all_reports, get_embed_params_for_single_report



# initialization
# here we define our menu items
topbar = Navbar('top')


with conn.cursor() as cursor:
                cursor.execute("SELECT DISTINCT TAB_GROUP FROM "+sch+".META_CRUD_TABLES where Tab_viewHidden = 0 ")
                camps = cursor.fetchall()
                for i in camps:
                  
                    lista=[]
                    las=cursor.execute("select TAB_LABEL from meta.META_CRUD_TABLES where  Tab_viewHidden = 0 and TAB_GROUP = ? order by tab_id", i).fetchall()
                    for txt in las:
                        
                        lista.append(View(f'{txt[0]}','index', idLinea=0,nomTaula=f'{txt[0]}',campFiltre=None,valorFiltre=None))
                    
                    if len(lista)==1:
                        topbar.items.append(Subgroup(i[0],lista[0]))
                    elif len(lista)==2:
                        topbar.items.append(Subgroup(i[0],lista[0],lista[1]))
                    elif len(lista)==3:
                        topbar.items.append(Subgroup(i[0],lista[0],lista[1],lista[2]))
                    elif len(lista)==4:
                        topbar.items.append(Subgroup(i[0],lista[0],lista[1],lista[2],lista[3]))
                    elif len(lista)==5:
                        topbar.items.append(Subgroup(i[0],lista[0],lista[1],lista[2],lista[3],lista[4]))
                    elif len(lista)==6:
                        topbar.items.append(Subgroup(i[0],lista[0],lista[1],lista[2],lista[3],lista[4],lista[5]))            
                    elif len(lista)==7:
                        topbar.items.append(Subgroup(i[0],lista[0],lista[1],lista[2],lista[3],lista[4],lista[5],lista[6]))     
                    elif len(lista)==8:
                        topbar.items.append(Subgroup(i[0],lista[0],lista[1],lista[2],lista[3],lista[4],lista[5],lista[6],lista[7]))     
                    elif len(lista)==9:
                        topbar.items.append(Subgroup(i[0],lista[0],lista[1],lista[2],lista[3],lista[4],lista[5],lista[6],lista[7],lista[8]))      
                    

# registers the "top" menubar

nav = Nav()
nav.register_element('top', topbar)
key = b'MTjfzcbVFZt_mCOGYjKo_lGMAeP_Un7-znPgsK_4pJI='
app = Flask(__name__)
app.secret_key = 'sdfzbabrq35d4fv4AEWV$w451*/*ew/rbv'
app.config.from_object('config.BaseConfig')
app.config['UPLOAD_FOLDER'] = "./input"
nav.init_app(app)

def get_registers(cursor,offset=0, per_page=50):
    
    for x in range(offset):
        retornar = cursor.fetchmany(per_page)
    return retornar






def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('login'))
    return wrap





@app.route('/powerbi',methods=['POST', 'GET'])
@is_logged_in
def index2():

  
    try:
        a=request.form['work']
        c=request.form['report']
        
    except:
        a=None
        c=None
     
    #una prueba
    
    value = all_workshop2(session['id'])  
    value2 = all_reports(app,session['id'], value)
    with conn.cursor() as cursor:
                result=cursor.execute("select User_PBI_Edit, User_PBI_Admin, User_PBI_Table_filter, User_PBI_Col_filter, User_PBI_Value_filter from dbo.USERS_POWERBI where User_PBI_ID_Users =?", session['id'])
                data = cursor.fetchone()
 
                cursor.execute("SELECT TAB_LABEL   FROM "+sch+".META_CRUD_TABLES where TAB_viewHidden = 0 order by tab_id")
                camps = cursor.fetchall()
                # print(camps)
                for camp in camps:
                    idTaula = camp[0]
                    break
                print(idTaula)

                if data[1] == 0:
                    value3=[]
                    value3.append(value2[0])
                    value2=value3
                    
                else:
                    pass
                
            

                return render_template('index2.html', value=value, b=a, value2=value2, c=c, usuario=session['username'], edit2=str(data[0]), admin=str(data[1]), idTaula=str(idTaula), filtertaula = str(data[2]), filterCol = str(data[3]), filterValue = str(data[4]))


@app.route('/getembedinfo', methods=['GET','POST'])
@is_logged_in
def get_embed_info():
  
    '''Returns report embed configuration'''
    # config_result = Utils.check_config(app)
   
    a=request.form['work']
    c=request.form['report']
    # if config_result is not None:
    #     return json.dumps({'errorMsg': config_result}), 500

    try:
      
        embed_info = get_embed_params_for_single_report(app,session['id'],a, c)
        return embed_info
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500

@app.route('/favicon.ico', methods=['GET'])
@is_logged_in
def getfavicon():
    '''Returns path of the favicon to be rendered'''

    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<string:nomTaula>/<int:idLinea>/<string:campFiltre>/<string:valorFiltre>', methods=['POST', 'GET'])
@app.route('/<string:nomTaula>/<int:idLinea>', methods=['POST', 'GET'])
@is_logged_in
def index(nomTaula,idLinea,campFiltre = 'SenseFiltre',valorFiltre=None):
    username = request.environ.get('REMOTE_USER')
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    schema = 'dbo'
    errors = 0
    per_page = 30
    if campFiltre != 'SenseFiltre':
        try:
            string=urllib.parse.unquote(session['url'])
            b=re.sub('.*\/', '', string)
            b=(re.findall(".*]",b)[0][1:-1].replace("'","").replace(" ","").split(','))
          
        except:
            pass

    while True:    
        try:
            ############################################################ 
            # 
            # obtengo las tablas en las cuales puedo insertar el fichero excel y creo el select del html   
            with conn.cursor() as cursor:
             
                sqlOptions = 'select concat(\'<option value="\',cast( TAB_NAME as varchar(50)),\'" >\',TAB_LABEL,\'</option>\') from meta.META_CRUD_TABLES'
                options = cursor.execute(sqlOptions).fetchall()
                optStr=''
                for option in options:
                    optStr+= option[0]
                sqlForm6 = '<select class="con_estilos" name="Table" id="Table" type="text" >'+optStr+'</select>'
             ########################################################  
                
             ########################################################

             # obtengo los metadatos de la tabla, es decir siesa tabla se puede actualizar, eliminar, insertar registros
                sql =  ' (' 
                cursor.execute("SELECT T.TAB_ID, concat(T.TAB_SCHEMA_NAME,'.',T.TAB_NAME), T.tab_viewHidden, T.tab_updHidden, T.TAB_newHidden, T.TAB_delHidden, T.TAB_con_Id,t.TAB_DetalleHidden, TD.TAB_LABEL, col_label TAB_DETALLE,  T.tab_filter FROM "+sch+".META_CRUD_TABLES t left join "+sch+".META_CRUD_COLUMNS  on t.tab_det_col_ID = col_ID left join "+sch+".META_CRUD_TABLES td on col_tAB_ID = TD.TAB_ID  where T.TAB_LABEL = ? order by col_id",nomTaula)
                
                camps = cursor.fetchall()
              
                for camp in camps:
                    idTaula = camp[0]
                    sqlTaula = camp[1]
                    viewHidden = camp[2]
                    updHidden = camp[3]
                    newHidden = camp[4]
                    delHidden = camp[5]
                    detHidden = camp[7]
                    connId = camp[6]
                    detTaula = camp[8]
                    detCol = camp[9]
                    filter2 = camp[10]
                ###########################################    
                
                ###########################################
                #obtener la conexion a la tabla que deseo mapear
                cursor.execute("SELECT CON_Driver, CON_host, CON_DBName, CON_DbUser, CON_DbPwd from "+sch+".META_CRUD_CONNECTIONS where Con_Id = ?",connId)
               
                camps = cursor.fetchall()
                for camp in camps:
                    driver = camp[0]
                    server = camp[1]
                    bdName = camp[2]
                    user = camp[3]
                    pwdCryp = camp[4]
                    cipher_suite = Fernet(key)
                    pwdBin =  (cipher_suite.decrypt(bytes(pwdCryp, encoding='utf-8')))
                    pwd = bytes(pwdBin).decode("utf-8")
                 
		    
                try:
                    connOri =  pyodbc.connect("DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s"%(driver,server,bdName,user,pwd))
        
                except Exception as e:
                    
                    return "Error al conectar al origen de Metadatos %s "%e

                ###############################################

                ###############################################
                # obtenemos toda la estructura de la tabla que se desea mapear (columnas, los metadatos de cada columna)
                
                cursor.execute("SELECT COL_NAME, COL_REL_schemaName, COL_REL_tableName, COL_REL_column_DESC, COL_isPK, COL_isFK, COL_view_Hidden, COL_upd_Hidden, COL_new_Hidden, COL_Label, COL_REL_COLUMN_ID, col_Type, COL_FILTER, col_opt_mult, col_checkbox from "+sch+".META_CRUD_COLUMNS where COL_tab_id = ? order by col_id",idTaula)
                
            
                camps = cursor.fetchall()
                ##############################################

                ##############################################
                # se ingresa a este procesa cuando añadimos un nuevo registro
                
                if  request.method == 'POST':
                    for camp in camps:
                        if not camp[8] and not newHidden:
                            
                            sql += camp[0]+', '
                        
                        if camp[4]:
                            pkField =  camp[0]
                    sql = 'insert into '+sqlTaula+ sql[:len(sql)-2]+')  select '
                    for camp in request.form:
                        if request.form[camp] == '':
                             sql += "NULL ,"
                        else:
                            sql += "'"+request.form[camp].replace("'","''''")+"' ,"

                    sql = sql[:len(sql)-1]+'; commit;'
                    with connOri.cursor() as cursorOri:
                        cursorOri.execute(sql)
                        return redirect(session['url'])
                ###################################################################
                ###################################################################
                #Se ingresa a este proceso en los siguiente casos: Cuando se cliquea en el menu en una tabla, cuando aplicamos filtro
                else:
                    valorFiltre,campFiltre=[],[]
                    for camp in camps:
                        if camp[4]!= 1:
                            if camp[13]==0:
                                if request.args.get(camp[9]+'2')!=None:
                                    campFiltre.append(camp[9])
                                    valorFiltre.append(request.args.get(camp[9]+'2').replace("'","''''").replace(" - ","' and '"))
                                    

                            else:
                                if request.args.get(camp[9])!=None:
                                    campFiltre.append(camp[9])
                                    valorFiltre.append(request.args.get(camp[9]).replace("'","''''"))
                            

                   
                    ### coloco sta condicion para decirle que si la lista de filtre esta vacia, me restablesta los valores de esas dos variable a las que son por defecto
                    if len(set(valorFiltre)) <= 1:
                      
                        try:
                         
                            valorFiltre,campFiltre=[],[]
                            a=(re.findall("0\/.*\/", string)[0][3:-2].replace("'","").replace(" ","").split(','))
                            b=re.sub('.*\/', '', string)
                            b=(re.findall(".*]",b)[0][1:-1].replace("'","").replace(" ","").replace('"','').replace('and'," 'and '").split(','))
                
                            for camp1,camp2 in zip(a,b):
                                campFiltre.append(camp1)
                                valorFiltre.append(camp2)
                        except:
                            campFiltre='SenseFiltre'
                            valorFiltre=None

                        
                    ###################
                
                    session['url'] = url_for('index',nomTaula = nomTaula,idLinea = idLinea,campFiltre = campFiltre,valorFiltre = valorFiltre,page=page)
                
                 
                   
                    ########
                    #Para generar los datos del filtro
                    filter_sqlForm = ''
                    description2 = []
                    for camp in camps:    
                        if not camp[6] and not camp[12] :
                          
                            if camp[5]:

                                filter_sqlOptions = 'select concat(\'<option value="\',cast('+camp[10]+' as varchar(6)),\'" >\','+camp[3]+',\'</option>\') from '+camp[1]+'.'+camp[2]+' order by '+camp[3]+' asc'
                        
                            
                                with connOri.cursor() as cursorOri:
                                    filter_optStr=''
                                
                                filter_options = cursorOri.execute(filter_sqlOptions).fetchall()
                            
                                
                                for option in filter_options:
            
                                    filter_optStr+= option[0]
                                
                                # if camp[13]==0:   
                                #     description2.append(camp[9])
                                #     #sqlForm += 'select \'<select name="'+camp[9]+'" id="'+camp[9]+'" type="text" >\'+(select STRING_AGG(\'<option value="\'+cast('+camp[10]+' as varchar(6))+\'" >\'+'+camp[3]+'+\'</option>\',\'\') from '+camp[1]+'.'+camp[2]+')+\'</select>\' union all '
                                #     filter_sqlForm += 'select \'<select multiple class="con_estilos" name="'+camp[9]+'" id="'+camp[9]+'" type="text" ><option selected="true" disabled="disabled">Select Option</option>'+filter_optStr+'</select>\' union all '
                                # else:
                                description2.append(camp[9])
                                #sqlForm += 'select \'<select name="'+camp[9]+'" id="'+camp[9]+'" type="text" >\'+(select STRING_AGG(\'<option value="\'+cast('+camp[10]+' as varchar(6))+\'" >\'+'+camp[3]+'+\'</option>\',\'\') from '+camp[1]+'.'+camp[2]+')+\'</select>\' union all '
                                filter_sqlForm += 'select \'<select class="con_estilos3" name="'+camp[9]+'" id="'+camp[9]+'" type="text" ><option selected="true" disabled="disabled">Select Option</option>'+filter_optStr+'</select>\' union all '
                               

                            else:
                                description2.append(camp[9])
                                if camp[4]==0:
                                    if camp[13]==0:
                                        filter_sqlForm += 'select \'<input name="'+camp[9]+'2" id="'+camp[9]+'2" type="text" value="">\' union all '
                                    else:
                                        if camp[11] == 'int':
                                            filter_sqlForm += 'select \'<input name="'+camp[9]+'" id="'+camp[9]+'" type="number" min="-10000" max="10000">\' union all '
                                        elif camp[11] == 'numeric':
                                            filter_sqlForm += 'select \'<input name="'+camp[9]+'" id="'+camp[9]+'" type="number" step="any"  >\' union all '
                                        elif camp[11] == 'datetime':
                                            filter_sqlForm += 'select \'<input name="'+camp[9]+'" id="'+camp[9]+'" type="datetime"  >\' union all ' 
                                        elif camp[11] == 'date':
                                            filter_sqlForm += 'select \'<input name="'+camp[9]+'" id="'+camp[9]+'" type="date" >\' union all ' 
                                        elif camp[11] == 'bit':   
                                            filter_sqlForm += 'select \'<select name="'+camp[9]+'" id="'+camp[9]+'" type="text" ><option>true</option><option>false</option> </select>\' union all ' 
                                        elif camp[11] == 'password':   
                                            filter_sqlForm += 'select \'<input name="'+camp[9]+'" id="'+camp[9]+'" type="password" >\' union all '
                                        else:
                                            filter_sqlForm += 'select \'<input name="'+camp[9]+'" id="'+camp[9]+'" type="text" >\' union all '
                                    
                            
                  
                            
                    filter_sqlForm =  filter_sqlForm[:len(filter_sqlForm)-11]   
                 
                    
                    
                    ########
                    #Para generar los datos en el formulario de nuevo registro y el de la tabla
                    sqlFields = 'select '
                    sqlForm = ''
                   
                    for camp in camps:    
                        if not camp[6]:
                          
                            if camp[5]:
                               
                                sqlFields +='(select max('+camp[3]+') from '+camp[1]+'.'+camp[2]+' where '+camp[10]+'='+camp[0]+')'
                                sqlOptions = 'select concat(\'<option value="\',cast('+camp[10]+' as varchar(6)),\'" >\','+camp[3]+',\'</option>\') from '+camp[1]+'.'+camp[2]+' order by '+camp[3]+' asc'
                        
                            
                                with connOri.cursor() as cursorOri:
                                    optStr=''
                                
                                options = cursorOri.execute(sqlOptions).fetchall()
                            
                                
                                for option in options:
            
                                    optStr+= option[0]
                                
                                #sqlForm += 'select \'<select name="'+camp[9]+'" id="'+camp[9]+'" type="text" >\'+(select STRING_AGG(\'<option value="\'+cast('+camp[10]+' as varchar(6))+\'" >\'+'+camp[3]+'+\'</option>\',\'\') from '+camp[1]+'.'+camp[2]+')+\'</select>\' union all '
                                sqlForm += 'select \'<select class="con_estilos" name="'+camp[9]+'" id="'+camp[9]+'" type="text" ><option selected="true" disabled="disabled">Select Option</option>'+optStr+'</select>\' union all '
                                
                            else:
                               
                                sqlFields += camp[0]
                                if camp[11] == 'int' and camp[14] != 0 :
                                    sqlForm += 'select \'<input placeholder="" name="'+camp[9]+'" id="'+camp[9]+'" type="number" min="-10000" max="10000">\' union all '
                                elif camp[11] == 'numeric':
                                    sqlForm += 'select \'<input placeholder="" name="'+camp[9]+'" id="'+camp[9]+'" type="number" step="any"  >\' union all '
                                elif camp[11] == 'datetime':
                                    sqlForm += 'select \'<input placeholder="" name="'+camp[9]+'" id="'+camp[9]+'" type="datetime"  >\' union all ' 
                                elif camp[11] == 'date':
                                    sqlForm += 'select \'<input placeholder="" name="'+camp[9]+'" id="'+camp[9]+'" type="date" >\' union all ' 
                                elif camp[11] == 'bit':   
                                    sqlForm += 'select \'<select  name="'+camp[9]+'" id="'+camp[9]+'" type="text" ><option>true</option><option>false</option> </select>\' union all ' 
                                elif camp[11] == 'password':   
                                    sqlForm += 'select \'<input placeholder="" name="'+camp[9]+'" id="'+camp[9]+'" type="password" >\' union all '
                                elif  camp[11] == 'int' and camp[14] == 0 :
                                    sqlForm += 'select \'<input placeholder="" name="'+camp[9]+'" id="'+camp[9]+'" type="checkbox" >\' union all '
                                else:
                                    sqlForm += 'select \'<input placeholder="" name="'+camp[9]+'" id="'+camp[9]+'" type="text" >\' union all '
                                    
                                
                            sqlFields+=' as "'+camp[9]+'", '
                        if camp[4]:
                            sqlFields += camp[0]+ ' as pk, '
                            pkField =  camp[0]
                            
                    sqlForm =  sqlForm[:len(sqlForm)-11]   
                    sqlFields = sqlFields[:len(sqlFields)-2]
                    sqlFrom = ' from '+sqlTaula
                    if idLinea != 0:
                        sqlFrom +=' where '+pkField+'=?'
                    else:
                        sqlFrom +=' where 0=? and Bud_Company = 5'
                        if campFiltre != 'SenseFiltre':
                          
                            detallCrud=0
                            with connOri.cursor() as cursorFiltre:
                                
                                try:
                                    
                                    if '_DetallCRUD' in campFiltre:
                                        
                                        detallCrud = 1
                                        campFiltre = campFiltre.replace('_DetallCRUD','')
                                        campFiltrat =  cursor.execute("select   concat('cast(', COL_NAME,' as varchar(1000))')    from "+sch+".META_crud_columns where col_label = ? and col_tab_id = ? order by col_id",campFiltre, idTaula).fetchone()[0]
                                                                
                                    else:
                                      
                                    #    campFiltrat =  cursorFiltre.execute("select   concat('cast(', COL_NAME,' as varchar(1000))')    from "+sch+".META_crud_columns where col_label = ? and col_tab_id = ? order by col_id",campFiltre, idTaula).fetchone()[0]
                                       campFiltrat=[]
                                       for i in  campFiltre:
                                        
                                           campFiltrat.append(cursor.execute("select case col_isfk  when 1 then CONCAT('(select max (',col_rel_column_id,') from ',col_rel_schemaname,'.',col_rel_tablename, ' as td where td.',col_rel_column_id ,'= ',COL_NAME, ')')  else  concat('cast(', COL_NAME,' as varchar(1000))')  end from "+sch+".META_crud_columns where col_label = ? and col_tab_id = ? order by col_id",i, idTaula).fetchone()[0])
                                except Exception as e:
                                   
                                   
                                    campFiltrat = None
                                if campFiltrat != None:
                                    
                                    if detallCrud == 0:
                                       
                                        for valor_camp, valor_filter in zip(campFiltrat,valorFiltre):
                                            
                                            if valor_filter != '':
                                                if 'and' in valor_filter:
                                                    valor_camp=valor_camp.replace('cast(','').replace('as varchar(1000))','')
                                                    sqlFrom+=" and "+valor_camp+" Between '"+valor_filter+"'"
                                                
                                                else:
                                                   
                                                    if 'Amount' in valor_camp:
                                                
                                                        valor_camp=valor_camp.replace("cast(","").replace("as varchar(1000))","")  
        
                                                        sqlFrom+=" and "+valor_camp+"  "+valor_filter
                                                    else:      
                                                        sqlFrom+=" and "+valor_camp+" ='"+valor_filter+"'"
                                        
                                    else:
                                        
                                        if filter2 == 0:
                                            with connOri.cursor() as cursorOri:
                                                cursorOri.execute("SELECT User_PBI_ID_Users from dbo.USERS_POWERBI where User_PBI_ID = ?",valorFiltre)
                                                valorFiltre = str(cursorOri.fetchall()[0][0])
                                        sqlFrom+=" and "+campFiltrat+"  ='"+valorFiltre+"' "

                    
                    print(sqlFields+sqlFrom+' order by 1 asc')
                    with connOri.cursor() as cursorOri:
                        list_fk=[]
                        fk=cursor.execute('SELECT col_label FROM BUSUP.meta.meta_crud_columns where COL_isFK=1 and col_tab_id=?',idTaula).fetchall()
                        for a in fk:
                            list_fk.append(a[0])
                        edit=cursor.execute('SELECT data_edit FROM BUSUP.meta.meta_crud_tables where tab_id=?',idTaula).fetchone()[0]
                
                        filter_formulari = cursorOri.execute(filter_sqlForm).fetchall()
                        filtros=list(zip(filter_formulari,description2))
                  
                       
                        
                        formulari = cursorOri.execute(sqlForm).fetchall()
                        
                        total = cursorOri.execute('select count(1) '+sqlFrom,idLinea).fetchone()[0]
                        
                        cursorOri.execute(sqlFields+sqlFrom+' order by 1 asc',idLinea)
                        
                        pagination = Pagination(page=page, per_page=per_page, 
                        total=total,
                        css_framework='bootstrap4')
                        description = cursorOri.description
                        descr= description[1:]
                      
                        Registro=list(zip(formulari,descr))
                  
                        prueba=[]
                        pk4,pk3,pk2,pk=[],[],[],[]
                        form3=[]
                        if edit == 1:
                            
                            for a in get_registers(cursor =cursorOri,offset=page,per_page=per_page):
                              
                                sqlForm2=sqlForm
                                count=0
                                for i in a:
                                    
                                   
                                    if description[count][0] in list_fk:
                 
                                        
                                        sqlForm2 = sqlForm2.replace(f">{i}</option>", f"selected> {i} </option>")
                                       
                                        count+=1
                                           
                                    else:
                                        sqlForm2 = sqlForm2.replace(f'name="{description[count][0]}"', f'value="{i}"  name="{description[count][0]}" class="type2" ')
                              
                                        count+=1
    
                               
                                if delHidden == 0 or detHidden == 0 : 
                                    if delHidden == 0 and detHidden == 0 : 
                                        c=f"<a href='/delete/{nomTaula}/{a[0]}'>Borrar</a> <a href='/{detTaula}/0/{detCol}_DetallCRUD/{a[0]}'>Detalle</a>"
                                    elif delHidden == 0 and detHidden != 0 :
                                        c=f"<a href='/delete/{nomTaula}/{a[0]}'>Borrar</a>"
                                    else:
                                        c=f"<a href='/{detTaula}/0/{detCol}_DetallCRUD/{a[0]}'>Detalle</a>"
                                    
                                    pk.append(a[0])
                                    pk2.append(c)
                                    pk3.append(pk2)
                                    pk4.append(pk3)
                                    pk3,pk2=[],[]
                                    formulari2 = cursorOri.execute(sqlForm2).fetchall()
                                    prueba.append(formulari2)
                                    form3=list(zip(prueba,pk4))
                                    
                                
                                else:
                                    pk.append(a[0])
                                    formulari2 = cursorOri.execute(sqlForm2).fetchall()
                                    prueba.append(formulari2)
                                    form3=None

                                   
                
                        return render_template('index.html',form =formulari, form2=prueba, description=description,taula=get_registers(cursor =cursorOri,offset=page,per_page=per_page),idLinea=idLinea,nomTaula=nomTaula,campFiltre=campFiltre, page=page, per_page=per_page, pagination=pagination,  updHidden = updHidden, newHidden = newHidden, delHidden = delHidden, detHidden = detHidden,detTaula=detTaula,detCol=detCol, edit=edit, pk=pk, usuario=session['username'], form3=form3, tab=sqlForm6, filter=filter_formulari, description2=description2, filtros=filtros, Registro=Registro  )
            break
        except Exception as e:
            print('Ko')
            return 'Hi ha hagut un problema2: %s'%e
            print(e)
            errors += 1
            if errors > 2:
                break      
    
@app.route('/delete/<string:nomTaula>/<int:id>')
@is_logged_in
def delete(nomTaula,id):
    print('probando el nuevo input')
    print(request.form.getlist('delete'))
    print(request.form.getlist('ID'))
    # sql = ' where '
    # with conn.cursor() as cursor:
    #     cursor.execute('SELECT * FROM '+sch+'.META_CRUD_TABLES where tab_label = ? ',nomTaula)
    #     camp=cursor.fetchone()
    #     schema = camp[2]
    #     nomTaula2 = camp[3]
    #     id_taula=camp[0]
    # with conn.cursor() as cursor:
    #     cursor.execute('SELECT col_name FROM '+sch+'.META_CRUD_COLUMNS where col_tab_id = ? ', id_taula)
    #     sql+=cursor.fetchone()[0]
    # sql = 'delete '+schema+'.'+nomTaula2+sql+'= ? ; commit;'
    # delete = conn.cursor()
    try:
        # delete.execute(sql,id)
        return redirect('/'+str(nomTaula)+'/0')
    except ValueError as err:
        return "Error: {0}".format(err)
        
# aca solo entro si le doy en el boton de actualizar o agregar

@app.route('/update/<string:nomTaula>/<int:idLinea>',methods=['POST', 'GET'])
@is_logged_in
def update(nomTaula,idLinea):
    # task = Renovacions.query.get_or_404(id)
    user ='N/A'
    if 'x-iis-windowsauthtoken' in request.headers.keys():
        handle_str = request.headers['x-iis-windowsauthtoken']
        handle = int(handle_str, 16) # need to convert from Hex / base 16
        win32security.ImpersonateLoggedOnUser(handle)
        user = win32api.GetUserName()
        win32security.RevertTo() # undo impersonation
        win32api.CloseHandle(handle) # don't leak resources, need to close the handle!

    if request.form.getlist('delete')[0]=='Si':
        sql = ' where '
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM '+sch+'.META_CRUD_TABLES where tab_label = ? ',nomTaula)
            camp=cursor.fetchone()
            schema = camp[2]
            nomTaula2 = camp[3]
            id_taula=camp[0]
        with conn.cursor() as cursor:
            cursor.execute('SELECT col_name FROM '+sch+'.META_CRUD_COLUMNS where col_tab_id = ? ', id_taula)
            sql+=cursor.fetchone()[0]
        sql = 'delete '+schema+'.'+nomTaula2+sql+'= ? ; commit;'
        delete = conn.cursor()
        try:
            for id in request.form.getlist('ID'):
                delete.execute(sql,id)
                
            return redirect('/'+str(nomTaula)+'/0')
        except ValueError as err:
            return "Error: {0}".format(err)
        
    else:
    

        with conn.cursor() as cursor:
            try:
                tab={'name':[],
                        'id':[]}
                cursor.execute("SELECT TAB_NAME, TAB_LABEL  FROM "+sch+".META_CRUD_TABLES")
                camps = cursor.fetchall()
                for a in camps:
                    tab['name'].append(a[0])
                    tab['id'].append(a[1])
                
                
                sql = ' Set '
                sql2 = ''
                cursor.execute("SELECT TAB_Id, CONCAT(TAB_schema_Name,'.',TAB_Name), TAB_viewHidden, TAB_updHidden, TAB_newHidden, TAB_delHidden, TAB_con_Id, tab_flag_field  FROM "+sch+".META_CRUD_TABLES where TAB_LABEL = ?",nomTaula)
                camps = cursor.fetchall()
                for camp in camps:
                    idTaula = camp[0]
                    sqlTaula = camp[1]
                    viewHidden = camp[2]
                    updHidden = camp[3]
                    newHidden = camp[4]
                    delHidden = camp[5]
                    connId = camp[6]
                    flagField = camp[7]
                    
                cursor.execute("SELECT CON_Driver, CON_host, CON_DBName, CON_DbUser, CON_DbPwd from "+sch+".META_CRUD_CONNECTIONS where Con_Id = ?",connId)
                camps = cursor.fetchall()
                if flagField is not None:
                    sql = sql+flagField+" = 1, "
                for camp in camps:
                    driver = camp[0]
                    server = camp[1]
                    bdName = camp[2]
                    user = camp[3]
                    pwdCryp = camp[4]
                    cipher_suite = Fernet(key)
                    pwdBin =  (cipher_suite.decrypt(bytes(pwdCryp, encoding='utf-8')))
                   
                    pwd = bytes(pwdBin).decode("utf-8")
                try:
                    connOri =  pyodbc.connect("DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s"%(driver,server,bdName,user,pwd))
                except Exception as e:
                    print("Error al conectar al origen de datos ",e)
                
                cursor.execute("SELECT COL_NAME, COL_REL_schemaName, COL_REL_tableName, COL_REL_column_DESC, COL_isPK, COL_isFK, COL_view_Hidden, COL_upd_Hidden, COL_new_Hidden, COL_Label, COL_REL_COLUMN_ID, col_Type from "+sch+".META_CRUD_COLUMNS where COL_TAB_ID = ? order by col_id",idTaula)
                camps = cursor.fetchall()
                
                # procedimiento para acutualizar

            
                
                if request.method == 'POST':   
                  
                    try:
                        
                        string=urllib.parse.unquote(session['url'])
                        campFiltre,valorFiltre=[],[]
                        a=(re.findall("0\/.*\/", string)[0][3:-3].replace("'","").replace(" ","").split(','))
                        
                        b=re.sub('.*\/', '', string)
                      
                        b=(re.findall(".*]",b)[0][1:-1].replace("'","").replace(" ","").split(','))
                      
                        page=re.sub('.*=', '', string).replace(" ","")
                      
                        
                    
                        for camp1,camp2 in zip(a,b):
                            campFiltre.append(camp1)
                            valorFiltre.append(camp2.replace("'","''''"))
                   
                        
                        session['url'] = url_for('index', nomTaula = nomTaula,idLinea = idLinea,campFiltre = campFiltre,valorFiltre = valorFiltre,page=page)
                      
                    except:
                       
                        pass
                
                    
                
                    for index,l in enumerate(request.form.getlist('pk')):
            
                        
                        for camp in camps:
                            
                            if not camp[7]:
                            
                                if request.form.getlist(camp[9])=='' or request.form.getlist(camp[9])[index]=='None' :
                                    sql += camp[0]+'=NULL , '
                                    sql2 += camp[0]+'!=NULL or '
                                  
                                else:
                                    sql += camp[0]+'=\''+request.form.getlist(camp[9])[index].replace("'","''''")+'\' , '
                                    sql2 += camp[0]+'!=\''+request.form.getlist(camp[9])[index].replace("'","''''")+'\' or '  
                                        
                            if camp[9] == "usuario":
                                sql += camp[0]+'=\''+user+'\' , '
                            
                            if camp[4]:
                                pkField =  camp[0]
                                schema = camp[0]

                        sql2 = sql2[:len(sql2)-4]    
                        sql = 'UPDATE '+sqlTaula+' '+sql[:len(sql)-2] + ' where '+pkField+'= ? ; commit;'
                        #que no se actulice siempre#
                        # sql = 'UPDATE '+sqlTaula+' '+sql[:len(sql)-2] + ' where '+pkField+'= ? and ('+sql2+') ; commit;'
                    
                    
                        with connOri.cursor() as cursorOri:
                        
                      
                            cursorOri.execute(sql,l)
                            sql = ' Set '
                            sql2 = ''
                            if flagField is not None:
                                sql = sql+flagField+" = 1, "
        
                    return redirect(urllib.parse.unquote(session['url']))
                
                # procedimiento cuando se le da en el boton de actualizar
                
                else:
                
            #    with conn.cursor() as cursor:
                   
                    sql = 'select '
                    pkField = ''
                    for camp in camps:
                        if not camp[7]:
                            if camp[5] :
                                sqlOptions = 'select concat(\'<option value="\',cast('+camp[10]+' as varchar(6)),\'" >\','+camp[3]+',\'</option>\') from '+camp[1]+'.'+camp[2]
                                with connOri.cursor() as cursorOri:
                                    optStr=''
                                    options = cursorOri.execute(sqlOptions).fetchall()
                                    for option in options:
                                        optStr+= option[0]
                                    
                                    
                                sql += 'replace(\''+optStr+'\',concat(\'"\',cast('+camp[0]+' as varchar(6)),\'"\'),concat(\'"\',cast('+camp[0]+' as varchar(6)),\'" selected\'))'
                            else:
                                sql += camp[0]
                            sql+=' as "'+camp[9]+'", '
                        if camp[4]:
                            pkField =  camp[0]
                          
                    sql = sql[:len(sql)-2]+' from '+sqlTaula
                    if idLinea != 0:
                        sql +=' where '+pkField+'= ?'
                  
                    with connOri.cursor() as cursorOri:
                        
                        cursorOri.execute(sql,idLinea)
                        return render_template('update.html',taula=cursorOri,idLinea=idLinea,nomTaula=nomTaula, usuario=session['username'])
            except Exception as e:
                return 'Hi ha hagut un problema: %s'%e


@app.route('/Login/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
      
        username = request.form['username']
        password_candidate = request.form['password']

        with conn.cursor() as cursor:
            result=cursor.execute("select * from dbo.users where username =?", username)
            data = cursor.fetchone()
            try: 
                password = data[2]
             
                if sha256_crypt.verify(password_candidate, password):
            
                    session ['logged_in'] = True
                    session['username'] = username
                    session['id'] = data[0]
                  
                    app.logger.info('PASSWORD MATCHED')

#                    

                    # with conn.cursor() as cursor:
                    #     cursor.execute("SELECT TAB_LABEL   FROM "+sch+".META_CRUD_TABLES where TAB_viewHidden = 0 order by tab_id")
                    #     camps = cursor.fetchall()
                    #     # print(camps)
                    #     for camp in camps:
                    #         idTaula = camp[0]
                    #         break
                    
                    # return redirect('/'+str(idTaula)+'/0')
                    return redirect('/powerbi')
        
                else:
                    app.logger.info('PASSWORD NO MATCHED')
                    flash('USERNAME OR PASSWORD INCORRECT', 'success')
                    return render_template('login_form.html')
        
                cursor.close()
            except:
                app.logger.info('NO USER')
                flash('USERNAME OR PASSWORD INCORRECT', 'success')
        
                return render_template('login_form.html')
    
    return render_template('login_form.html')
      


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/')
def inicio():
    return redirect('/Login/')


@app.route('/insertar', methods=["GET", "POST"])
@is_logged_in
def insert():
    start = time.time()


    Table=request.form['Table']
    conn4=("DRIVER={ODBC Driver 17 for SQL Server};SERVER=da-punt.database.windows.net;DATABASE=DEMO;UID=pyuser;PWD=py3141592#")
    connection_uri = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(conn4)
    engine = create_engine(connection_uri, fast_executemany=True)
    f = request.files['archivo'] # obtenemos el archivo del input "archivo"
    filename = secure_filename(f.filename)

    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    excel=open(f"input/{filename}")
    data = pd.read_excel(f"input/{filename}")
    excel.close() 
    os.remove(f"input/{filename}")
    with conn.cursor() as cursor:



        cursor.execute(f"select COLUMN_NAME, DATA_TYPE from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '{Table}'and not ORDINAL_POSITION = 1")
        data2=cursor.fetchall()
      
        columna=''
        dfcolumna=[]
       
        val='('
        for i in data2:
            val+=' ?,'
      
            if re.search(' ', i[0]) == None:
                columna+=i[0]+','
                dfcolumna.append(i[0])
            else:
                columna+='['+i[0]+'],'
                dfcolumna.append(i[0])
        columna = columna[:len(columna)-1]
        val = val[:len(val)-1]+')'


     

       
        
       
       
       
        cursor.execute(f"select COLUMN_NAME, DATA_TYPE from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '{Table}'and not ORDINAL_POSITION = 1")
        data2=cursor.fetchall()


      
     
        # for i,b in zip (data, tipo):
        #     if b == 'varchar':
        #         data[i]=data[i].apply(lambda x: "'"+str(x)+"'")
        # laprueba=pd.DataFrame(data).to_numpy().tolist()
        laprueba=pd.DataFrame(data)
        laprueba.columns = dfcolumna
     
       
        # cursor.execute(f"select * into etl.{Table}3 from dbo.{Table}")
        # cursor.executemany(f"INSERT INTO etl.{Table}2 ({columna}) VALUES {val}",laprueba)


        cursor.execute(f" select tab_id from meta.meta_crud_tables where tab_name = ?", Table)
        tabid=cursor.fetchone()[0]
      
        cursor.execute("SELECT COL_NAME, COL_REL_schemaName, COL_REL_tableName, COL_REL_column_DESC, col_rel_column_id from meta.meta_crud_columns where COL_isFK = 1 and col_tab_id = ?",tabid)
        fk=cursor.fetchall()
        
        for i in fk:
            cursor.execute(f"select {i[3]}, {i[4]}  from {i[1]}.{i[2]}")
            datos=cursor.fetchall()
            v1, v2 = [],[]
            for d in datos:
                #caso particular para busup
                if 'Group' in i[0] or 'SubGroup' in i[0]:
               
                    v1.append(str.lower(d[0][5:]))
                    v2.append(d[1])
                else:
                    v1.append(str.lower(d[0]))
                    v2.append(d[1])
          
            laprueba[i[0]] = laprueba[i[0]].astype(str).str.lower()
            laprueba[i[0]]=laprueba[i[0]].replace(v1,v2)
       
        cursor.execute(f"select * into etl.{Table}3 from dbo.{Table}")
        cursor.execute(f"truncate table etl.{Table}3 ")
        laprueba=laprueba.to_numpy().tolist()
        
        try:
            
            cursor.executemany(f"INSERT INTO etl.{Table}3 ({columna}) VALUES {val}",laprueba)
        except Exception as e:
            return "Error uno de los valores de la columna no se encuentra en dimension de la misma %s "%e
        
     


   

    end = time.time()


    return redirect(session['url'])



if __name__ == "__main__":
    app.run(debug=True)