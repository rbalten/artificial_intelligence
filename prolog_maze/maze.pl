% Ryan Baltenberger
% CS 463G Program 4 - Prolog Maze

% Example maze used for testing
maze([[0, 0, 1, 1, 1, 0],
      [1, 0, 1, 1, 1, 0],
      [1, 0, 1, 1, 1, 0],
      [1, 0, 0, 1, 0, 0],
      [1, 1, 0, 1, 0, 1],
			[1, 1, 0, 1, 0, 1],
      [1, 1, 0, 0, 0, 1]]).

% checkelement
% M - Maze in list form
% X - X-Coordinate for element to check
% Y - Y-Coordinate for element to check
% This predicate gets the element at 
% coordinate (X,Y) and is true if that
% value is 0 (a walkable space)
checkelement(M, X, Y) :-
	nth0(Y, M, Row),
	nth0(X, Row, 0).

% adjacent
% M - Maze in list form
% X1 - X-Coordinate for first element
% Y1 - Y-Coordinate for first element
% X2 - X-Coordinate for second element
% Y2 - Y-Coordinate for second element
% This predicate takes in two maze elements
% and checks whether they are adjacent to 
% each other and checks if the second element
% is walkable, is true if the elements are 
% adjacent and walkable.
adjacent(M, X1, Y1, X2, Y2) :-
  ( Y2 is Y1 + 1; 
	  Y2 is Y1 - 1 ),
	X2 is X1,
	checkelement(M, X2, Y2).
adjacent(M, X1, Y1, X2, Y2) :-
  ( X2 is X1 + 1;
	  X2 is X1 - 1),
	Y2 is Y1,
	checkelement(M, X2, Y2).

% path
% M - Maze in list form
% X1 - X-Coordinate for first element
% Y1 - Y-Coordinate for first element
% X2 - X-Coordinate for second element
% Y2 - Y-Coordinate for second element
% CurPath - Current path through the maze
% [[A,B]|Tail] - Remaining path to the end of maze
% The first path predicate is the base case that 
% prints the path and its length when the coordinates
% for the first and second element are the same. 
% The second path predicate checks the walkability of 
% the first element and checks the adjacency of the 
% second element. It then checks if the second 
% element is already in the current path (keeps from 
% repeating rooms in the maze). Finally, it recursively
% calls itself with the second element and the end of
% maze.
path(M, X2, Y2, X2, Y2, CurPath, []) :-
	length(CurPath, L),
	writeln(CurPath),
	writeln(L).
path(M, X1, Y1, X2, Y2, CurPath, [[A,B]|Tail]) :-
	checkelement(M, X1, Y1),
	adjacent(M, X1, Y1, A, B),
	\+ member([A,B], CurPath),
	path(M, A, B, X2, Y2, [[A,B]|CurPath], Tail).

% mazepath
% X1 - X-Coordinate for first element
% Y1 - Y-Coordinate for first element
% X2 - X-Coordinate for second element
% Y2 - Y-Coordinate for second element
% Maze - Maze in list form
% Path - Path to be found from (X1,Y1) to (X2,Y2)
% Main driver predicate for the program.  Calls
% path to find the path from (X1,Y1) to (X2,Y2)
mazepath(X1, Y1, X2, Y2, Maze, Path) :-
	path(Maze, X1, Y1, X2, Y2, [[X1,Y1]], Path).

