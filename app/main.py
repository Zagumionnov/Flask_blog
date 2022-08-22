from app import app
from app import db # noqa

from auth.blueprint import auth
from posts.blueprint import posts

import view # noqa

app.register_blueprint(auth)
app.register_blueprint(posts, url_prefix='/blog')

if __name__ == '__main__':
    app.run()
