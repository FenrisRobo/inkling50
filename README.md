# inkling50
inkling50 is a notepad-based productivity app designed to increase the user's writing efficiency by enforcing continuous typing via a timer. Stop for too long and... POOF! There goes your work! 

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

### General Instructions

First, users must navigate to the inkling50 GitHub page. Prior to doing anything, the user must login to their GitHub account and request permission from Ben Raihane. Upon approval, the user will be able to download 

[the inkling50 file by directly clicking on the {insert Ben's GUI program name} and, on the file view page, right-click the "Raw" button in the upper right-hand corner and select "Save link as.../Save target as". Once the user has chosen an appropriate location for the file, click Save, with renaming being possible if the user so chooses.]

/

[the entire inkling50 repository by clicking on the green "Code" button on the main repository page. Once the dropdown menu appears, select Download Zip.] 

Though the user shouldn't need to download specific releases of inkling50 (as the main repository will continue the newest/fully functional version of the application), the user can choose to do so via two methods. Primarily, on the main repository page, the user should click on "Releases" on the lower right-hand side. A new page should appear, showing releases from newest to oldest. Choose the release you want to download, and click Assets to expand. Click the zip file to download it. Alternatively, on the main repository page, the user can click "Tags" underneath the username. A list of releases should appear from newest to oldest once again. Click the zip file below the tag to download it to the user's device. 

Secondly, at this point, we'll assume the user has installed [insert Ben's GUI program name/installer] which includes the functionalities of inkling50.py (found in gui), notepad.py, and timer.py (both found in main). 

[This {insert Ben's GUI program name/installer} operates similarly to how a Google Chrome or Epic Games pre-installer works, whereby in order to download the actual application itself, the user must first click on the pre-installer to initiate the downloading process of inkling50's full application. Upon completing the pre-installation process, the user can choose to delete the pre-installer and open the full application, inkling50, by clicking on the feather-pen icon.]

/

[This {insert Ben's GUI program name} is the full, direct inkling50 application. By clicking on the feather-pen icon, the user can open up inkling50.]

Thirdly, if the user optionally chooses on Windows, the user can right-click on the inkling50 icon in their taskbar to pin it there. In the future, instead of having to find the folder that they installed inkling50 in repetitively to open the application, they can directly navigate to the inkling50 icon in their taskbar. If the user is on MacOS, the user can right-click on the inkling50 icon in their Dock to pin it there. The rest of the process is similar to Windows. 

Lastly, because inkling50 is designed to be a desktop application that shouldn't have openly user-accessible code that can be compiled or executed in Visual Studio Code or other Integrated Development Environments (IDEs), the method to ensure successful installation include: (1) checking that the inkling50 opens when clicked, (2) there are no security messages/error messages that pops up when clicking on various buttons in the homepage, and (3) there are no conflicts between inkling50 and any existing user program files/packages. 

There you go! The user should have correctly installed inkling50 and will be able to use it without any error/interruption! 

### CS50 TF Instructions

Specifically for the CS50 TFs grading inkling50 (first of all, merry CS50-mas!), the .zip file should contain the raw, source code for notepad.py, timer.py, and inkling50.py. In order to view this code in Visual Studio Code (assuming this is the main IDE that graders are using), the user should unzip the file in their chosen file location. Then, the user should drag the files into the Explorer side of VS Code. By entering into the file location that the notepad.py, timer.py, and inkling50.py (with inkling50.py being the most important as it is the gui which contains calls to notepad and timer) is downloaded in using one's VS Code terminal, the user should type python inkling50.py to run the code to make sure that everything is working properly.

## Usage

### Homepage

The Hompeage part of inkling50 contains all the other programs the user will need such as notepad & timer, calendar, and the landing page. The Homepage section also contains a fixed menu on the left side of the window, which has icons that leads the user to the different programs of inkling50 while also allowing them to go back to the landing page if they so choose. Each respective icon correlates to a specific program, with the calendar icon corresponding to calendar, notepad icon corresponding to notepad, timer corresponding to timer, and the home icon corresponding to the landing page. On the landing page, the user will see a greeting which changes according to the user's device time settings along with instructions on how too navigate the inkling50 application.

### Notepad & Timer

The Notepad & Timer part of inkling50 constitutes the main "productivity"/functionalities of inkling50. In combination with the timer, the notepad is a space for the user to type down whatever they need to within the time that they are given while also ensuring that they're doing so in a timely manner. The various basic type-setting functions such as bold, italics, and underline (along with advanced functions that combine said-options and also include highlighting, 'centering' of words', and font color changes) are also implemented in notepad to assist the user in emphasizing or annotating parts of the text they find important or useful to remember/refer to while typing. It is important to note here that copy and paste is disabled in notepad to ensure the user doesn't simply type on another application like Google Docs or Microsoft Word and copy over their work, which would ultimately defeat the purpose of having a timed-writing space. The notepad also automatically disables any further input and deletes the contents of the document once the timer has run out, ensuring that the user can't go back to work on their content after the period has elapsed.

The timer itself is also very intuitive. Essentially, to enable editing on notepad, the user must first determine a time period (maximum of 10 minutes) on the inkling50 timer, which will 'start' once the user presses "Start!". It is important to note, though, that the timer doesn't actually start counting down (even though it has started) until the user has gone inactive on the notepad page for too long. Once the timer has started, the user will be able to continuously type until the time period runs out and the notepad is locked. Alternative, if the user feels like they have finished before the timer has ended, they can press the "Done!" button which disables notepad as well. It's important for the user to make sure what they've typed down is exactly what they want; otherwise, there is no method for them to go back and continue working on it. Another aspect to note is that as long as the user is typing continuously, the timer won't begin to count down. However, once the user becomes inactive, the timer will begin counting down without waiting for the user. Thus, it is advisable for the user to mentally prepare for what they are going to type before they actually press "Start!" and enable editing on notepad.  

### Calendar

The Notepad part of inkling50 

## FAQs 



## Contributors
- Ben Raihane - Homepage & GUI
- Ha Le - Timer, Calendar, DESIGN.md & README.md
- Ryan Whalen - Notepad & README.md
