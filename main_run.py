import global_utils as nira
import pandas as pd
from flask import Flask, render_template,request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/search.html')
    
@app.route('/result',methods=['GET','POST'])
def result():
    #Data frame for displaying data
    df=pd.DataFrame(columns=["Attr","value"])
    if request.method == 'POST':
        company_name = request.form['search']    
    df.loc[0,'Attr']="Email"
    df.loc[0,'value']=  (nira.email_id(company_name))
    df.loc[1,'Attr']="Employee Strength"
    df.loc[1,'value']=(nira.employee(company_name)) 
    df.loc[2,'Attr']="Industry Category"
    data= (nira.industry_category(company_name)) 
    df.loc[2,'value']=data['industry']
    df.loc[3,'Attr']="Revenue"
    df.loc[3,'value']=data['revenue']
    df.loc[4,'Attr']="Profit"
    df.loc[4,'value']=data['profit']
    df.loc[5,'Attr']="Number of opening on naukri"
    df.loc[5,"value"]=nira.naukri(company_name)
    return render_template('/view1.html', tables=[df.to_html(index=False)], data=company_name)

if __name__ == '__main__':
    app.run(debug="true")