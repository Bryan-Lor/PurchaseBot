# PurchaseBot
A Simple Bot That Finds Products

## IMPORTANT ---------------------------------------------------------------------
This Program was not meant to be used for mass purchasing items. Although it can be used to buy multiple
products at once, it was only designed for you to make one purchase at a time. (You can work around this by
running multiple Bots at once without any chrome profile. Although you have to log in to every website each time you start the program).


## Installation ---------------------------------------------------------------------
	1. Install Python 3.6+ (3.9 Recommended)

	2. Install Selenium for Python via PIP

	3. Ready To Use Purchase Bot!


## How To Use ---------------------------------------------------------------------
	1. Update the Chrome Path in the py file to your chrome user data location
		-Typically C:\\Users\\<NAMEHERE>\AppData\\Local\\Google\\Chrome\\User Data
	
	2. Enter your information in the pi.txt

	3. Enter the URL Link(s) in the Websites.txt
		-It is recommended to keep the amount of links per bot low (Recommended Amount: 3)!

	4. For each unique Website you have in your websites, create a .txt file containing the element data in the PurchaseBot\data folder
		-Use the template given to you! Copy and paste it, then rename it to 'yourwebsitename.com'
		-Enter all the elements and information into the file
			-You can find the information needed by inspecting the website and retrieving the element data
		-save the .txt file

	5. Run the bot!


## Known Website Compatibility Issues----------------------------------------------------------------
Below are the currently known websites that don't work well or at all <br />
- Walmart.com (NOT WORKING: Has a captcha that appears after refreshing multiple times)<br />
- Samsclub.com (NOT WORKING: Has a Anti-Bot feature upon arrival and after refreshing multiple times.)<br />
- Direct.playstation.com (NOT WELL: Has a captcha that can appear upon arrival. Simply Do it yourself before running the bot with WaitUntilReady enabled in 		'Settings.txt')<br />


## Known Limitations ---------------------------------------------------------------------
This Bot will not bypass Captchas, any website with anti-bot catpchas will NOT work!<br />
This Program DOES NOT SCALE WELL with high numbers of websites! Keep Your Numbers LOW! The more tabs you have, the more CPU Processing and Memory is required!!!<br />
- Since it runs on Google Chrome, this program is dependent on how fast your CPU is and how much RAM you have<br />
- Unless your computer can handle it, IT'S STRONGLY RECOMMENDED TO AVOID RUNNING ANY INTENSIVE PROGRAMS (SUCH AS VIDEO GAMES) ALONGSIDE THIS PROGRAM!!!<br />

