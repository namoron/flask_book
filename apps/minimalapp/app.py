from email_validator import validate_email,EmailNotValidError
from flask import Flask,render_template,url_for,current_app,g,request,redirect,flash
import logging
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
# SECRET_KEYを追加
app.config["SECRET_KEY"]  = "2AZSMss3p5QPbcY2hBsJ"
#ログレベルを設定する
app.logger.setLevel(logging.DEBUG)
#リダイレクトを中断しないようにする
app.config["DEBUG_TB_INSTERCEPT_REDIRECTS"]  = False
# DebugToolbarExtension にアプリケーションをセットする
toolbar  =  DebugToolbarExtension(app)
@app.route("/")
def index():
    return 'Hello,Flaskbook!'

@app.route("/hello/<name>",methods=["GET"],endpoint="hello-endpoint")
def hello(name):
    return f"Hello,{name}!"

@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html",name = name) 

with app.test_request_context():
    # /
    print(url_for("index"))
    # /hello/world
    print(url_for("hello-endpoint",name= "world"))
    # /name/mana?page=1
    print(url_for("show_name",name= "mana",page="1"))

#アプリケーションコンテキストを取得してスタックへpush
ctx = app.app_context()
ctx.push()

print(current_app.name)

g.connection = "connection"
print(g.connection)



with app.test_request_context("/users?updated=true"):
    # /
    print(request.args.get("updated"))

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/complete",methods=["GET","POST"])
def contact_complete():
    if request.method == "POST":
        # form属性を使ってフォームの値を取得
        username = request.form["username"]
        email  = request.form["email"]
        description  = request.form["description"]
        #入力チェック
        is_valid = True
        
        if not username:
            flash("ユーザー名は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))
        # メールを送る

        #問い合わせ完了エンドポイントへリダイレクト
        flash("問い合わせ内容はメールにて送信しました．問い合わせありがとうございました．")
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")