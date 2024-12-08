## Language & Frameworks

For this project, we decided to use **Python**. Although it is slower, the language is easier for all team members to understand and use. 

We used two frameworks: **Flet** and **tkinter**. Both are Python GUI frameworks that provide controls (Flet) and widgets (tkinter) to create desktop applications with cross-compatibility. We decided to use a combination of both frameworks as Flet simplifies the GUI design process with an aesthetically pleasing interface while tkinter is a standard Python framework with more documentation to aid us when we encounter a bug or issue in the main aspect of the project: Notepad.

To establish communication between the two processes (tkinter - Notepad and Flet - Timer), we used a multiprocessing pipe that allows Flet to run in the main thread (the initial thread of execution when the program starts) and tkinter in the daemon thread (background thread that automatically exits when the main thread terminates). Flet is used in the main thread as the Timer controls when the user can start/stop typing and when Notepad can delete the document. If we switched the threads, this would mean Notepad could run without Timer, presenting a logic error and defeating the purpose of our program. The two processes communicate through `pipe.send(msg)` (which is defined in the `send_to_tkinter(msg)` function - Flet Timer and `send_to_flet(msg)` function - tkinter Notepad) to send a message, `pipe.poll()` to check the pipe for messages, and `pipe.rcv()` to retrieve the message. The message is checked by conditionals to determine the corresponding function to call.

Since Flet is asynchronous (where multiple functions can run concurrently without blocking the main event) and tkinter is synchronous, we often ran into issues of ensuring messages are sent and received immediately during the implementation of Timer. Due to the fast-paced nature of this project, we opted for a compromised option to try our best to optimize both the GUI & functionalities and were able to achieve the proposed program. However, we learned that it would be best for future projects to only use one framework or multiple frameworks of the same nature.

## Testing

To test our source code at the command line, please install the following modules:

1. Flet  
   ```pip install flet```
2. tkinter  
   ```pip install tkinter```
3. ttkbootstrap  
   ```pip install ttkbootstrap```
4. fpdf  
   ```pip install fpdf```

To run all the components of our project (which starts from Homepage):  
```flet inkling50.py```

To run the main component of our project (Notepad & timer without Homepage):  
```flet timer.py```  
   - Please ensure that `timer.py` and `notepad.py` are in the same directory!  

## Homepage - inkling50.py (Flet)

## Notepad - notepad.py (tkinter)

Notepad uses the framework tkinter to implement basic word-processing functionalities and an idle timer that expires if the user stops typing for more than 5 seconds.

1. The tkinter framework displays differently on Windows and macOS. The `if sys.platform == "darwin":` block is used to ensure cross-compatibility.
2. The `Notepad` class inherits from the Tk (tkinter) module and encapsulates all the components of the Notepad window. An object of the class `Notepad` is created by timer.py.
   - sd

## Timer - timer.py (Flet)

## Communication Flow Between Timer & Notepad

We use a multiprocessing pipe to establish communication between `timer.py` (main thread) and `notepad.py` (daemon thread). A `Notepad` object (tkinter) is created by ```start_tkinter(pipe)```. A timer object (Flet) is created by `start_flet(pipe)`. The pipe is used to send and receive messages between the two processes. Both the Flet and tkinter processes have `send_to_tkinter(msg)` and `send_to_flet(msg)` respectively that include `pipe.send()` to send messages to the other process. They both have `check_pipe()` scheduled to run every 100 ms. `if pipe.poll()` checks whether there is data available to be read. If it is true, `pipe.recv()` retrieves the message from the pipe. This message is stored in a variable and runs through an if-elif block to call the corresponding function. Below is the expected flow of communication between the two processes.  
 
 F represents Flet  
 T represents tkinter  
 ** means the event always occurs 

1. **(Timer & notepad opens) F -> T: "Not started"
   - T disable typing in Notepad so that the user can not work unless the timer is started.
2. **(User press Start timer) F -> T: "User started"
   - T enable typing in Notepad
   - T runs its own idle timer which reset if user starts typing again within 5 seconds**
3. (User stopped typing for more than 5 seconds) T -> F: "Idle expired"
   - F starts its timer where the user has the specified amount of time left to work before their work in the text area deletes.
4. (User press Done on timer) F -> T: "Done"
   - T disable typing in Notepad to prevent the user from pressing Done to avoid the timer
   - T calls `__saveFile()` to prompt the user to save their work as PDF (which is not easily copied from)
   - After the user saves the file or presses canceled, T calls `__deleteDocument()` to delete the document and close Notepad
5. (Timer ran out) F -> T: "Timer expired"
   - T show info dialog to inform the user
   - T calls `__saveFile()` to prompt the user to save their work as PDF (which is not easily copied from)
   - After the user saves the file or presses canceled, T calls `__deleteDocument()` to delete the document and close Notepad
6. **(__deleteDocument() is called) T -> F: "End"
   - F close the Flet timer window  
  
There are 3 possible patterns for the communication flow, referencing the list above:  
- User never triggered the timer - Flet side
   - 1 -> 2 -> 4 -> 6
- User trigger the timer - Flet side but press Done
   - 1 -> 2 -> 3 -> 4 -> 6
- User trigger the timer - Flet side and the timer runs out
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
