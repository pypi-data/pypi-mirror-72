Pomodoropie
===========

Pomodoropie is a simple command-line pomodoro clock written in Python. The application allows you to specify
the duration, in minutes, of the work segments, short breaks, and long breaks. Each run of the application
times one session, which consists of four work segments, three short breaks, and one long break. After the
long break, the application closes and the user must rerun the application to start a new session. The default
duration for work segments is 25 minutes. The default for short and long breaks is 5 and 15 minutes respectively.
The application accepts three arguments: `-w` or `--work`, `-s` or `--short`, and `-l` or `--long`. These
represent the duration of each corresponding segment, should the user decide they do not want to use the default
durations.

In between each session, an alert box is displayed to tell the user that the segment is over and how much time
there is in the new segment. The user should only exit the alert box when they are ready to move onto the
next segment of the session. The alert box is powered by Zenity and will appear even if the user is in a different
window. This is to ensure that the user will always know when it is time to break or time to start working.

Pomodoropie may be simple, but it will be handy if you just need a simple time keeping device. Please feel free
to send me an email at jeff.moorhead1@gmail.com with any modification requests.

