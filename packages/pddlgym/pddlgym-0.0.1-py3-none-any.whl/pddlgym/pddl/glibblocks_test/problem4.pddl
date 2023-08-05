(define (problem blocks)
    (:domain glibblocks)
    (:objects 
        d - block
        b - block
        a - block
        c - block
        e - block
        robot - robot
    )
    (:init 
        (clear c) 
        (clear a) 
        (clear b) 
        (clear d) 
        (ontable c) 
        (ontable a)
        (ontable b) 
        (ontable e)
        (on d e)
        (handempty robot)

        ; action literals
        (pickup a)
        (putdown a)
        (unstack a)
        (stack a b)
        (stack a c)
        (stack a d)
        (stack a e)
        (pickup b)
        (putdown b)
        (unstack b)
        (stack b a)
        (stack b c)
        (stack b d)
        (stack b e)
        (pickup c)
        (putdown c)
        (unstack c)
        (stack c b)
        (stack c a)
        (stack c d)
        (stack c e)
        (pickup d)
        (putdown d)
        (unstack d)
        (stack d b)
        (stack d c)
        (stack d a)
        (stack d e)
        (pickup e)
        (putdown e)
        (unstack e)
        (stack e b)
        (stack e c)
        (stack e a)
        (stack e d)

    )
    (:goal (and (on a b) (on b c) (on c d) (on d e)))
)
