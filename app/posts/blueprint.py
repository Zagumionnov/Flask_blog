from flask import Blueprint, render_template, redirect, url_for
from models import Post, Tag, User
from .forms import PostForm # noqa
from flask_login import login_required, current_user

from flask import request
from app import db


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/profile')
@login_required
def profile():
    return render_template('posts/profile.html', name=current_user.name)


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        user_id = current_user.id

        try:
            post = Post(title=title, body=body, user_id=user_id)
            db.session.add(post)
            db.session.commit()
        except:
            print('Smth wrong')

        return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)


@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug==slug).first()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('posts.post_detail', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form)


@posts.route('/')
@login_required
def index():

    q = request.args.get('q')
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=5)

    return render_template('posts/index.html', pages=pages)


@posts.route('/all-bloggers')
@login_required
def all_bloggers():

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    users = User.query.filter()

    pages = users.paginate(page=page, per_page=5)

    return render_template('posts/all_bloggers.html', pages=pages)


@posts.route('/blogger/<id>')
@login_required
def user_detail(id):
    user = User.query.filter(User.id==id).first()
    all_posts = user.posts
    return render_template('posts/user_detail.html', user=user, posts=all_posts)


@posts.route('/<slug>')
@login_required
def post_detail(slug):
    post = Post.query.filter(Post.slug==slug).first()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)


@posts.route('/tag/<slug>')
@login_required
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    posts = tag.posts.all()

    return render_template('posts/tag_detail.html', tag=tag, posts=posts)
