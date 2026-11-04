from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from wtforms.fields.numeric import FloatField

from eapp.models import Category, Product
from eapp import app, db
from flask_admin import Admin


admin = Admin(app=app, name="E-commerce's Admin")


class ProductView(ModelView):
    column_list = ['id', 'name', 'active', 'category_id']
    column_searchable_list = ['name']
    can_export = True
    edit_modal = True
    column_editable_list = ['name']
    column_filters = ['name', 'price']
    form_overrides = {
        'price': FloatField
    }


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(StatsView(name='Thống kê'))