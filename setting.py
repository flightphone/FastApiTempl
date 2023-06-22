from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="wwwroot")
def gethtml(filename, params):
    return templates.TemplateResponse(filename, params)  