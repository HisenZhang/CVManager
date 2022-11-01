import jinja2
import pdfkit
import os
import sys
from utility import img2b64
import datetime

class RendererFactory:
    def __init__(self,profile):
        self.profile=profile
        pass

    def buildSubDir(self):
        ts = datetime.datetime.today().isoformat().split('T')[0]
        time_dir = ts + '-' + sys.argv[1].split('/')[-1].split('.')[0]
        try:
            os.mkdir(os.path.join(self.profile['output.path'], time_dir))
        except FileExistsError:
            pass
        return os.path.join(
            self.profile['output.path'], time_dir, self.profile['output.filename'] + ' - ' + ts)

    def createRenderers(self,outputTypes):
        outpath = self.buildSubDir()
        renderers = dict()
        for o in set(outputTypes):
            if 'HTML' == o:
                from renderer import HTMLRenderer
                renderers[o] = HTMLRenderer(outpath)              
            elif 'PDF' == o:
                from renderer import PDFRenderer
                renderers[o] = PDFRenderer(outpath)
            else:
                print('Unknown type ignored:',o)            
        return renderers

class BaseRenderer:
    def __init__(self, outpath):
        self.outpath = outpath
        pass

    def render(self,data,path,time):
        pass

class HTMLRenderer(BaseRenderer):
    def __init__(self,outpath):         
        super().__init__(outpath)

    def render(self, db, profile, time):
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
        
        if self.outpath:
            html_path = self.outpath+'.html'
            html_file = open(html_path, 'w')
            html_file.write(html_string)
            html_file.close()

            return self.outpath+'.pdf'

        else:
            return html_string

class PDFRenderer(BaseRenderer):
    def __init__(self,outpath):               
        super().__init__(outpath)

    def render(self, db, profile,time):
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


        html_string = HTMLRenderer(None).render(db, profile, time)
        pdfkit.from_string(html_string, output_path=self.outpath+'.pdf',
                            configuration=config, options=options)

        return self.outpath+'.pdf'                        