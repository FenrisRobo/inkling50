## Language & Frameworks

For this project, we decided to use **Python**. Although it is slower, the language is easier for all team members to understand and use for this project. 

We used two frameworks for this project: **Flet** and **tkinter**. Both are Python GUI frameworks that provide controls (Flet) and widgets (tkinter) to create desktop applications with cross-compatibility. We decided to use a combination of both frameworks as Flet simplifies the GUI design process with an aesthetically pleasing interface while tkinter is a standard Python framework with more documentation to aid us when we encounter a bug or issue in the main aspect of the project: Notepad.

To establish communication between the two processes (tkinter - Notepad and Flet - Timer), we used a multiprocessing pipe that allows Flet to run in the main thread (the initial thread of execution when the program starts) and tkinter in the daemon thread (background thread that automatically exits when the main thread terminates). Flet is used in the main thread as the Timer controls when the user can start/stop typing and when Notepad can delete the document. If we switched the threads, this would mean Notepad could run without Timer, presenting a logic error and defeating the purpose of our program. The two processes communicate through pipe.send() to send a message, pipe.poll() to check the pipe for messages, and pipe.rcv() to retrieve the message. The message is checked by conditionals to determine the corresponding function to call.

Since Flet is asynchronous (where multiple functions can run concurrently without blocking the main event) and tkinter is synchronous, we often ran into issues of ensuring messages are sent and received immediately during the implementation of Timer. Due to the fast-paced nature of this project, we opted for a compromised option to try our best to optimize both the GUI and functionalities and were able to achieve the proposed program. However, we learned that it would be best for future projects to only use one framework or multiple frameworks of the same nature.

## Homepage (Flet)

## Notepad (tkinter)

## Timer (Flet)

## Calendar (Flet)

