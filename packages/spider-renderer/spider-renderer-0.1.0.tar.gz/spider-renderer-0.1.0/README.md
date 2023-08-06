# 基于 Jinja2 构建模块化爬虫模板系统

懒惰是人类的天性，重复性工作必然令人不胜其烦，哪怕是简单的复制粘贴，还经常担心会不会弄错了。在这个还不到一个月的实习中，我所做的工作就是解析一系列相同主题的网页，写出对应的爬虫程序。

而这些程序，首先由于内部规范，很多字段都是相同的，只需填入相应网站的信息即可；其次很多网站的结构具有相似性，解析方法可以在一定程度上通用。

一开始，我只是复制粘贴，但很快我就开始厌烦了，比如引号经常看不准填外面了、一直手动输入网页信息等等，这些真的无聊又可能输错或者忘记改掉。于是，我开始寻求模板渲染的解决方案。

在学习 *Scrapy* 过程中，我了解到官方就有根据模板生成爬虫的命令：

```shell
$ scrapy genspider -l
Available templates:
  basic
  crawl
  csvfeed
  xmlfeed
 
$ scrapy genspider example example.com
Created spider 'example' using template 'basic'
```

顺藤摸瓜我找到了实现该功能的源码：

```python
def render_templatefile(path, **kwargs):
    with open(path, 'rb') as fp:
        raw = fp.read().decode('utf8')
    content = string.Template(raw).substitute(**kwargs)
    render_path = path[:-len('.tmpl')] if path.endswith('.tmpl') else path
    with open(render_path, 'wb') as fp:
        fp.write(content.encode('utf8'))
    if path.endswith('.tmpl'):
        os.remove(path)
```

于是我就根据该函数设计了自己的爬虫生成函数：

```python
def genspider(area, city, home_url, page_url, all_page, regex, tmpl, dst):
    response = requests.get(home_url)
    string = response.content.decode('utf-8')
    source = re.findall(r'(?is)<title>(.*?)</title>', string)[0]
    tvars = {
        'source': source,
        'area': area,
        'city': city,
        'region': source[:3],
        'home_url': home_url,
        'author': 'Rustle Karl',
        'page_url': page_url,
        'all_page': all_page + 1,
        'regex': regex,
    }
    spider_file = '%s/%s.py' % (dst, name)
    shutil.copyfile(tmpl, spider_file)
    render_templatefile(spider_file, **tvars)
```

然而，过了几天我就又觉得不够方便了。因为我写了不止一个模板，这些不同的模板里却有部分相同的代码，若是这部分相同的代码有所改进，每次都必须复制粘贴多个模板，有时候未即时同步，过一会就忘了哪个是最新部分。

我又开始寻找新的方法，Jinja2 频繁出现在我的搜索结果页里。网上基本都是用 Jinja2 渲染网页的内容，很容易让人觉得它只能渲染 HTML 文件，我没有先入为主地这样认为。于是，我开始学习 Jinja2 的相关知识，尝试边学变实现我所想的功能。具体过程不再赘述，这里就放上我现在已经用了挺久的一些解决方法：

1. **模板渲染函数**

```python
def render_templatefile(dst, tmpl, **kwargs):
    env = Environment(loader=FileSystemLoader(
        kwargs.pop('tmplpath', './templates')))
    template = env.get_template(tmpl)
    with open(dst, 'w', encoding='utf-8') as fp:
        fp.write(template.render(**kwargs))
```

- **dst**：程序生成的位置
- **tmpl**：渲染时使用的模板文件
- **kwargs**：接受多个键值对，用于填充模板，其中 `tmplpath` 参数是模板文件的目录，默认为 `./templates`

2. **程序文件生成函数**

```python
def replace_all(string, words=tuple()):
    for w in words:
        string = string.replace(w, '')
    return string

def genspider(area, city, name, home_url, page_url, all_page, regex, tmpl, dst):
    response = retry_get(home_url)
    if not response:
        raise Exception('Request failed, invalid URL or parameter.')

    try:
        string = response.content.decode('utf8')
    except UnicodeDecodeError:
        string = response.content.decode('gbk')

    _source = re.findall(r'(?is)<title>(.*?)</title>', string)[0]
    words = ('&nbsp;', '-', '_', '()')
    source = re.sub(r'\s', '', replace_all(_source, words))

    tvars = {
        'date': datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'),
        'name': name,
        'source': source,
        'area': area,
        'city': city,
        'region': replace_all(source, list(city))[:3] if name[5] == '0' else '',
        'home_url': home_url,
        'author': 'Rustle Karl',
        'page_url': page_url,
        'all_page': all_page + 1,
        'regex': regex,
    }

    spider = '%s/%s.py' % (dst, name)
    render_templatefile(spider, tmpl, **tvars)
```

- **regex**：是一个正则表达式，用于提取网页的相关信息
- 各种参数都可以根据实际情况增减，这里只是一种参考

3. **填入数据的技巧**

我觉得引号真的挺难选准填入的，所以，对于无法双击全部选中的情况，我用了下面的方法：

```python
home_url = '''
https://www.google.com
'''.strip()
```

## 爬虫模板的编写

模块化爬虫模板系统，我的设想是将程序的模板拆分到最小粒度，比如拆分为固定的头部信息、请求翻页函数、详情页解析等功能部分，然后编写不同的相似网页的解析程序模板，比如表格解析、纯文本解析等的方法，遇到类似网页时只需选取已有的模板进行自由组合即可，而今后遇到新的页面格式，只需编写新的解析部分，放入模板库，解释说明可用的情况。若是多人合作还可以共享模板库，大家一起讨论贡献最好的解析方法。

然而，**这其实还是只能算是我的一个想法，目前我所实现的模板也只是用于自己的工作**，更何况我不太敢向其他人说出自己的想法，或许别人有更好的解决方案而我未尝得知。

我目前的做法是将一个爬虫程序尽可能拆分为独立的模块：

- 头部固定模块 - 包括导入库、自定义的函数和爬虫类的静态属性信息
- 首页解析模块 - 用于解析详情页的链接
- 表格头部模块 - 不同的表格解析方法仍有相同的预处理，因此有必要独立出来
- 表格解析模块 - 不同的表格解析方法都分别作为一个模块
- 文字解析模块 - 纯文本内容的解析，中间可嵌入表格解析等

> 全部的相关代码和模块模板示例，等我将相关数据脱敏后会放到 https://github.com/ffujiawei 上开源。

毫无疑问，编写模板模块是最核心的部分。其中我最希望实现的动态自由组合的功能，仅依靠 Jinja2 似乎无法实现，因为 Jinja2 只能在编写模板时就指定包含或继承，这就必须另外寻求解决方案（也可能我对 Jinja2 的了解还不够深入）。

但由于效益问题（毕竟现在的方法已经基本满足我一开始的诉求了）架构、实现细节等我还没深入构思，我不知道是否有朝一日能够实现这样一个系统，也许吧。