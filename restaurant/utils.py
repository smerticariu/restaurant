from django.core.mail import send_mail, BadHeaderError
def send_m(email, name, title, dish1, dish2, desert, menu_id):

    subject = "Order confirmation"  
    msg = "-> "+" "
    send_mail(subject, msg, "testlunch72@gmail.com", [email])
