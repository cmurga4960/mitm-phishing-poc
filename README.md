Password Reset Man in the Middle Attack Framework
========================================================


Based of the reseach paper (https://www.ieee-security.org/TC/SP2017/papers/207.pdf), this framework aims to aid in the proccess of a password reset MITM attack.

As cyber awareness is increasing day by day,number of failed phishing attempts is also increasing. Most of the Internet users goes through few check before entering critical information like user name password in an web form.This approach is a kind of an indirect phishing attack.Here instead of asking victims directly their user name and password attacker will put some challenges to victim which Google or any other email service provider gives us while trying to reset the password of his/her Email account. When victim solve those challenges we will take the solution of those challenges from victim and submit it to actual server and successfully reset password in an automated manner. These challenges can be related to answering security questions or SMS based password reset.

Here our main intention is to abuse the same password reset functionality of various email service providers in a smarter and automated manner.We will use selenium and its Python WebDriver api to automate this entire process.Selenium is a software testing framework for web applications. Selenium can automate browser locally or remotely. http://seleniumhq.org/.) We will write a custom selenium web server in python and a dynamic fake survey form in PHP. The fake survey form will communicate with selenium web server using its custom APIs in back end(using PHP curl or something similar thing).

Video Demo
==========

[![IMAGE ALT TEXT HERE](http://edudemic.com/wp-content/uploads/2013/01/youtube.png)](http://www.youtube.com/watch?v=lXNGeURi3hA)

Read Full Article Here
=======================

http://www.debasish.in/2012/07/how-i-can-reset-your-gmail-password_28.html
