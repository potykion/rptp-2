import json

from sanic import Sanic, response
from sanic_jinja2 import SanicJinja2

from rptp.auth import VKAuthorizer
from rptp.config import TEMPLATES_DIR
from rptp.cookie import save_token_data
from rptp.getters import get_videos

app = Sanic(__name__)
app.static('/static', './static')
jinja = SanicJinja2(app, pkg_path=TEMPLATES_DIR)


@app.route('/api/videos')
async def video_api_view(request):
    query = request.args.get('query')
    token = request.headers.get('authorization') or request.args.get('token')

    videos = await get_videos(query, token)

    return response.json(videos)


@app.route('/videos')
async def videos_template_view(request):
    template = 'videos.html'

    query = request.args.get('query')

    response_ = await video_api_view(request)
    videos = json.loads(response_.body)

    context = {'query': query, 'videos': videos}

    return jinja.render(template, request, **context)


@app.route('/index')
async def index_template_view(request):
    template = 'index.html'
    context = {}

    code = request.args.get('code')
    authorizer = VKAuthorizer()

    if code:
        user_id, token = await authorizer.auth(code)
        response_ = response.text('oppa')
        response_ = save_token_data(response_, user_id, token)
        return response_
    else:
        auth_link = authorizer.generate_auth_link()
        context.update({'auth_link': auth_link})

        return jinja.render(template, request, **context)
