## Program Flow

When the program first opens, the user will be presented with a homepage. From the sidebar, the user can click the `calendar` icon to view the calendar within the same window. The `home` icon will return to the starting screen. The `notepad` icon will open the main component of our program: Notepad and Timer.

At the opening of Notepad and Timer (which happens concurrently), the user will be prompted to set the amount of time that they have left to work on their document after the idle (5 seconds) expires. Once they click `Start`, the timer will not start immediately but rather send a message to Notepad - tkinter to enable typing and trigger the idle timer. Within the text area while typing is enabled, the user can change the text formatting to help them visually during the writing process. Once the idle expires, the timer begins counting down. When the timer expires, typing will be disabled, the user will be notified and prompted to save as a PDF, the text area content deletes, and `Notepad.py` and `timer.py` exits. The user will then be returned to homepage. At any point from when the user click `Start` and the expiration of the timer, they can click `Done` to reach the same end case.

Since we were not able to fully implement the calendar's track history feature in time (our "Best" outcome), we wanted to provide the user with an opportunity to save their work if desired. We decided to limit the save option to PDF only as this makes it more troublesome to copy and paste as compared to a TXT file. Furthermore, copy and paste is disabled in our program, so the user must begin from scratch when they start over, aligning with our app's purpose.



## Language & Frameworks

For this project, we decided to use **Python**. Although it is slower, the language is easier for all team members to understand and use. 

We used two frameworks: **Flet** and **tkinter**. Both are Python GUI frameworks that provide controls (Flet) and widgets (tkinter) to create desktop applications with cross-compatibility. We decided to use a combination of both frameworks as Flet simplifies the GUI design process with an aesthetically pleasing interface while tkinter is a standard Python framework with more documentation to aid us when we encounter a bug or issue in the main aspect of the project: Notepad.

