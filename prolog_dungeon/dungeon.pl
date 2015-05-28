% Ryan Baltenberger
% CS 463G Program 5 - Prolog Dungeon

% Example Maze used for testing
maze([[ f,  f,  f,  f,  f],
      [ w,  w,  k,  w,  f],
      [dl,  w,  w,  w,  f],
      [ f,  w,  s,  w,  f],
      [ f,  f,  f,  d,  f]]).

% canWalk
%%
% M - Maze in list form
% X - X-Coordinate for element to check
% Y - Y-Coordinate for element to check
% Key - whether or not the key has been found
% Sword - whether or not the sword has been found
%%
% This predicate checks whether or not the 
% tile at coordinates (X,Y) is walkable
% based on whether or not the key and sword
% have been found and the tile itself.
canWalk(M, X, Y, Key, Sword) :-
	checkelement(M, X, Y, Tile),
	(member(Tile, [f, k, s]);
	(Tile = d, Key);
	(Tile = dl, Sword)).

% checkelement
%%
% M - Maze in list form
% X - X-Coordinate for element to check
% Y - Y-Coordinate for element to check
% Tile - the space type to check for
%%
% This predicate gets the element at 
% coordinate (X,Y) and is true if that
% value is the type of the passed in 
% Tile 
checkelement(M, X, Y, Tile) :-
	nth0(Y, M, Row),
	nth0(X, Row, Tile).

% return
%%
% Position - Position in the maze to check
% CurPath - Currently traversed path
%%
% This predicate checks to see if the 
% tile at the passed in position has 
% already been traversed.
return(Position, CurPath) :-
	member(Position, CurPath).

% adjacent
%%
% M - Maze in list form
% X1 - X-Coordinate for first element
% Y1 - Y-Coordinate for first element
% X2 - X-Coordinate for second element
% Y2 - Y-Coordinate for second element
% Key - whether or not the key has been found
% Sword - whether or not the sword has been found
%%
% This predicate takes in two maze elements
% and checks whether they are adjacent to 
% each other and checks if the second element
% is walkable, is true if the elements are 
% adjacent and walkable.
adjacent(M, X1, Y1, X2, Y2, Key, Sword) :-
  ( Y2 is Y1 + 1; 
	  Y2 is Y1 - 1 ),
	X2 is X1,
	canWalk(M, X2, Y2, Key, Sword).
adjacent(M, X1, Y1, X2, Y2, Key, Sword) :-
  ( X2 is X1 + 1;
	  X2 is X1 - 1),
	Y2 is Y1,
	canWalk(M, X2, Y2, Key, Sword).

% path
%%
% M - Maze in list form
% X1 - X-Coordinate for first element
% Y1 - Y-Coordinate for first element
% X2 - X-Coordinate for second element
% Y2 - Y-Coordinate for second element
% CurPath - Current path through the maze
% [[A,B]|Tail] - Remaining path to the end of maze
% Key - whether or not the key has been found
% Sword - whether or not the sword has been found
%%
% The first path predicate is the base case for 
% when the coordinates of the first and second 
% element are the same. 
% The second path predicate checks the walkability of 
% the first element and checks the adjacency of the 
% second element. It then checks if the second 
% element is already in the current path (keeps from 
% repeating rooms in the maze). Finally, it recursively
% calls itself with the second element and the end of
% maze.
path(M, X2, Y2, X2, Y2, CurPath, [], Key, Sword).
path(M, X1, Y1, X2, Y2, CurPath, [[A,B]|Tail], Key, Sword) :-
	canWalk(M, X1, Y1, Key, Sword),
	adjacent(M, X1, Y1, A, B, Key, Sword),
	\+ return([A,B], CurPath),
	path(M, A, B, X2, Y2, [[A,B]|CurPath], Tail, Key, Sword).

% mazepath
%%
% X1 - X-Coordinate for first element
% Y1 - Y-Coordinate for first element
% Maze - Maze in list form
% Path - Path to be found from (X1,Y1) to (X2,Y2)
%% 
% Main driver predicate for the program.  Calls
% path to find the path from (X1,Y1) to the Dark Lord.
% This is two cases ORed together. The first case is 
% the case of the sword and Dark Lord being accessible
% without the key being needed.  The second case is 
% when a key is needed to proceed through the maze.
% Each of the blocks cover these cases by calling
% the path predicate and appending the returned
% paths together.
mazepath(X1, Y1, Maze, Path) :-
	(
	 (
		checkelement(Maze, SwordX, SwordY, s),
		checkelement(Maze, LordX, LordY, dl),
  	path(Maze, X1, Y1, SwordX, SwordY, [[X1,Y1]], PathToSword, false, false),
	  path(Maze, SwordX, SwordY, LordX, LordY, [[SwordX,SwordY]], PathToLord, false, true),
	  append([[X1,Y1]], PathToSword, Temp),
		append(Temp, PathToLord, Path)
	 );
	 (
		checkelement(Maze, KeyX, KeyY, k),
		checkelement(Maze, SwordX, SwordY, s),
		checkelement(Maze, LordX, LordY, dl),
	  path(Maze, X1, Y1, KeyX, KeyY, [[X1,Y1]], PathToKey, false, false),
	  path(Maze, KeyX, KeyY, SwordX, SwordY, [[KeyX,KeyY]], PathToSword, true, false),
	  path(Maze, SwordX, SwordY, LordX, LordY, [[SwordX,SwordY]], PathToLord, true, true),
	  append([[X1,Y1]], PathToKey, Temp),
		append(Temp, PathToSword, Temp2),
	  append(Temp2, PathToLord, Path)
   )
	).
