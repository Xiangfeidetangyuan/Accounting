import request as request
from django.shortcuts import render
from django.shortcuts import HttpResponse
import tkinter.messagebox  #弹窗库
from tkinter import ttk
from login import models
from tkinter import *
import datetime
import json
from mails import SendMails
# Create your views here.

'''
接口demo
'''
def api_userinfo(request):
    dic = {}
    if request.method == 'GET':
        dic['message'] = 0
        return HttpResponse(json.dumps(dic))
    else:
        dic['message'] = '方法错误'
        return HttpResponse(json.dumps(dic, ensure_ascii=False))


'''
原函数
'''
def index(request):  # 接收登录的消息
    if request.method == "POST":
        # 注册界面跳转
        if "register" in request.POST:
            print("1")
            return render(request, "signup.html")
        # 登录
        username = request.POST.get("username")
        password = request.POST.get("password")
    # 数据库操作方法
        user = models.UserInfo.objects.get(user=username)
        if password == user.pwd:
            # 使用session保存当前用户信息
            request.session["currentUser"] = user.user
            print(request.session.get("currentUser"))
            print("验证成功")
            return render(request, "menu.html")
        else:
            return HttpResponse("账号或用户名错误!")
    return render(request, "index.html")



def signup(request):
    if request.method == "POST":
        print(request.POST)
        # 进行验证
        if request.POST.get("password") == request.POST.get("password2") and\
                request.POST.get("username") != "" and request.POST.get("mail") != "":
            username = request.POST.get("username")
            password = request.POST.get("password")
            checkresult=[]
            try:
                checkresult=models.UserInfo.objects.get(user=username)
            except models.UserInfo.DoesNotExist:
                print("注册信息已保存")
                #  将数据保存到数据库
                models.UserInfo.objects.create(user=username, pwd=password, mail=request.POST.get("mail"))
                return render(request, "index.html")
            return HttpResponse("该用户名已存在,请重新注册")
        else:
            return HttpResponse("信息为空或密码不匹配")


def add(request):
    return render(request, "AddExpend.html")


# 保存消费项
def SaveExpend(request):
    print(request.POST)
    price = request.POST.get("price")
    remarks = request.POST.get("remarks")
    itemtype = request.POST.get("radio")
    cur = datetime.datetime.now()
    # 数据库操作方法
    models.ExpendItem.objects.create(price=price, remarks=remarks, ItemType=itemtype, ItemTime=cur,
                                     ItemUser=models.UserInfo.objects.get(user=request.session.get("currentUser")).user)
    return render(request, "menu.html")


# 保存收入项
def SaveIncome(request):
    print(request.POST)
    price = request.POST.get("price")
    remarks=request.POST.get("remarks")
    itemtype=request.POST.get("radio")
    cur = datetime.datetime.now()
    # 数据库操作方法
    models.IncomItem.objects.create(price=price, remarks=remarks, ItemType=itemtype, ItemTime=cur,
                                    ItemUser=models.UserInfo.objects.get(user=request.session.get("currentUser")).user)
    return render(request, "menu.html")


# 展示账单
def show(request):
    if request.method == "POST":
            print("subtotal")
            # 创建容器
            root = tkinter.Tk()
            root.title("账单")
            root.tree = ttk.Treeview(height=10, columns=("#0", "#1", "#2", "#3", "#4"))
            ttk.Button(text="支出", command=lambda: showExpendItem(root, request.session.get("currentUser"))).grid(row=1, column=0)
            ttk.Button(text="收入", command=lambda: showIncomeItem(root, request.session.get("currentUser"))).grid(row=1, column=1)
            root.tree.heading("#0", text="序号", anchor=CENTER)
            root.tree.heading("#1", text="项目", anchor=CENTER)
            root.tree.heading("#2", text="费用", anchor=CENTER)
            root.tree.heading("#3", text="时间", anchor=CENTER)
            root.tree.heading("#4", text="备注", anchor=CENTER)
            root.tree.grid(row=2, columnspan=4, padx=1, pady=1)
            ttk.Button(text='删除', command=lambda: delete_accounting(root)).grid(row=5, column=0)
            ttk.Button(text='编辑', command=lambda: edit_accouting(root)).grid(row=5, column=1)
            root.mainloop()
    return render(request, "menu.html")


