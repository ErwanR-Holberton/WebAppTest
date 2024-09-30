from FlaskApp import *
import requests
prefix = "/Redirect/"

url = "https://as1.ftcdn.net/v2/jpg/01/25/83/12/1000_F_125831282_aJIAvrzGLGjQ436kjbj9Uodory1FBqBb.jpg"
url2 = "https://img.freepik.com/premium-vector/modern-repeating-seamless-pattern-repeat-round-shapes-black-white-circle-dot-stylish-texture_231786-4866.jpg"

def routes():
    @app.route(prefix)
    def Redirect_index():
        return render_template(prefix + "index.html")
    
    @app.route(prefix + '/save_url', methods=['POST'])
    def redirect_save_url():
        global url
        url = request.form.get('url')
        return f"URL saved: {url}. <a href='/'>Go back</a>."
    
    @app.route(prefix + '/get_url', methods=['GET'])
    def redirect_get_url():
        return f"{url}"    
    
    @app.route(prefix + '/save_url2', methods=['POST'])
    def redirect_save_url2():
        global url2
        url2 = request.form.get('url')
        return f"URL saved: {url2}. <a href='/'>Go back</a>."
    
    @app.route(prefix + '/get_url2', methods=['GET'])
    def redirect_get_url2():
        return f"{url2}"
    