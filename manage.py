from jobweb.app import create_app

app = create_app('development')

if __name__ =='__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app=ProxyFix(app.wsgi_app)
    app.run()
