# Flask-hCaptcha

A hCaptcha extension for Flask based on flask-recaptcha.

---

## Install

    pip install flask-hcaptcha

# Usage

### Implementation view.py

    from flask import Flask
    from flask_hcaptcha import hCaptcha

    app = Flask(__name__)
    hcaptcha = hCaptcha(app)
    
    #or 
    
    hcaptcha = hCaptcha()
    hcaptcha.init_app(app)
    

### In your template: **{{ hcaptcha }}**

Inside of the form you want to protect, include the tag: **{{ hcaptcha }}**

It will insert the code automatically


    <form method="post" action="/submit">
        ... your field
        ... your field

        {{ hcaptcha }}

        [submit button]
    </form>


### Verify the captcha

In the view that's going to validate the captcha

    from flask import Flask
    from flask_hcaptcha import hCaptcha

    app = Flask(__name__)
    hcaptcha = hCaptcha(app)

    @route("/submit", methods=["POST"])
    def submit():

        if hcaptcha.verify():
            # SUCCESS
            pass
        else:
            # FAILED
            pass


## Api

**hCaptcha.__init__(app, site_key, secret_key, is_enabled=True)**

**hCaptcha.get_code()**

Returns the HTML code to implement. But you can use
**{{ hcaptcha }}** directly in your template

**hCaptcha.verfiy()**

Returns bool

## In Template

Just include **{{ hcaptcha }}** wherever you want to show the hcaptcha


## Config

Flask-ReCaptcha is configured through the standard Flask config API.
These are the available options:

**HCAPTCHA_ENABLED**: Bool - True by default, when False it will bypass validation

**HCAPTCHA_SITE_KEY** : Public key

**HCAPTCHA_SECRET_KEY**: Private key

    RECAPTCHA_ENABLED = True
    RECAPTCHA_SITE_KEY = ""
    RECAPTCHA_SECRET_KEY = ""

---

(c) 2020 Knugi (originally ReCaptcha by Mardix 2015)