# 展示花费项  传入参数tkinter，用户名
def showExpendItem(root,User):
    print(User)
    # 搜索该用户消费项
    try:
        ExpendItemList = models.ExpendItem.objects.filter(ItemUser=User).\
            values_list("id", "ItemType", "price", "ItemTime", "remarks")
    except models.ExpendItem.DoesNotExist:
        tkinter.messagebox.showinfo('提示', "无记录")
    # 在tkinter展示
    records = root.tree.get_children()
    for element in records:
        root.tree.delete(element)
    for i, (id,type, price, time, remarks) in enumerate(ExpendItemList, start=1):
        root.tree.insert("", "end", text="支出"+str(id), values=(type, price, time, remarks))


# 展示收入项  传入参数tkinter，用户名
def showIncomeItem(root,User):
        print(User)
        # 搜索该用户收入项
        try:
            IncomeItemList = models.IncomItem.objects.filter(ItemUser=User).values_list\
                ("id", "ItemType", "price", "ItemTime", "remarks")
        except models.IncomItem.DoesNotExist:
            tkinter.messagebox.showinfo('提示', "无记录")
        print("输出收入列表：")
        print(IncomeItemList)
        # 在tkinter展示
        records = root.tree.get_children()
        for element in records:
            root.tree.delete(element)
        for i, (id, type, price, time, remarks) in enumerate(IncomeItemList, start=1):
            root.tree.insert("", "end", text="收入"+str(id), values=(type, price, time, remarks))


# 删除项目
def delete_accounting(root):
       a = tkinter.messagebox.askokcancel('提示', '要执行此操作吗')
       if a:
            for item in root.tree.selection():
                item_text=root.tree.item(item, "text")
                print(item_text)
                str = re.sub("\D", "", item_text)
                print(str)
                if "支出" in item_text:
                    models.ExpendItem.objects.filter(id=str).delete()
                    print("删除成功")
                else:
                    models.IncomItem.objects.filter(id=str).delete()
                    print("删除成功")


# 编辑项目
def edit_accouting(root):
    edit_new = Toplevel()
    edit_new.title = "编辑项目"
    for item in root.tree.selection():
        item_text = root.tree.item(item, "text")
        str = re.sub("\D", "", item_text)
        if "支出" in item_text:
            accouting = models.ExpendItem.objects.get(id=str)
            new_type = ttk.Combobox(edit_new, values=["Dining", "Shopping", "Housing", "Transporting",
                                                      "Communicating", "Entertainmenting", "Medical", "Education",
                                                      "RedPaper", "Investent",
                                                      "loan", "PayDebt", "Others"], state='readonly')
        else :
            accouting = models.IncomItem.objects.get(id=str)
            new_type = ttk.Combobox(edit_new, values=["wage", "MoneyManagement", "RedPaper", "Borrow",
                                                      "CollectDebt", "Others"], state='readonly')

        # print(accouting.ItemTime,accouting.remarks)
        # 原来的项目
        Label(edit_new, text='原来金额').grid(row=0, column=1)
        Entry(edit_new, textvariable=StringVar(edit_new, accouting.price), state='readonly').grid(row=0, column=2)

        Label(edit_new, text='新的金额').grid(row=1, column=1)
        new_price = Entry(edit_new)
        new_price.grid(row=1, column=2)

        Label(edit_new, text='原来备注').grid(row=2, column=1)
        Entry(edit_new, textvariable=StringVar(edit_new, value=accouting.remarks), state='readonly').grid(row=2, column=2)

        Label(edit_new, text='新的备注').grid(row=3, column=1)
        new_remarks = Entry(edit_new)
        new_remarks.grid(row=3, column=2)

        Label(edit_new, text='类别').grid(row=4, column=1)

        new_type.grid(row=4, column=2)
        new_type.set(accouting.ItemType)

        Label(edit_new, text='原来时间').grid(row=5, column=1)
        Entry(edit_new, textvariable=StringVar(edit_new, value=accouting.ItemTime), state='readonly').grid(row=5,column=2)

        Label(edit_new, text='新的时间').grid(row=6, column=1)
        new_time = Entry(edit_new)
        new_time.grid(row=6, column=2)

        Button(edit_new, text='更新',command=lambda: edit_record(item_text, new_price.get(), new_remarks.get(),
                                                               new_type.get(), new_time.get(),accouting)).grid(row=8, column=2)
        edit_new.mainloop()


