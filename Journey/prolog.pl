route(dublin, cork, 200, "fct").
route(cork, dublin, 200, "fct").
route(cork, corkAirport, 20, "fc").
route(corkAirport, cork, 25, "fc").
route(dublin, dublinAirport, 10, "fc").
route(dublinAirport, dublin, 20, "fc").
route(dublinAirport, corkAirport, 225, "p").
route(corkAirport, dublinAirport, 225, "p").
route(cork, nigeria, 20, "fctp").

mode(f,5,foot).
mode(c,80,car).
mode(t,100,train).
mode(p,500,plane).


journey(S, D ,M) :-
    shortestRoute(S,D,M).

% getting the shortest route possible with your available options of
% transport
shortestRoute(PointA,PointB,MyOption) :-
    existingroutes(PointA,PointB,[],_,_,MyOption),
    findall(TotalTime,existingroutes(PointA,PointB,[],_,TotalTime,MyOption),Lst),
    min_member(Hours,Lst),
    existingroutes(PointA,PointB,[],Route,Hours,MyOption), !,
    concat(Route,Hours).

%finding all possible routes
existingroutes(PointA,PointB,Covered,Routes,Hours,MyOption) :-
    route(PointA,PointB,Distance,Options),
    mode(_,AvgSpeed,_),
    append([PointB,PointA],Covered,R),
    reverse(R,Routes),
    string2list(MyOption,Options,M),
    M \= [],
    quickestOption(M,_,AvgSpeed),
    Hours is Distance / AvgSpeed.
existingroutes(PointA,PointB,Covered,R,Hours,MyOption) :-
    route(PointA,PointC,Distance,Options),
    mode(_,AvgSpeed,_),
    string2list(MyOption,Options,M),
    M \= [],
    quickestOption(M,_,AvgSpeed),
    not(myElem(PointC,Covered)),
    existingroutes(PointC,PointB,[PointA|Covered],R,Time,MyOption),
    Hrs is Distance / AvgSpeed,
    Hours is Time + Hrs.

%getting the quickest option based on the average speed per hour
quickestOption([MyOptions],MyOptions,AvgSpeed) :-
    mode(MyOptions,AvgSpeed,_).
quickestOption([MyOptions|Tail],MyOptions,AvgSpeed) :-
    quickestOption(Tail,_,Speed),
    mode(MyOptions,AvgSpeed,_),
    AvgSpeed > Speed.
quickestOption([MyOptions|Tail],Best,Speed) :-
    quickestOption(Tail,Best,Speed),
    mode(MyOptions,AvgSpeed,_),
    AvgSpeed < Speed.

%turning two strings into two separate lists
string2list(String,String2,Lst) :-
    atom_chars(String,Lst1),
    atom_chars(String2,Lst2),
    intersectOptions(Lst1,Lst2,Lst).

%getting the intersection between two lists
intersectOptions([],_,[]).
intersectOptions([Options|Tail],MyOptions,[Options|M]) :-
    myElem(Options, MyOptions),
    intersectOptions(Tail,MyOptions,M).
intersectOptions([_|Tail], MyOptions, M):-
    intersectOptions(Tail, MyOptions, M).


%MyElem() checks if element is in list.
myElem(X,[X|_]).
myElem(X,[_|XS]) :- myElem(X,XS).

%turning the timetaken into hours
hours(Input, Factor, 0, Remainder) :-
    X is Input - Factor,
    Remainder is Input,
    X < 0, !.
hours(Input,Factor,Overflow,Remainder) :-
    X is Input - Factor,
    hours(X,Factor,Flow,Remainder),
    Overflow is Flow + 1.

%how i want it to be formated and printed out
concat(Route,Input) :-
    hours(Input,0.6,Hours,Min),
    Minutes is round(Min * 100),
    write("Route = "), write(Route),
    write("\n"),
    write("Time = "),write(Hours), write("h "), write(Minutes), write("mins").

