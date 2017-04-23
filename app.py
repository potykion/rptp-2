from flask import Flask, request, redirect, url_for
from jinja2 import Template

from rptp.vk_api import find_videos

DEFAULT_QUERY = 'Jessie Rogers'
DEFAULT_OFFSET = 20

app = Flask(__name__)


def generate_actress():
    return 'Ukraine'


@app.route("/")
def hello():
    if request.args.get('refresh'):
        query = generate_actress()
    else:
        query = request.args.get('query', DEFAULT_QUERY)

    offset = request.args.get('search', 0, type=int)

    count_, videos = find_videos(query, offset=offset).values()

    if not videos:
        return redirect(url_for('hello', refresh=1))

    context = {
        'query': query,
        'count': count_,
        'videos': videos,
        'offset': offset,
        'DEFAULT_OFFSET': DEFAULT_OFFSET
    }

    with open('templates/video.html') as f:
        template = Template(f.read())

    html = template.render(**context)
    return html


if __name__ == "__main__":
    app.run()
