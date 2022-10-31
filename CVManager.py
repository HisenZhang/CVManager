import os
import sys
import pprint
import base64
import datetime
from yamldb import YamlDB

if len(sys.argv) != 2:
    print('Usage: CVManager.py PATH_TO_PROFILE')
    sys.exit()


profile = YamlDB(filename=sys.argv[1])
db = YamlDB(filename=os.path.join(
            profile['input.path'], profile['input.data']))

html_string = str()

# pprint.pprint(db.experience)


def img2b64(imgpath):
    with open(imgpath, 'rb') as f:
        return base64.b64encode(f.read()).decode()


def render_html(db, outpath):
    global html_string
    template_loader = jinja2.FileSystemLoader(searchpath="./theme")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "layout.html"
    template = template_env.get_template(template_file)
    html_string = template.render(
        utcnow=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        profile=profile,
        person=db['contact'],
        exp=db['experience'],
        img_string=img2b64(os.path.join(
            profile['input.path'], profile['input.logo'])))

    html_path = outpath + '.html'
    html_file = open(html_path, 'w')
    html_file.write(html_string)
    html_file.close()


def render_pdf(db, outpath):

    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.5in',
        'margin-right': '0.8in',
        'margin-bottom': '0.5in',
        'margin-left': '0.8in',
        'encoding': "UTF-8",
        "dpi": "300",
    }

    if html_string is None:
        render_html(db, outpath)

    pdfkit.from_string(html_string, output_path=outpath + '.pdf',
                       configuration=config, options=options)


outputs = profile['output.type']

if outputs is not None:
    ts = datetime.datetime.today().isoformat().split('T')[0]
    time_dir = ts + '-' + sys.argv[1].split('/')[-1].split('.')[0]
    try:
        os.mkdir(os.path.join(profile['output.path'], time_dir))
    except FileExistsError:
        pass
    outpath = os.path.join(
        profile['output.path'], time_dir, profile['output.filename']+ ' ' +ts)

if 'HTML' in outputs:
    import jinja2
    render_html(db, outpath)
if 'PDF' in outputs:
    import jinja2
    import pdfkit
    render_pdf(db, outpath)
