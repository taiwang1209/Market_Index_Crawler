# save this as app.py
import requests, time, smtplib
from datetime import datetime
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, flash, render_template, url_for, redirect

app = Flask(__name__)

url = 'https://histock.tw/index'
suffix = ['/DJI', '/NASDAQ', '/SP500', '/SOX', '-tw/FITX']
data = []

def crawl(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    name = soup.find('h3').text.strip().replace('美國指數','道瓊指數').replace('NASDAQ','那斯達克').replace('S&P500','標普500').replace('費城半導體','費半指數').replace('台指期','台指期貨')
    change = soup.find(id='Price1_lbTChange').text.strip()
    percent = soup.find(id='Price1_lbTPercent').text.strip()
    price = '收' + soup.find(id='Price1_lbTPrice').text.strip()
    data.extend([name, change, percent, price])
    return data

@app.route('/')
def index():
    title = '指數爬蟲'
    bootstrap = url_for('static', filename='css/bootstrap.min.css')
    form = url_for('static', filename='css/form.css')
    fontawsome = url_for('static', filename='css/fa.all.min.css')
    return render_template('index.html', title = title, bootstrap = bootstrap, form = form, fontawsome = fontawsome)

@app.route('/mail', methods=['GET','POST'])
def mail():
    email = request.form.get('email') #從表單取得收件人email
    
    for i in range(len(suffix)):
        crawl(url+suffix[i])

    #寄信
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content['subject'] = datetime.now().strftime('%Y-%m-%d')+' 指數資訊'  #郵件標題
    content['from'] = '寄件者email'  #改為寄件者email
    content['to'] = email #收件人email
    content.attach(MIMEText(datetime.now().strftime('%Y-%m-%d')+' 指數資訊'+'\n'+
                            data[0]+' '+data[1]+' '+data[2]+' '+data[3]+'\n'+
                            data[4]+' '+data[5]+' '+data[6]+' '+data[7]+'\n'+
                            data[8]+' '+data[9]+' '+data[10]+' '+data[11]+'\n'+
                            data[12]+' '+data[13]+' '+data[14]+' '+data[15]+'\n'+
                            data[16]+' '+data[17]+' '+data[18]+' '+data[19]+'\n'))  #郵件內容

    with smtplib.SMTP(host='smtp.gmail.com', port='587') as smtp:  # 設定SMTP伺服器
        smtp.ehlo()  # 驗證SMTP伺服器
        smtp.starttls()  # 建立加密傳輸
        smtp.login('寄件者email', 'Google應用程式密碼')  #改為寄件者email及Google應用程式密碼
        smtp.send_message(content)  # 寄送郵件

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()