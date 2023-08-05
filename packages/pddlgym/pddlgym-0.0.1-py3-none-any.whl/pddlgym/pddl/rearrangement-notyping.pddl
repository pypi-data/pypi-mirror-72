(define (domain rearrangement-notyping)
  (:requirements :strips)
  (:predicates
     (isrobot ?robot)
     (ispawn ?pawn)
     (isbear ?bear)
     (isgoal ?goal)
     (ismonkey ?monkey)
     (at ?obj ?loc)
     (holding ?obj)
     (handsfree ?robot)
     (moveto ?loc)
     (pick ?obj)
     (place ?obj)
  )

  ; (:actions moveto pick place)

  (:action movetonotholding
    :parameters (?robot ?start ?end)
    :precondition (and (moveto ?end)
                       (isrobot ?robot)
                       (handsfree ?robot)
                       (at ?robot ?start)
                  )
    :effect (and (not (at ?robot ?start))
                 (at ?robot ?end)
            )
  )

  (:action movetoholding
    :parameters (?robot ?obj ?start ?end)
    :precondition (and (moveto ?end)
                       (isrobot ?robot)
                       (holding ?obj)
                       (at ?robot ?start)
                       (at ?obj ?start)
                  )
    :effect (and (not (at ?robot ?start))
                 (at ?robot ?end)
                 (not (at ?obj ?start))
                 (at ?obj ?end)
            )
  )

  (:action pick
    :parameters (?robot ?obj ?loc)
    :precondition (and (pick ?obj)
                       (isrobot ?robot)
                       (handsfree ?robot)
                       (at ?robot ?loc)
                       (at ?obj ?loc)
                       (not (isrobot ?obj))
                  )
    :effect (and (holding ?obj)
                 (not (handsfree ?robot))
            )
  )

  (:action place
    :parameters (?robot ?obj)
    :precondition (and (place ?obj)
                       (isrobot ?robot)
                       (holding ?obj)
                  )
    :effect (and (not (holding ?obj))
                 (handsfree ?robot)
            )
  )
)