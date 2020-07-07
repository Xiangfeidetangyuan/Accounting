from django.db import models
# Create your models here.


class UserInfo(models.Model):  # 用户
    user = models.CharField(max_length=32)   # 用户名
    mail = models.CharField(max_length=16)   # 邮箱
    pwd = models.CharField(max_length=32)    # 密码


class ExpendItem(models.Model):  # 支出项目
    ItemUser = models.CharField(max_length=32)   # 用户
    price = models.CharField(max_length=4)       # 金额
    ItemTime = models.CharField(max_length=32)   # 时间
    ItemType = models.CharField(max_length=16)  # 项目的类型
    remarks = models.CharField(max_length=48)   # 备注


class IncomItem(models.Model):  # 收入项目
    ItemUser = models.CharField(max_length=32)   # 用户
    price = models.CharField(max_length=4)       # 金额
    ItemTime = models.CharField(max_length=32)    # 时间
    ItemType = models.CharField(max_length=16)  # 项目的类型
    remarks = models.CharField(max_length=48)   # 备注


class goal_plan(models.Model):   # 星愿计划
    goal_income = models.CharField(max_length=4)  # 目标收入
    goal_expend = models.CharField(max_length=4)  # 目标消费
    goal_User = models.CharField(max_length=32)   # 用户
    goalTime = models.CharField(max_length=32)    # 时间