To establish communication between the two processes (tkinter - Notepad and Flet - Timer), we used a multiprocessing pipe that allows Flet to run in the main thread (the initial thread of execution when the program starts) and tkinter in the daemon thread (background thread that automatically exits when the main thread terminates). Flet is used in the main thread as the Timer controls when the user can start/stop typing and when Notepad can delete the document. If we switched the threads, this would mean Notepad could run without Timer, presenting a logic error and defeating the purpose of our program. The two processes communicate through `pipe.send(msg)` (which is defined in the `send_to_tkinter(message)` function - Flet Timer and `send_to_flet(message)` function - tkinter Notepad) to send a message, `pipe.poll()` to check the pipe for messages, and `pipe.rcv()` to retrieve the message. The message is checked by conditionals to determine the corresponding function to call. Refer to [Communication Flow Between Timer & Notepad](#communication) for explanations of the use of different pipe functions, functions associated with each message, and communication with between the two processes.

Since Flet is asynchronous (where multiple functions can run concurrently without blocking the main event) and tkinter is synchronous, we often ran into issues of ensuring messages are sent and received immediately during the implementation of Timer. Due to the fast-paced nature of this project, we opted for a compromised option to try our best to optimize both the GUI & functionalities and were able to achieve the proposed program. However, we learned that it would be best for future projects to only use one framework or multiple frameworks of the same nature.




## Testing

To test our source code at the command line, please run navigate to the ***directory of the source code** and run this command in your terminal:
   ```pip install -r requirements.txt```

To run all the components of our project (which starts from Homepage):  
```flet inkling50.py```
   - Please ensure that `inkling50.py`, `timer.py`, and `notepad.py` are in the same directory!  

To run the main component of our project (Notepad & timer without Homepage):  
```flet timer.py```  
   - Please ensure that `timer.py` and `notepad.py` are in the same directory!  




## Homepage - inkling50.py (Flet)

The homepage uses the framework Flet to implement the starting screen when the application first opens and is returned to when Notepad and Timer exits.

1. `main(page: ft.Page)` sets up the the GUI for homepage by defining functions that retrieve the necessary data and create the required controls and assign them to the `on_click` event of the corresponding button. The sidebar and content are then added to the page through `page.add()` and the page updates for the user through `load_home()`
2. `ft.app(target=main)` starts the Homepage - Flet application.
3. We decided for our main color to be a certain shade of green and dark mode to be aesthetically pleasing to the user while also not straining their eyes from continuous typing.




## <a name="timer"></a>Timer - timer.py (Flet)

The timer uses the framework Flet to implement a timer that is visible to the user. It works hand-in-hand with Notepad to achieve our goal. For more details regarding notepad.py and flow of communication, please refer to [Notepad - notepad.py](#notepad) and [Communication Flow Between Timer & Notepad](#communication), respectively.

1. The tkinter framework displays differently on Windows and macOS. The `if sys.platform == "darwin":` block is used to ensure cross-compatibility.
2. `start_tkinter(pipe)` creates an object of class `Notepad`, which is a tkinter window, and pass the pipe variable (which is the connection from starting the multiprocessing pipe) to the constructor to enable communication between tkinter and Flet. It then runs the main application loop.
3. `start_flet(pipe)` sets up the timer - Flet side.
   - `send_to_tkinter(message)` sends the `message` passed to it by the caller to tkinter using `pipe.send(message)`. We decided to make it a separate function although it contains only one line to ensure clarity on the sender and receiver as both `notepad.py` and `timer.py` use `pipe.send(message)`.
   - `async def main(page: ft.Page)` is the main function that sets up both the logic and appearance of the timer. We opted to make this and some of its child functions to be `async` or asynchronous as we need multiple functions to run asynchronously without blocking the main loop. 
      - `async def check_pipe()` checks the pipe for any messages from tkinter to Flet and call the corresponding functions. Refer to [Communication Flow Between Timer & Notepad](#communication) for explanations of the different pipe functions, functions associated with each message, and communication with tkinter.
         - `await asyncio.sleep(0.1)` runs the nested-if block inside `check_pipe()` every 0.1 seconds (100 ms)
      - `asyncio.create_task(check_pipe())` schedule the initial task to run `check_pipe()` since the function does not automatically run when the program start without the scheduler.
      - We decided to use `Dropdown` for the timer's user input as it limits the user input to a set of acceptable numbers, preventing malicious input.
      - `async def start_writing(e)` is the action triggered by the `on_click` event of `start_button` . It updates the GUI, call `send_to_tkinter("User started")` to enable typing in Notepad, and print to the command line for debugging purposes
      - `async def start_timer()` is called when Flet receive "Idle expired" from tkinter to start the countdown.
         - We check `stop_count[0] == False` to ensure that the timer has not been stopped by another function (such as `pause_timer()` triggered by the `Done` button or elsewhere in the code.
            - Then, user input is retrieved and converted to int. In the case the user figured out how to enter an invalid input, we used a try-except block around these statements to notify the user of the error when applicable.
            - The UI is updated, call `send_to_tkinter("Timer started")` (this currently does not trigger anything on the tkinter side, but we included this for possible expansion in the future), and print to the command line
            - It calls `await update_timer(minutes_value, seconds_value)` to start the countdown. `await` is necessary as the functional call is inside an `async` function. When `await` is used, the current coroutine pauses and control is returned to the event loop to execute other tasks. Usually, when the awaited task is completed, the coroutine resumes, but we do not have any statements after that.
      - `async def update_timer(minutes_value, seconds_value):` perform the countdown of the timer.
         - It converts the total amount of time set by the user into seconds.
         - The `for` loop steps through each second of total_seconds, performing the logic countdown until it reaches 0 or is broken out of.
            - We check `stop_count[0]` to ensure that the timer has not been stopped by another function (such as `pause_timer()` triggered by the `Done` button or elsewhere in the code.
               - If it is `True`, we update the UI to the original time set and end the function.
               - If it is `False`, we update the UI to the amount of time remaining and execute `await asyncio.sleep(1)` which forces the current coroutine to wait for 1 second to pass by before continuing with the while loop. This is critical because without this, the timer will finishes faster than the set time, creating a logical error.
      - `async def pause_timer(e)` is the action triggered by the `on_click` event of `pause_button` . It updates the GUI, set `stop_count[0] = True` so the `for` loop in `update_timer()` is broken out of at the next iteration, call `send_to_tkinter("Done")` (to disable typing in Notepad, prompt the user to save, delete the document, and exit out of the windows), and print to the command line for debugging purposes
      - `send_to_tkinter("Not started")` ensures typing in Notepad is disabled when the program starts, so the user cannot start working unless they have pressed `Start`.
   - `ft.app(target=main)` starts the Flet application when `start_flet()` is called.
4. In `if __name__ == "__main__":`, we create a pipe to establish inter-process communication between timer - Flet and Notepad - tkinter through `multiprocessing.Pipe()`. We start tkinter in a daemon thread (subthread) and Flet in a main thread. tkinter then join the process to start the communication pipeline. We used a try-finally block to catch any errors when running start_flet()





## <a name="notepad"></a>Notepad - notepad.py (tkinter)

Notepad uses the framework tkinter to implement basic word-processing functionalities and an idle that expires if the user stops typing for more than 5 seconds. It works hand-in-hand with Timer to achieve our goal. For more details regarding timer.py and flow of communication, please refer to [Timer - timer.py](#timer) and [Communication Flow Between Timer & Notepad](#communication), respectively.

1. The tkinter framework displays differently on Windows and macOS. The `if sys.platform == "darwin":` block is used to ensure cross-compatibility.
2. The `Notepad` class inherits from the `Tk` (tkinter) module and encapsulates all the components of the Notepad window. An object of the class `Notepad` is created by timer.py.
   - `super().__init__()` creates a temporary instance of the parent class `Tk` to allow us to leverage its existing functions, such as `after()`.
      - `self.pipe = pipe` assigns the pipe being passed to the constructor to the `pipe` variable of the object and allows for inter-process communication with Flet.
      - `self.running` is used as a flag variable to allow us to terminate check_pipe() when the application quits, effectively stopping communication with Flet.
      - The next few code blocks set up the GUI of Notepad using `ttkbootstrap` either through direct widget classes or helper functions when the aspect is composed of multiple widgets. We used `ttkbootstrap` as it enhances the UI features of tkinter.
      - `self.idle_time_limit = 5000` gives the user 5 seconds of idle activity before the Flet timer is triggered. `self.idle_timer = None` will later be used to reset the idle timer in response to keypress events.
      - `self.check_pipe_id = self.after(100, self.check_pipe)` schedules `check_pipe()` to run every 100 ms so the pipe is continuously checked for incoming messages and timely responses. The returned integer ID is stored to later cancel the task when the application quits.
   - `send_to_flet(self, message)` sends the `message` passed to it by the caller to Flet using `self.pipe.send(message)`. We decided to make it a separate function although it contains only one line to ensure clarity on the sender and receiver as both `notepad.py` and `timer.py` use `pipe.send(message)`.
   - `check_pipe(self)` checks the pipe for any messages from Flet to tkinter and call the corresponding functions. Refer to [Communication Flow Between Timer & Notepad](#commnication) for explanations of the different pipe functions, functions associated with each message, and communication with Flet.
      - `self.after(100, self.check_pipe)` runs the nested-if block inside `check_pipe(self)` every 0.1 seconds (100 ms)
   - `run(self)` is called by timer.py, executing `self.__root.mainloop()` which runs the main application loop. Without this, the Notepad - tkinter side of the program would never start.
   - `__bindEvents(self)` defines a list of key bindings and the associated functions, such as changing text format, updating the word count, and disabling certain actions.
      - We decided to disable copy and paste to prevent any loopholes around the delete document aspect of our program. The user not being able to copy and paste will remove their reliance on being able to just continue the work later in the app and push them to continuously write.
   - `__onKeyPress(self, event)` calls `__resetIdleTimer(self)` which checks if `self.idle_timer` has an integer ID associated with a scheduled event.
      - If `self.idle_timer` does have an integer ID (returns `True`), the idle is canceled as this function was indirectly triggered by a keypress event which means the user is continuously typing.
      - If `self.idle_timer` does not have an integer ID (returns `False`), the idle is started. If 5 seconds of idle activity have passed, a message will be sent to Flet to start the countdown timer until document deletion.
      - However, if the user is continuously typing, the `__resetIdleTimer(self)` will execute again and this time run the `True` condition. This essentially creates a cycle of creating and canceling the idle, effectively resetting the idle of 5 seconds as long as the user continues typing. 
   - `__deleteDocument(self)` is called after receiving a `"Timer expired"` or `"Done"` message from Flet. It disables typing, deletes all the text the user has typed in Notepad, sends a message to Flet to close the timer window, and destroys the tkinter window -- ending the program.
   - `__disableTyping(self)` and `__enableTyping(self)` change whether user input is accepted by changing the configuration state of the TextArea. This further enforces the timer that is an integral part of our program.
   - `__createMenuBar(self)` and `__createToolbar(self)` create the toolbar at the top of Notepad that allows users to change the text formatting to assist them visually during the writing process. We were able to achieve our "Better" outcome of implementing text highlighting and text color, Due to issues with tkinter allowing multiple buttons to be "selected" at once, we had to create additional buttons for a combination of bold, italic, and underline.
   - `__createStatusBar(self)` and `def __updateWordCount(self, event=None)` to implement the word count to inform the user of their progress throughout the work time.
   - `__disableAction(self, event=None)` informs the user that they cannot copy and paste.
   - `__quitApplication(self)` cancels the scheduled tasks, which are checking the pipe for incoming messages and the idle timer, to prevent a memory leak. `self.running = False` also stops `check_pipe()`. The Notepad - tkinter window then closes.
   - `__saveFile(self)` and `__saveAsPDF(self, file)` prompts the user to save their work as a PDF before the program terminates. Since we were not able to fully implement the calendar's track history feature in time, we wanted to provide the user with an opportunity to save their work if desired. However, since it saves as a PDF, this makes it more troublesome to copy and paste as compared to a TXT file. Furthermore, copy and paste is disabled in our program, so the user must begin from scratch when they start over, aligning with our app's purpose.




## <a name="communication"></a>Communication Flow Between Timer (Flet) & Notepad (tkinter)

We use a multiprocessing pipe to establish communication between `timer.py` (main thread) and `notepad.py` (daemon thread). A `Notepad` object (tkinter) is created by ```start_tkinter(pipe)```. A timer object (Flet) is created by `start_flet(pipe)`. The pipe is used to send and receive messages between the two processes. Both the Flet and tkinter processes have `send_to_tkinter(message)` and `send_to_flet(message)` respectively that include `pipe.send()` to send messages to the other process. They both have `check_pipe()` scheduled to run every 100 ms. `if pipe.poll()` checks whether there is data available to be read. If it is true, `pipe.recv()` retrieves the message from the pipe. This message is stored in a variable and runs through an if-elif block to call the corresponding function. Below is the expected flow of communication between the two processes.  
 
 F represents Flet  
 T represents tkinter  
 ** means the event always occurs 

1. **(Timer & notepad opens) F -> T: "Not started"
   - T disable typing in Notepad so that the user can not work unless the timer is started.
     ```self.__disableTyping()```
2. **(User press Start timer) F -> T: "User started"
   - T enable typing in Notepad
   ```self.__enableTyping()```
   - T runs its idle which reset if user starts typing again within 5 seconds
3. (User stopped typing for more than 5 seconds) T -> F: "Idle expired"
   - F starts its timer where the user has the specified amount of time left to work before their work in the text area deletes.
     ```
     stop_count[0] = False
     await start_timer()
     ```
4. (User press Done on timer) F -> T: "Done"
   - T disable typing in Notepad to prevent the user from pressing Done to avoid the timer
   - T calls `__saveFile()` to prompt the user to save their work as PDF (which is not easily copied from)
   - After the user saves the file or presses canceled, T calls `__deleteDocument()` to delete the document and close Notepad
   ```
   self.__disableTyping()
   self.__saveFile()
   self.__deleteDocument()
   ```
5. (Timer ran out) F -> T: "Timer expired"
   - T show info dialog to inform the user
   - T calls `__saveFile()` to prompt the user to save their work as PDF (which is not easily copied from)
   - After the user saves the file or presses canceled, T calls `__deleteDocument()` to delete the document and close Notepad
   ```
   showinfo("Time's up!", "You took too long. Press Ok to save & return home")
   self.__saveFile()
   self.__deleteDocument()
   ```
6. **(__deleteDocument() is called) T -> F: "End"
   - F close the Flet timer window  
     ```page.window.close()```

  
There are 3 possible patterns for the communication flow, referencing the list above:  
- User never triggered the timer (Flet side)
   - 1 -> 2 -> 4 -> 6
- User trigger the timer (Flet side) but press Done
   - 1 -> 2 -> 3 -> 4 -> 6
- User trigger the timer (Flet side) and the timer runs out
   - 1 -> 2 -> 3 -> 5 -> 6




## Calendar - inkling50.py (Flet)

Calendar, which is in our "Best" outcome, uses the framework Flet and is implemented at the top of `inkling50.py`.

1. A Calendar object of name `cal` is created to help with the process of outputting the calendar by providing accurate calendar information (day of the week, leap year, etc.).
2. Dictionaries for weekdays and months map days and months to the according number.  The key `0` is associated with Monday as the `monthdayscalendar()` of cal returns a list of weeks in the specified month of that year, starting with Monday. Thus, having the value `Monday` for the key `0` simplified the process.
3. The `Settings` class is used to set and get the currently selected month and year. We decided to use the `@staticmethod` decorator so the functions belong to class itself and can be called without creating an object of that class. These functions can of course be standalone. However, since they are related to one another, defining them in one class increased the organization of our code.
   - The `update_date(delta: int)` function change the current date based on the clicked arrow. A `delta` value of `1` corresponds to the next month and a value of `-1` corresponds to the previous month. We implemented if-else blocks within each value conditional to ensure wrapping of the month and increasing/decreasing the year accordingly.
4. The `DateGrid` class inherits from the `ft.Column` class, simplifying setting up the calendar display object.
   - In the `__init_` class constructor,  the constructor of the parent class is called to leverage its existing methods, saving us from having to write new functions that were already available.
     - `self.year_month` creates a container for the header of the calendar that includes the currently selected month and year. We used a container as the header contain different controls (IconButton, Container). `self.controls.insert(1, self.year_month)` add the container into the first column, whereby `controls.insert()` was inherited from the parent class.
       - When the user clicks the `IconButton`, the `on_click` event is triggered and the `update_date_grid` function is called to update the calendar display of the previous or next month.
     - `weekday` creates the weekday header. This time, we used a row instead as there is only one control type. It is then added to the first column but below the `self.year_month` object as the line is executed after.
   - `populate_date_grid(self, year: int, month: int)` add each date of the month to the calendar by each week, essentially creating a date grid.
     - `del self.controls[2:]` delete any controls after the month & year header (index 0 in the controls list) and weekday header (index 1). This clears any previously populated rows (in cases when the user clicks the arrow button to move backward or forward) and allow the following statements to correctly add the updated dates.
     - The outer `for` loop iterates through a list of weeks in the current month of the current year in full weeks returned by `cal.monthdayscalendar(year, month)` and create a new row for each week.
     - The iner `for` loop iterates through each day of that week and create & format a container for the GUI. Since day can have the `0`, we included a conditional to not explicitly display that value as there is no date 0.
     - After each row is finished setting up, it is appended to the end of the controls list.
   - `update_date_grid(self, delta: int)` is called when `IconButton` is clicked to update the calendar display to the new month.
     - `Settings.update_date` updates the currently selected month and year in `Settings` based on which arrow button was clicked by the user
     - `self.update_year_month(Settings.get_year(), Settings.get_month())` retrieve the current year & month from Settings and update the month & year header accordingly.
     - `self.populate_date_grid(Settings.get_year(), Settings.get_month())` retrieve the current year & month from Settings and update the date grid accordingly.
     - Once everything has been updated on the backend, `self.update()` reload the page to reflect the changes to the user.
   - `update_year_month(self, year: int, month: int):` ensures the year & month variables in the `DateGrid` class is synchronized with the variables in Settings and the month & year header is updated every time there is a change
5. The `HistoryManager` class inherits from the `ft.Column` class, simplifying setting up the history object. In the class constructor, a temporary object of the parent class is created to inherit its existing functions and a `TextField` control is added to display the currently selected date.

Due to time limitation, we were only able to achieve the base GUI without connecting it with Notepad and Timer to properly record datetime data of document creation and deletion.
