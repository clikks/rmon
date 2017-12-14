"""
rmon.view.index

index view
"""

from flask import render_template
from flask.views import MethodView


class IndexView(MethodView):
    """ index view
    """

    def get(self):
        """render model
        """

        return render_template('index.html')

