from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from wtforms.fields.numeric import FloatField

from eapp.models import Category, Product, UserRoleEnum
from eapp import app, db, dao
from flask_admin import Admin, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=dao.count_products_by_cate())


admin = Admin(app=app, name="E-commerce's Admin", index_view=MyAdminIndexView())


class AdminView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class BaseAdminView(BaseView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated


class ProductView(AdminView):
    column_list = ['id', 'name', 'active', 'category_id']
    column_searchable_list = ['name']
    can_export = True
    edit_modal = True
    column_editable_list = ['name']
    column_filters = ['name', 'price']
    form_overrides = {
        'price': FloatField
    }


class StatsView(BaseAdminView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(BaseAdminView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(AdminView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))