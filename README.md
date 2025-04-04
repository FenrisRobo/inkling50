# inkling50
inkling50 is a notepad-based productivity app designed to increase the user's writing efficiency by enforcing continuous typing via a timer. Stop for too long and... POOF! There goes your work!

YouTube Video Link: https://youtu.be/oKuuKOcC3i0

## Features
- Homepage
  - The homepage allows the user to navigate through the different features of our application: Notepad with Timer and Calendar.
- Notepad with Timer
  - Notepad-like text area that includes text formatting options with copy and paste disabled.
  - At the start of Notepad, the user is required to set the duration of time they will have left to work on the document when the idle of 5 seconds expires. The user will not be able to start working unless they press `Start` on the timer. Typing will then be enabled and the user must continuously type.
  - If the user is idle for more than 5 seconds, the timer they set at the beginning will start.
  - The user has the selected amount of time left to work on the document before typing is disabled, the user is prompted to save the file as a PDF, the text area content deletes, and Notepad with Timer exits.
  - At any time between when the user clicks `Start` and the timer expiration, the user can click `Done!` to stop the timer, export the file as a PDF, and exit Notepad with Timer.
- Calendar
  - A basic monthly view calendar with the ability to view previous and next months.

## Program Flow

When the program first opens, the user will be presented with a homepage. From the left sidebar, the user can click the `calendar` icon to view the calendar within the same window. The `home` icon will return to the starting screen. The `notepad` icon will open the main component of our program: Notepad and Timer.

At the opening of Notepad with Timer, the user will be prompted to set the amount of time that they have left to work on their document after the idle (5 seconds) expires. Once they click `Start`, the timer will not start immediately but rather enable typing and trigger the idle loop. Within the text area while typing is enabled, the user can change the text formatting using the toolbar buttons at the top to help them visually during the writing process. Once the idle expires, the timer begins counting down. When the timer expires, typing will be disabled, the user will be notified and prompted to save as a PDF, the text area content deletes, and Notepad with Timer will exit The user will then be returned to Homepage. At any point from when the user click `Start` and the expiration of the timer, they can click `Done` to reach the same end case.

## Installation

### CS50 TF Instructions

Specifically for the CS50 TFs grading inkling50 (first of all, merry CS50-mas!), the .zip file should contain the raw, source code for notepad.py, timer.py, and inkling50.py. In order to view this code in Visual Studio Code (assuming this is the main IDE that graders are using), the user should unzip the file in their chosen file location. Then, the user should drag the files into the Explorer side of VS Code. By entering into the file location that the notepad.py, timer.py, and inkling50.py (with inkling50.py being the most important as it is the GUI which contains calls to notepad and timer) is downloaded in, the user should run the following commands in the terminal:

To install the required modules  
`pip install -r requirements.txt`  

To start the application  
`flet inkling50.py`


### General Instructions


First/primarily, users must navigate to the inkling50 GitHub page. Prior to doing anything, the user must login to their GitHub account and request permission from Ben Raihane. Upon approval, the user will be able to download the inkling50 repository by clicking on the green "Code" button on the main repository page. The user needs to download the `gui` folder. Once the dropdown menu appears, select Download Zip. Once the user has completed that, they will navigate to the folder that they downloaded the zipped file in and unzip it in another folder location of their choosing (ideally in the same folder they downloaded the original zipped file in). After locating the unzipped folder, the user should drag this folder into an IDE (Integrated Development Environment) like Visual Studio Code. Then, after opening the folder in Visual Studio Code, the user should run the following commands in the terminal:  

To install the required modules  
`pip install -r requirements.txt`  

To start the application  
`flet inkling50.py`

Secondly/alternatively, though the user shouldn't need to download specific releases of inkling50 (as the main repository will continue the newest/fully functional version of the application), the user can choose to do so via two methods. Primarily, on the main repository page, the user should click on "Releases" on the lower right-hand side. A new page should appear, showing releases from newest to oldest. Choose the release you want to download, and click Assets to expand. Click the zip file to download it. Alternatively, on the main repository page, the user can click "Tags" underneath the username. A list of releases should appear from newest to oldest once again. Click the zip file below the tag to download it to the user's device. 

Thirdly/lastly, the method to ensure successful installation include: (1) checking that the inkling50 opens when clicked, (2) there are no security messages/error messages that pops up when clicking on various buttons in the homepage, and (3) there are no conflicts between inkling50 and any existing user program files/packages. 

