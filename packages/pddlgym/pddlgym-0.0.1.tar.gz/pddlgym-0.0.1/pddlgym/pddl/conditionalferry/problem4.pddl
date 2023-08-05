
(define (problem ferry-l10-c8) (:domain conditionalferry)
  (:objects
        c0 - obj
	c1 - obj
	c2 - obj
	c3 - obj
	c4 - obj
	c5 - obj
	c6 - obj
	c7 - obj
	ferry - ferry
	l0 - obj
	l1 - obj
	l2 - obj
	l3 - obj
	l4 - obj
	l5 - obj
	l6 - obj
	l7 - obj
	l8 - obj
	l9 - obj
  )
  (:goal (and
	(at c0 l2)
	(at c1 l5)
	(at c2 l7)
	(at c3 l8)
	(at c4 l7)
	(at c5 l8)
	(at c6 l4)
	(at c7 l9)))
  (:init 
	(at c0 l8)
	(at c1 l0)
	(at c2 l9)
	(at c3 l7)
	(at c4 l4)
	(at c5 l1)
	(at c6 l7)
	(at c7 l0)
	(at-ferry l1)
	(board c0)
	(board c1)
	(board c2)
	(board c3)
	(board c4)
	(board c5)
	(board c6)
	(board c7)
	(board l0)
	(board l1)
	(board l2)
	(board l3)
	(board l4)
	(board l5)
	(board l6)
	(board l7)
	(board l8)
	(board l9)
	(car c0)
	(car c1)
	(car c2)
	(car c3)
	(car c4)
	(car c5)
	(car c6)
	(car c7)
	(empty-ferry ferry)
	(location l0)
	(location l1)
	(location l2)
	(location l3)
	(location l4)
	(location l5)
	(location l6)
	(location l7)
	(location l8)
	(location l9)
	(not-eq l0 l1)
	(not-eq l0 l2)
	(not-eq l0 l3)
	(not-eq l0 l4)
	(not-eq l0 l5)
	(not-eq l0 l6)
	(not-eq l0 l7)
	(not-eq l0 l8)
	(not-eq l0 l9)
	(not-eq l1 l0)
	(not-eq l1 l2)
	(not-eq l1 l3)
	(not-eq l1 l4)
	(not-eq l1 l5)
	(not-eq l1 l6)
	(not-eq l1 l7)
	(not-eq l1 l8)
	(not-eq l1 l9)
	(not-eq l2 l0)
	(not-eq l2 l1)
	(not-eq l2 l3)
	(not-eq l2 l4)
	(not-eq l2 l5)
	(not-eq l2 l6)
	(not-eq l2 l7)
	(not-eq l2 l8)
	(not-eq l2 l9)
	(not-eq l3 l0)
	(not-eq l3 l1)
	(not-eq l3 l2)
	(not-eq l3 l4)
	(not-eq l3 l5)
	(not-eq l3 l6)
	(not-eq l3 l7)
	(not-eq l3 l8)
	(not-eq l3 l9)
	(not-eq l4 l0)
	(not-eq l4 l1)
	(not-eq l4 l2)
	(not-eq l4 l3)
	(not-eq l4 l5)
	(not-eq l4 l6)
	(not-eq l4 l7)
	(not-eq l4 l8)
	(not-eq l4 l9)
	(not-eq l5 l0)
	(not-eq l5 l1)
	(not-eq l5 l2)
	(not-eq l5 l3)
	(not-eq l5 l4)
	(not-eq l5 l6)
	(not-eq l5 l7)
	(not-eq l5 l8)
	(not-eq l5 l9)
	(not-eq l6 l0)
	(not-eq l6 l1)
	(not-eq l6 l2)
	(not-eq l6 l3)
	(not-eq l6 l4)
	(not-eq l6 l5)
	(not-eq l6 l7)
	(not-eq l6 l8)
	(not-eq l6 l9)
	(not-eq l7 l0)
	(not-eq l7 l1)
	(not-eq l7 l2)
	(not-eq l7 l3)
	(not-eq l7 l4)
	(not-eq l7 l5)
	(not-eq l7 l6)
	(not-eq l7 l8)
	(not-eq l7 l9)
	(not-eq l8 l0)
	(not-eq l8 l1)
	(not-eq l8 l2)
	(not-eq l8 l3)
	(not-eq l8 l4)
	(not-eq l8 l5)
	(not-eq l8 l6)
	(not-eq l8 l7)
	(not-eq l8 l9)
	(not-eq l9 l0)
	(not-eq l9 l1)
	(not-eq l9 l2)
	(not-eq l9 l3)
	(not-eq l9 l4)
	(not-eq l9 l5)
	(not-eq l9 l6)
	(not-eq l9 l7)
	(not-eq l9 l8)
	(sail c0)
	(sail c1)
	(sail c2)
	(sail c3)
	(sail c4)
	(sail c5)
	(sail c6)
	(sail c7)
	(sail l0)
	(sail l1)
	(sail l2)
	(sail l3)
	(sail l4)
	(sail l5)
	(sail l6)
	(sail l7)
	(sail l8)
	(sail l9)
))
        