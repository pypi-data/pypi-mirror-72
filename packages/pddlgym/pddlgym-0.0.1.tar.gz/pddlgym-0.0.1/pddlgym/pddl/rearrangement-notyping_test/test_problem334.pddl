(define (problem rearrangement-notyping) 
    (:domain rearrangement-notyping)

    (:objects
    
	pawn-0
	pawn-1
	pawn-2
	pawn-3
	robot
	loc-0-0
	loc-0-1
	loc-0-2
	loc-1-0
	loc-1-1
	loc-1-2
	loc-2-0
	loc-2-1
	loc-2-2
	loc-3-0
	loc-3-1
	loc-3-2
	loc-4-0
	loc-4-1
	loc-4-2
    )

    (:init
    
	(ispawn pawn-0)
	(ispawn pawn-1)
	(ispawn pawn-2)
	(ispawn pawn-3)
	(isrobot robot)
	(at pawn-0 loc-3-2)
	(at pawn-1 loc-2-2)
	(at pawn-2 loc-2-1)
	(at pawn-3 loc-3-1)
	(at robot loc-0-1)
	(handsfree robot)

    ; action literals
    
	(pick pawn-0)
	(place pawn-0)
	(pick pawn-1)
	(place pawn-1)
	(pick pawn-2)
	(place pawn-2)
	(pick pawn-3)
	(place pawn-3)
	(moveto loc-0-0)
	(moveto loc-0-1)
	(moveto loc-0-2)
	(moveto loc-1-0)
	(moveto loc-1-1)
	(moveto loc-1-2)
	(moveto loc-2-0)
	(moveto loc-2-1)
	(moveto loc-2-2)
	(moveto loc-3-0)
	(moveto loc-3-1)
	(moveto loc-3-2)
	(moveto loc-4-0)
	(moveto loc-4-1)
	(moveto loc-4-2)
    )

    (:goal (and  (at pawn-2 loc-3-0)  (at pawn-3 loc-4-2) ))
)
    