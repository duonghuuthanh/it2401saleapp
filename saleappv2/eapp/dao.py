from eapp.models import Category, Product, User
from eapp import app, db
import hashlib
from sqlalchemy import func

def load_categories():
    return Category.query.order_by('id').all()

def load_products(kw=None, cate_id=None, page=1):
    query = Product.query

    if kw:
        query = query.filter(Product.name.contains(kw))

    if cate_id:
        query = query.filter(Product.category_id==int(cate_id))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size

    return query.order_by('id').slice(start, start + page_size).all()

def count_products():
    return Product.query.count()

def authenticate(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username==username.strip(), User.password==password).first()

def get_user_by_id(id):
    return User.query.get(id)

def count_products_by_cate():
    return (db.session.query(Category.id, Category.name, func.count(Product.id))
            .join(Product, Product.category_id==Category.id, isouter=True).group_by(Category.id).all())


if __name__ == '__main__':
    with app.app_context():
        print(count_products_by_cate())