There you go! The user should have correctly installed inkling50 and will be able to use it without any error/interruption! 

## Usage

### Homepage

The Homepage part of inkling50 contains all the other programs the user will need such as notepad & timer, calendar, and the landing page. The Homepage section also contains a fixed menu on the left side of the window, which has icons that leads the user to the different programs of inkling50 while also allowing them to go back to the landing page if they so choose. Each respective icon correlates to a specific program, with the calendar icon corresponding to calendar, notepad icon corresponding to notepad, timer corresponding to timer, and the home icon corresponding to the landing page. On the landing page, the user will see a greeting which changes according to the user's device time settings along with instructions on how too navigate the inkling50 application.

### Notepad & Timer

The Notepad & Timer part of inkling50 constitutes the main "productivity"/functionalities of inkling50. In combination with the timer, the notepad is a space for the user to type down whatever they need to within the time that they are given while also ensuring that they're doing so in a timely manner. The various basic type-setting functions such as bold, italics, and underline (along with advanced functions that combine said-options and also include highlighting, 'centering' of words', and font color changes) are also implemented in notepad to assist the user in emphasizing or annotating parts of the text they find important or useful to remember/refer to while typing. It is important to note here that copy and paste is disabled in notepad to ensure the user doesn't simply type on another application like Google Docs or Microsoft Word and copy over their work, which would ultimately defeat the purpose of having a timed-writing space. The notepad also automatically disables any further input and deletes the contents of the document once the timer has run out, ensuring that the user can't go back to work on their content after the period has elapsed. It is important to note that once the user's designated time period has fully elapsed, while the contents on the *notepad* will delete, the user will be prompted to save their content as a *PDF* in whichever folder on their device they choose to do so.

The timer itself is also very intuitive. Essentially, to enable editing on notepad, the user must first determine a time period (maximum of 10 minutes) on the inkling50 timer, which will 'start' once the user presses "Start!". It is important to note, though, that the timer doesn't actually start counting down (even though it has started) until the user has gone inactive on the notepad page for too long. Once the timer has started, the user will be able to continuously type until the time period runs out and the notepad is locked. Alternative, if the user feels like they have finished before the timer has ended, they can press the "Done!" button which disables notepad as well. It's important for the user to make sure what they've typed down is exactly what they want; otherwise, there is no method for them to go back and continue working on it. Another aspect to note is that as long as the user is typing continuously, the timer won't begin to count down. However, once the user becomes inactive, the timer will begin counting down without waiting for the user. Thus, it is advisable for the user to mentally prepare for what they are going to type before they actually press "Start!" and enable editing on notepad.  

### Calendar

The Calendar gives the user a monthly view. The user can press the left arrow to go to the previous month and the right arrow to go to the next month. Currently, the calendar helps the user to see the dates of the month and year selected, supporting the "productivity" nature of our program. The current calendar is a basic GUI that we plan to integrate with Notepad and Timer to track writing history in the future.

## FAQs 

- Is there anything that the user can currently do with the calendar?
  - While there is currently no functions that the user can use to interact with the calendar, we will likely implement, in the future, features in the calendar that enable it to both automatically track when the user is on for a session and allow for the user to schedule sessions in the future (i.e., if they used inkling50 three times within a week across three days, the calendar will indicate so. If the user plans to type another time in the future that week, they can also schedule that into the calendar).

- Is there a logging on and off function?
  - inkling50 is meant to operate on one's local machine. While there are certainly plans in the future to integrate sign-on and log-off functions using Google as an API, inkling50, in its current state and given our timeframe, is installed directly onto the user's device, meaning that there is no need for that functionality yet.

- Can I save the notepad's editted/customized text in the PDF?
  - To clarify, the notepad's text-editing features are mainly for the user to use *while* they are typing. As such, they are not intended to be saved for later recall by the user. The save as PDF file is in-case there is something that the user absolutely needs to check. Furthermore, in the future, the 'save as PDF' feature will be used as a means to collect metadata from the user that makes inkling50 more dynamic and interactive.

## Contributors
- Ben Raihane - Homepage & GUI
- Ha Le - Timer, Calendar, DESIGN.md & README.md
- Ryan Whalen - Notepad & README.md 
