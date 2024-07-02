from flask_smorest import Blueprint
from flask.views import MethodView
from flask import redirect

bp = Blueprint("root", "rooth", description="Root route operations")


@bp.route('/')
class Root(MethodView):
    def get(self):
        return redirect('https://itsadeadh2.github.io/commodore-landing/', code=302)
