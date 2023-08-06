import re
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from utils import DATETIME_12, WHITESPACE, replace_all, replace_ws, retry_get


def render_templatefile(dst, templatefile, **kwargs):
    env = Environment(loader=FileSystemLoader(
        kwargs.pop('templates_folder', './templates')))
    template = env.get_template(templatefile)
    with open(dst, 'w', encoding='utf-8') as fp:
        fp.write(template.render(**kwargs))


# 可根据实际需求修改部分代码
def genspider(home_url, templatefile, dst, spider, **kwargs):
    response = retry_get(home_url)
    if not response:
        raise Exception('Request failed, invalid URL or parameter.')

    try:
        string = response.content.decode('utf8')
    except UnicodeDecodeError:
        string = response.content.decode('gbk')

    source = re.findall(r'(?is)<title>(.*?)</title>', string)[0]

    # 清理标题中的干扰字符
    clear_chars = kwargs.pop('clear_chars', WHITESPACE)
    source = re.sub(r'\s', '', replace_all(source, clear_chars))

    # 仅供参考，建议自行修改
    kwargs.update({
        'datetime': datetime.now().strftime(DATETIME_12),
        'source': source,
        'home_url': home_url,
        'author': kwargs.pop('author', 'Rustle Karl'),
    })

    spiderfile = f'{dst}/{spider}.py'
    render_templatefile(spiderfile, templatefile, **kwargs)
