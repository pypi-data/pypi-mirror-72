(define (problem rearrangement-notyping) 
    (:domain rearrangement-notyping)

    (:objects
    
	monkey-0
	monkey-1
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
    )

    (:init
    
	(ismonkey monkey-0)
	(ismonkey monkey-1)
	(isrobot robot)
	(at monkey-0 loc-1-0)
	(at monkey-1 loc-0-1)
	(at robot loc-0-2)
	(handsfree robot)

    ; action literals
    
	(pick monkey-0)
	(place monkey-0)
	(pick monkey-1)
	(place monkey-1)
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
    )

    (:goal (and  (at monkey-0 loc-3-2) ))
)
    