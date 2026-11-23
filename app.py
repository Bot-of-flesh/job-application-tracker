import sqlite3

def create_company(company_id, name):
    dic = {
        "id": company_id, "name": name, "status": "未応募"
    }
    return dic

def display_companies(company_list):
    for company in company_list:
        print(f"""{company["id"]} {company["name"]} {company["status"]}""")

def find_company(company_list, company_id):
    for company in company_list:
        if company["id"] == company_id:
            return company

def update_company_status(company_list, company_id, new_status):
    found = find_company(company_list, company_id)
    if found:   
        conn = sqlite3.connect("application.db")
        conn.execute("update companies set status = ? where id = ?", (new_status, company_id))
        conn.commit()
        conn.close()
        found["status"] = new_status
        return True
    else:
        return False

def filter_companies_by_status(company_list, status):
    filtered_list = []
    for company in company_list:
        if status == company["status"]:
            filtered_list.append(company)
    return filtered_list

def get_next_company(company_list):
    IDs = []
    if company_list:
        for company in company_list:
            IDs.append(company["id"])
    else: return 1
    return max(IDs) + 1
    
def register_company(company_list):
    name = input("会社名を入力してください:")
    next = insert_company(name, "未応募")
    company_list.append(create_company(next, name))
    display_companies(company_list)

def change_status(company_list):
    try:
        ID = int(input("IDを入力してください:"))
    except ValueError:
        print("IDは数字で入力してください")
        return
    status = input("新しい選考状況:")
    
    if update_company_status(company_list, ID, status) == True:
        print("更新しました")
    else:
        print("会社が見つかりません")

def show_filtered_companies(company_list):
    status = input("絞り込む選考状況:")
    filtered = filter_companies_by_status(company_list, status)
    if filtered:
        display_companies(filtered)
    else:
        print("該当する会社はありません")

def initialize_database():
    conn = sqlite3.connect("application.db")
    conn.execute("CREATE TABLE if not exists companies(id integer primary key, name text not null, status text not null)")
    conn.commit()
    conn.close()

def load_companies():
    conn = sqlite3.connect("application.db")
    results = conn.execute("select id, name, status from companies").fetchall()
    conn.close()
    diclist = []
    for result in results:
        dic = {"id": result[0], "name": result[1], "status": result[2]}
        diclist.append(dic)
    
    return diclist

def insert_company(name, status, max_companies=None):
    conn = sqlite3.connect("application.db")
    if max_companies is None:
        ins = conn.execute("insert into companies (name, status) VALUES(?, ?)" , (name, status))
    else:   
        ins = conn.execute("insert into companies (name, status) select ?, ? where(select count(*) from companies ) < ?" , (name, status, max_companies))
    conn.commit()
    conn.close()
    if ins.rowcount == 0:
        return None
    return ins.lastrowid

def delete_company(company_id):
    conn = sqlite3.connect("application.db")
    delete = conn.execute("delete from companies where id = ?", (company_id,))
    conn.commit()
    conn.close()
    if delete.rowcount == 1:
        return True
    elif delete.rowcount == 0:
        return False
   

def main():
    initialize_database()
    companies = load_companies()
    
    
    operation = "99"
    while(operation != "0"):
        print("1: 会社登録")
        print("2: 一覧表示")
        print("3: 選考状況変更")
        print("4: 選考状況で絞り込み")
        print("0: 終了")
        operation = input("操作を選んでください:")

        if operation == "1":
            register_company(companies)
        elif operation == "2":
            display_companies(companies)
        elif operation == "3":
            change_status(companies)
        elif operation == "4":
            show_filtered_companies(companies)
        elif operation == "0":
            print("終了します")
            break
        else:
            print("選択できない番号です")

if __name__ == "__main__":
    main()

