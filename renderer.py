from inspect import signature
import jinja2
import pdfkit
import imgkit
import os
import sys
import rsa
from utility import img2b64
import datetime


class RendererFactory:
    def __init__(self, profile):
        self.profile = profile
        pass

    def createRenderers(self, outputTypes):
        if outputTypes is None:
            return None
        renderers = dict()
        for o in set(outputTypes):
            if 'HTML' == o:
                renderers[o] = HTMLRenderer(self.profile)
            elif 'PDF' == o:
                renderers[o] = PDFRenderer(self.profile)
            elif 'PNG' == o:
                renderers[o] = PNGRenderer(self.profile)
            else:
                print('Unknown type ignored:', o)
        return renderers


class BaseRenderer:
    def __init__(self, profile):
        self.ts = datetime.datetime.today().isoformat().split('T')[0]
        self.profile = profile
        self.outpath = self._buildSubDir()
        pass

    def _buildSubDir(self):
        time_dir = self.ts + '-' + os.path.basename(sys.argv[1]).split('.')[0]
        try:
            os.mkdir(os.path.join(self.profile['output.path'], time_dir))
        except FileExistsError:
            pass
        return os.path.join(
            self.profile['output.path'],
            time_dir,
            self.profile['output.filename'] + ' - ' + self.ts)

    def render(self, data, path, time):
        pass

    def sign(self, document):
        if self.profile['input.privatekey']:
            with open(os.path.join(self.profile['input.path'],
                        self.profile['input.privatekey']), mode='rb') as keyfile, \
                    open(document, 'rb') as msgfile, \
                    open(document+'.sig', 'wb') as sigfile:
                privkey = rsa.PrivateKey.load_pkcs1(keyfile.read())
                signature = rsa.sign(msgfile, privkey, 'SHA-256')
                sigfile.write(signature)
                return signature
        else:
            return None


class HTMLRenderer(BaseRenderer):
    def __init__(self, profile):
        super().__init__(profile)
        self.outpath += '.html'

    def render(self, db, profile, time, file=True):
        template_loader = jinja2.FileSystemLoader(searchpath="./theme")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = "layout.html"
        template = template_env.get_template(template_file)
        html_string = template.render(
            utcnow=time,
            profile=profile,
            person=db['contact'],
            exp=db['experience'],
            img_string=img2b64(os.path.join(
                profile['input.path'], profile['input.logo'])))

        if file:
            html_path = self.outpath
            html_file = open(html_path, 'w')
            html_file.write(html_string)
            html_file.close()
            self.sign(self.outpath)

            return self.outpath

        else:
            return html_string


class PNGRenderer(BaseRenderer):
    def __init__(self, profile):
        super().__init__(profile)
        self.outpath += '.png'

    def render(self, db, profile, time, file=True):
        path_to_wkhtmltoimg = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_to_wkhtmltoimg)
        options = {
            'encoding': 'UTF-8',
            'quality': '70',
            'quiet': ''
        }

        html_string = HTMLRenderer(profile).render(db, profile, time, False)
        imgkit.from_string(html_string, output_path=self.outpath,
                           config=config, options=options)

        if file:
            self.sign(self.outpath)

        return self.outpath


class PDFRenderer(BaseRenderer):
    def __init__(self, profile):
        super().__init__(profile)
        self.outpath += '.pdf'

    def render(self, db, profile, time, file=True):
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

        html_string = HTMLRenderer(profile).render(db, profile, time, False)
        pdfkit.from_string(html_string, output_path=self.outpath,
                           configuration=config, options=options)

        if file:
            self.sign(self.outpath)

        return self.outpath
