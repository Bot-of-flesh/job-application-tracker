import flask
import app
web = flask.Flask(__name__)

@web.route("/")
def home():
    companies = app.load_companies()
    status = flask.request.args.get("status", "")
    if status:
        display_list = app.filter_companies_by_status(companies, status)
    else:
        display_list = companies
    return flask.render_template("index.html", company_count = len(companies), company_list = display_list, selected_status = status)

@web.route("/register", methods = ["GET", "POST"])
def register():
    if flask.request.method == "POST":
        company_name = flask.request.form.get("company_name", "").strip()
        if not company_name:
            return "会社名を入力してください"
        else:
            new_id = app.insert_company(company_name, "未応募", max_companies=30)
            if new_id is None:
                return "登録上限に達しました"
            else:
                list_url = flask.url_for("home")
                return flask.redirect(list_url)
    elif flask.request.method == "GET":
        company_name = flask.request.form.get("company_name", "")
        return flask.render_template("register.html", company_name = company_name)
    return flask.render_template("register.html")

@web.route("/status/<int:company_id>", methods = ["GET", "POST"])
def edit_status(company_id):
    companies = app.load_companies()
    company = app.find_company(companies, company_id)
    if not company:
        return "会社が見つかりません"
    if flask.request.method == "POST":       
            new_status = flask.request.form.get("new_status", "").strip()
            if not new_status:
                return "選考状況を入力してください"
            else:
                app.update_company_status(companies, company_id, new_status)
            list_url = flask.url_for('home')
            return flask.redirect(list_url)
    else:
        return flask.render_template("edit_status.html", company = company)

@web.cli.command("init-db")
def init_db():
    app.initialize_database()
    print("DBの準備ができました")