# 进行数据的更改  传入参数 序号、金额、备注、类型、时间、该条目
def edit_record(item_text, price, remarks, type, time, account):
    # 若用户没有更改，则还是原来的数据
    if price == "":
         price = account.price
    if remarks == "":
        remarks = account.remarks
    if time == "":
        time = account.ItemTime
    str = re.sub("\D", "", item_text)
    if "支出" in item_text:
        accouting = models.ExpendItem.objects.get(id=str)
    else:
        accouting = models.IncomItem.objects.get(id=str)
    accouting.price = price
    accouting.ItemType = type
    accouting.remarks = remarks
    accouting.ItemTime = time
    accouting.save()


def plan(request):
    incometypelist, incomepricelist,incomesum=getIncomeData(request.session.get("currentUser"))
    Expendtypelist, Expendpricelist, Expendsum=getExpendData(request.session.get("currentUser"))
    username = request.session.get("currentUser")
    try:
        m=models.goal_plan.objects.get(goal_User=username)
    except models.goal_plan.DoesNotExist:
        goal_income = "未设置"
        goal_expend = "未设置"
        return render(request, "plan.html",
                      {"incometypedata": json.dumps(incometypelist), "incomepricedata": json.dumps(incomepricelist),
                       "incomesumdata": incomesum, "Expendtypedata": json.dumps(Expendtypelist),
                       "Expendpricedata": json.dumps(Expendpricelist), "expendsumdata": Expendsum,
                       "goal_income": goal_income, "goal_expend": goal_expend})
    goal_income = models.goal_plan.objects.get(goal_User=username).goal_income
    goal_expend = models.goal_plan.objects.get(goal_User=username).goal_expend
    return render(request, "plan.html", {"incometypedata": json.dumps(incometypelist), "incomepricedata": json.dumps(incomepricelist),
                    "incomesumdata":incomesum, "Expendtypedata": json.dumps(Expendtypelist),
                    "Expendpricedata":json.dumps(Expendpricelist), "expendsumdata": Expendsum,
                     "goal_income":goal_income, "goal_expend": goal_expend})


def setplan(request):
        print("访问setplan 成功")
        return render(request, "setplan.html")


def saveplan(request):
        cur = datetime.datetime.now()
        username = models.UserInfo.objects.get(user=request.session.get("currentUser")).user
        try:
            user = models.goal_plan.objects.get(goal_User=username)
        except models.goal_plan.DoesNotExist:
            models.goal_plan.objects.create(goal_income=request.POST.get("goal_income"),
                                            goal_expend=request.POST.get("goal_expend"), goalTime=cur,
                                            goal_User=username)
            print("setplan 成功")
            return render(request, "menu.html")
        user.goal_income = request.POST.get("goal_income")
        user.goal_expend = request.POST.get("goal_expend")
        user.goalTime = cur
        user.save()
        print("setplan 成功")
        return render(request, "menu.html")


