import os
from os.path import join
from reportlab.lib import pdfencrypt
from xhtml2pdf import pisa
from django.conf import settings
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from reportlab.pdfbase import pdfmetrics
from reportlab.rl_config import TTFSearchPath
from reportlab.pdfbase.ttfonts import TTFont

# Only for windows:
# from xhtml2pdf import pisa, default
# from xhtml2pdf.default import DEFAULT_CSS
# from xhtml2pdf.files import pisaFileObject

TTFSearchPath.append(join(settings.BASE_DIR, "oauth", "static", "fonts"))
pdfmetrics.registerFont(TTFont("OpenSans", "OpenSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans-Bold", "OpenSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans-Italic", "OpenSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans-BoldItalic", "OpenSans-BoldItalic.ttf"))
pdfmetrics.registerFontFamily(
    "OpenSans",
    normal="OpenSans",
    bold="OpenSans-Bold",
    italic="OpenSans-Italic",
    boldItalic="OpenSans-BoldItalic",
)


class PdfCreator:
    @classmethod
    def link_callback(cls, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL  # Typically /static/
            sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL  # Typically /media/
            mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception("media URI must start with %s or %s" % (sUrl, mUrl))
        return path

    @classmethod
    def create_pdf(
        cls, template_path, dest=None, dest_bytes=False, context=None, password=None
    ):
        template = get_template(template_path)
        html = template.render(context)

        enc = pdfencrypt.StandardEncryption(password) if password is not None else None

        # Only for windows:
        # default.DEFAULT_CSS = DEFAULT_CSS.replace(
        #     "background-color: transparent;", "", 1
        # )
        # # patch temporary file resolution when loading fonts
        # pisaFileObject.getNamedFile = lambda self: self.uri

        # create a pdf
        return pisa.CreatePDF(
            html,
            dest=dest,
            dest_bytes=dest_bytes,
            link_callback=cls.link_callback,
            encrypt=enc,
        )
