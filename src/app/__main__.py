"""Run local dev server at port 80."""

from app.core import create_app
app = create_app('app.settings')
app.run(host='0.0.0.0', port=80)
