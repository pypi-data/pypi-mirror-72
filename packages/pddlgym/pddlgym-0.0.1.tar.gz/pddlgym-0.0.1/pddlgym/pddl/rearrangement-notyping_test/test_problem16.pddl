(define (problem rearrangement-notyping) 
    (:domain rearrangement-notyping)

    (:objects
    
	pawn-0
	bear-1
	pawn-2
	bear-3
	robot
	loc-0-0
	loc-0-1
	loc-0-2
	loc-0-3
	loc-1-0
	loc-1-1
	loc-1-2
	loc-1-3
	loc-2-0
	loc-2-1
	loc-2-2
	loc-2-3
    )

    (:init
    
	(ispawn pawn-0)
	(isbear bear-1)
	(ispawn pawn-2)
	(isbear bear-3)
	(isrobot robot)
	(at pawn-0 loc-2-0)
	(at bear-1 loc-1-3)
	(at pawn-2 loc-1-3)
	(at bear-3 loc-2-1)
	(at robot loc-1-1)
	(handsfree robot)

    ; action literals
    
	(pick pawn-0)
	(place pawn-0)
	(pick bear-1)
	(place bear-1)
	(pick pawn-2)
	(place pawn-2)
	(pick bear-3)
	(place bear-3)
	(moveto loc-0-0)
	(moveto loc-0-1)
	(moveto loc-0-2)
	(moveto loc-0-3)
	(moveto loc-1-0)
	(moveto loc-1-1)
	(moveto loc-1-2)
	(moveto loc-1-3)
	(moveto loc-2-0)
	(moveto loc-2-1)
	(moveto loc-2-2)
	(moveto loc-2-3)
    )

    (:goal (and  (at pawn-2 loc-2-1) ))
)
    