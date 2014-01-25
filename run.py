# This Python file uses the following encoding: utf-8

from flask import Flask, request, redirect, url_for
import twilio.twiml
import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import passpack #so my credentials aren't displayed on github!
 
app = Flask(__name__)
INTRO_URL = "http://k007.kiwi6.com/hotlink/te39eptrpt/intro.mp3"
MENU_URL = "http://k007.kiwi6.com/hotlink/evgbxp77on/menu.mp3"
NASA_URL = "http://k007.kiwi6.com/hotlink/7f6277e67d/NASA.mp3"
PROJECTS_URL = "http://k007.kiwi6.com/hotlink/frxam9caf9/projects.mp3"
CANIDATE_URL_1 = "http://k007.kiwi6.com/hotlink/vhp2s0zni7/candidate.mp3"
CLASSES_URL = "http://k007.kiwi6.com/hotlink/9rahflylrt/classes.mp3"
WOMAN_URL = "http://k007.kiwi6.com/hotlink/tru647ykao/woman.mp3"
# Try adding your own number to this list!

gmail_user = passpack.gmail_email
gmail_pwd = passpack.gmail_password



def mail(to, subject, text, attach):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

@app.route("/intro", methods=['GET', 'POST'])
def hello_monkey():
	# Get the caller's phone number from the incoming Twilio request
	from_number = request.values.get('From', None)
	
	# Create a Response object to send back to Twilio
	resp = twilio.twiml.Response()
	#body = ""
	eml = request.values.get('Body', "")
	
	if (eml != ""):
		body = "Thank you for considering me for the Product Management Internship at Twilio for Summer 2014.\n\n\
I have attached my resume and cover letter to this email. I hope you enjoyed my telephone resume!\n\n\
Joshua Philpott\njphil529@gmail.com\n(386)316-9856\nComputer Engineering, University of South Florida\nUSRP Grant Recipient 2013"

		mail("jphil529@gmail.com",
		"Application to Product Management Internship - Summer 2014 - Joshua Philpott",
		body,
		"joshuaphilpott.pdf")
		resp.sms("Joshua Philpott's resume has been sent to " + str(eml) +". Thank you for your consideration!")
		
	else:
		#Play introduction
		#resp.play("http://k007.kiwi6.com/hotlink/iy4c9y61en/response.mp3")
		resp.play(INTRO_URL)
		#Play introduction
		#resp.say("Hey! It sure is nice getting a call from you. My name is Josh Philpott \
		#		  and I'm a computer engineering student at USF. I saw your position for a \
		#		  Product Management Intern and I think I would be great for the position! Have a listen\
		#		  through this telephone resume and afterwards give me a call! I'd love to chat about what I could \
		#		  do at Twilio. Also, If you'd like my resume sent to another email address\
		#		  send a text with just the email address to this number and the app will automatically send it!")
		#Redirect to menu after the introduction
		resp.redirect("/menu")
		#return the response to Twilio.
	print body
	return str(resp)

@app.route("/menu", methods=['GET', 'POST'])
def menu():
	resp = twilio.twiml.Response()
	#Play the menu twice. If no selection is made either time, Twilio will hang up. If a selection is made, it will redirect to handle-key.

	with resp.gather(numDigits=1, action="/handle-key", method="POST", timeout=10) as g:
		#g.say("To call Josh's cell phone and offer him an internship,\
		#	   press 0 now. To hear why I would be a good candidate\
		#	   for this opportunity, press 1. To hear about my experience\
		#	   interning at NASA's Jet Propulsion Laboratory, press 2. For education and relevant \
		#	   courses, press 3. To hear about some of my projects, press 4.")
		g.play(MENU_URL)
	resp.redirect("/menu")	
	return str(resp)
 
@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
	"""Handle key press from a user."""
	resp = twilio.twiml.Response()
	# Get the digit pressed by the user
	digit_pressed = request.values.get('Digits', None)
	if digit_pressed == "0":
		# Dial  - connect that number to the incoming caller.
		resp.dial(passpack.cellphone) 
		# If the dial fails:
		resp.say("Sorry! Josh was unavailable to take your call. The system will email him and let him know you attempted!")
	elif digit_pressed == "1":
		#resp.say("I think I would be an excellent candidate for the position! I believe\
		#		  Twilio has great potential to expand the market in cloud communications. \
		#		  Using my knowledge of both hardware and software, I believe I can develop\
		#		  unique and creative ways in which the Twilio team could push the product forward.\
		#		  I also come with great recommendations! Listen to this guy!")
		resp.play(CANIDATE_URL_1)
		resp.say("Joshua is an excellent employee, a hard worker, and he has a fantastic personality.")#male robot voice
		#resp.say("And take a listen to what this lively woman has to say")
		resp.play(WOMAN_URL)
		resp.say("Joshua is handsome, has an excellent singing voice, and will definitely be a great\
				  intern at Twilio", voice = "female") #female robot voice
		#back to menu
	elif digit_pressed == "2":
		#resp.say("I had a great opportunity last year to intern at NASA's Jet Propulsion Laboratory. I\
		#		  was selected for two consecutive internships from January to August 2013. I had an opportunity\
		#		  to work with world class engineers in an incredible environment. I made multiple\
		#		  enhancements to an FPGA instrument computing and control platform called ISAAC. I developed\
		#		  an IP core called iFunction that allowed engineers to easily create sinusoidal waveforms for\
		#		  a number of applications. I also designed and helped implement iHub, an interface between spacecraft instrumentation\
		#		  and the ISAAC frameowrk. I made great friends in the industry and fell in love with California.") 
		resp.play(NASA_URL)
	elif digit_pressed == "3":
		#resp.say("I believe that in order to be great at product management, one must have a well rounded foundation\
		#		  in all technical aspects of the product.I am currently a senior in Computer Engineering \
		#		  the University of South Florida and I believe I have gained the foundational knowledge required\
		#		  to understand a complex computer infrastructure, such as the one at Twilio. I have acquired \
		#		  this experience through a diverse set of \
		#		  classes. I have a wide background in software which spans back to when I learned JAVA in high school. In college,\
		#		  expanded upon my knowledge of JAVA and  have began learning the Android libraries. I have also taken\
		#		   classes in C, C++, and Python. I also have a strong foundation\
		#		  in computer hardware which I've gained from classes such as microcontrollers, CMOS-VLSI, and computer systems design. ")
		resp.play(CLASSES_URL)
	elif digit_pressed == "4":
		#resp.say("I've worked on a number of projects in the past year which I think display my growing skills in software\
		#and hardware engineering. Last semester, I worked with a group of students and designed an Application Specific Integrated Circuit(ASIC)\
		#for interfacing a temperature sensor with a seven segment display. We were able to successfully simulate our design and we are\
		#currently waiting for it to be manufactured. I also built a custom UNIX shell and  Process Scheduler last semester for my operating systems class.\
		#I am currently working on an Android App designed to offer immediate tutoring services and group study notifications for College Students. Now, my question is, \
		#What can I work on at Twilio?")	
		resp.play(PROJECTS_URL)	
	resp.redirect("/menu")	
	return str(resp)
		
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, port=port)
	