def getIncomeData(User):
    IncomeType = {"wage": 0, "MoneyManagement": 1, "RedPaper": 2, "Borrow": 3, "CollectDebt": 4, "Others": 5}
    cur = datetime.datetime.now().month
    incometypelist = ["wage", "MoneyManagement", "RedPaper", "Borrow", "CollectDebt", "Others"]
    incomepricelist = [0]*6
    incomesum = 0
    # 进行判空检测
    try:
       incomedatalist = models.IncomItem.objects.filter(ItemUser=User).values_list("ItemTime", "ItemType", "price")
    except models.IncomItem.DoesNotExist:
        return incometypelist, incomepricelist, incomesum
    if incomedatalist.exists():
        print(incomedatalist)
        for i, (time, type, price) in enumerate(incomedatalist, start=1):
            time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")  # 获取月份
            if cur == time.month:
                incomepricelist[IncomeType[type]] += int(price)
        print(incometypelist)
        print(incomepricelist)
        for i in incomepricelist:
            incomesum += int(i)
        j = 0
        while j < len(incomepricelist):
            incomepricelist[j] = int(incomepricelist[j])/incomesum
            j += 1
    return incometypelist, incomepricelist, incomesum


def getExpendData(User):
    ExpendType = {"Dining": 0, "Shopping":1, "Housing": 2, "Transporting": 3, "Communicating": 4, "Entertainmenting": 5,
                  "Medical": 6, "Education": 7, "RedPaper": 8, "Investent": 9, "loan": 10,  "PayDebt": 11, "Others": 12}
    cur = datetime.datetime.now().month
    Expendtypelist = ["Dining", "Shopping", "Housing", "Transporting", "Communicating", "Entertainmenting",
                  "Medical", "Education", "RedPaper", "Investent", "loan", "PayDebt", "Others "]
    Expendpricelist = [0]*13
    Expendsum = 0
    try:
        Expenddatalist = models.ExpendItem.objects.filter(ItemUser=User).values_list("ItemTime", "ItemType", "price")
    except models.ExpendItem.DoesNotExist:
        return Expendtypelist, Expendpricelist, Expendsum
    if Expenddatalist.exists():
        for i, (time, type, price) in enumerate(Expenddatalist, start=1):
            print(time)
            time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")  # 获取月份
            if cur == time.month:
                Expendpricelist[ExpendType[type]] += int(price)
        print(Expendtypelist)
        print(Expendpricelist)
        for i in Expendpricelist:
            Expendsum += int(i)
        j = 0
        while j < len(Expendpricelist):
            Expendpricelist[j] = int(Expendpricelist[j])/Expendsum
            j += 1
    return Expendtypelist, Expendpricelist, Expendsum


# 发送邮件
def sendEmail(request):
    incometypelist, incomepricelist, incomesum = getIncomeData(request.session.get("currentUser"))
    Expendtypelist, Expendpricelist, Expendsum = getExpendData(request.session.get("currentUser"))
    username = request.session.get("currentUser")
    try:
        goal_income = models.goal_plan.objects.get(goal_User=username).goal_income
        goal_expend = models.goal_plan.objects.get(goal_User=username).goal_expend
    except models.goal_plan.DoesNotExist:
         goal_income = "未设置"
         goal_expend = "未设置"
    if goal_income == "未设置":
        return HttpResponse("还未设置星愿计划，请设置后在发送账单")
    context = "亲爱的用户，您好，您的本月消费计划金额："+str(goal_expend)+"元    已经消费："\
              + str(Expendsum)+"元\n 收入计划金额："+str(goal_income)+"元  已经收入："+str(incomesum)\
              + "元\n详情请登录爱记账 爱生活官网查看"

    # 密码已修改
    s = SendMails("smtp.126.com", "hitwh_jzy@126.com", 'JTUCDAVMWE',
                  models.UserInfo.objects.get(user=request.session.get("currentUser")).mail, "星愿计划", context)
    if s.sendE():
        print('提示', '发送成功！')
    else:
        print('提示', '发送失败！')
    return render(request, "menu.html")









