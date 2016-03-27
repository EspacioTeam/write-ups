#Amazing

> An important step towards the strong AI is the ability of an
> artificial agent to solve a well-defined problem. A project by the
> name 'amazing' was one of such test problems. It's still up...
> 
> **nc amazing.2016.volgactf.ru 45678**

***Scouting phase***

Use BFS to find all hidden cells reachable from current position. Add them to the stack. Repeat until stack is not empty or until there are no hidden cells on the map.

***Solving phase***

When we scouted all maze, use BFS to find the path to the very right/bottom cell.
Go there and make move to the right.

***Repeat until you get flag***


[solve.py](/2016/volga/Amazing/solve.py)


[First round in bot's eyes](http://pastebin.com/RQmP1EDr)

After 30 rounds I got the flag: 

> VolgaCTF{eurisco!}
