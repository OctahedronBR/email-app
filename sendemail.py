import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail


class SendEmail(webapp.RequestHandler):
    def post(self):
        senderEmail = self.request.get("email")
        senderName = self.request.get("name")
        message = self.request.get("message")
        response = ''
        
        if not mail.is_email_valid(senderEmail) or senderName == '' or message == '':
            logging.error('Error sending email, invalid parameter(s).')
            response = '{ "status": "error", "msg" : "Invalid parameters" }'
        else:
            email = mail.EmailMessage(sender="<daniloqueiroz@octahedron.com.br>",subject="Mensagem enviada pelo Site da Octahedron")
            email.to = "contato+site@octahedron.com.br"
            email.body = "Messagem enviada por %s <%s>\n\n%s" % (senderName, senderEmail, message)
            email.send()
            response = '{ "status": "ok", "msg" : "Email Sent" }'
            
        self.response.headers["Content-Type"] = "application/json"
        self.response.out.write(response)


application = webapp.WSGIApplication([('/email', SendEmail)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
