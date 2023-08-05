
(define (problem mixed-f14-p7-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0) (:domain miconic)
  (:objects
        f0 - floor
	f1 - floor
	f10 - floor
	f11 - floor
	f12 - floor
	f13 - floor
	f2 - floor
	f3 - floor
	f4 - floor
	f5 - floor
	f6 - floor
	f7 - floor
	f8 - floor
	f9 - floor
	p0 - passenger
	p1 - passenger
	p2 - passenger
	p3 - passenger
	p4 - passenger
	p5 - passenger
	p6 - passenger
  )
  (:goal (and
	(served p0)
	(served p1)
	(served p2)
	(served p3)
	(served p4)
	(served p5)
	(served p6)))
  (:init 
	(above f0 f10)
	(above f0 f11)
	(above f0 f12)
	(above f0 f13)
	(above f0 f1)
	(above f0 f2)
	(above f0 f3)
	(above f0 f4)
	(above f0 f5)
	(above f0 f6)
	(above f0 f7)
	(above f0 f8)
	(above f0 f9)
	(above f10 f11)
	(above f10 f12)
	(above f10 f13)
	(above f11 f12)
	(above f11 f13)
	(above f12 f13)
	(above f1 f10)
	(above f1 f11)
	(above f1 f12)
	(above f1 f13)
	(above f1 f2)
	(above f1 f3)
	(above f1 f4)
	(above f1 f5)
	(above f1 f6)
	(above f1 f7)
	(above f1 f8)
	(above f1 f9)
	(above f2 f10)
	(above f2 f11)
	(above f2 f12)
	(above f2 f13)
	(above f2 f3)
	(above f2 f4)
	(above f2 f5)
	(above f2 f6)
	(above f2 f7)
	(above f2 f8)
	(above f2 f9)
	(above f3 f10)
	(above f3 f11)
	(above f3 f12)
	(above f3 f13)
	(above f3 f4)
	(above f3 f5)
	(above f3 f6)
	(above f3 f7)
	(above f3 f8)
	(above f3 f9)
	(above f4 f10)
	(above f4 f11)
	(above f4 f12)
	(above f4 f13)
	(above f4 f5)
	(above f4 f6)
	(above f4 f7)
	(above f4 f8)
	(above f4 f9)
	(above f5 f10)
	(above f5 f11)
	(above f5 f12)
	(above f5 f13)
	(above f5 f6)
	(above f5 f7)
	(above f5 f8)
	(above f5 f9)
	(above f6 f10)
	(above f6 f11)
	(above f6 f12)
	(above f6 f13)
	(above f6 f7)
	(above f6 f8)
	(above f6 f9)
	(above f7 f10)
	(above f7 f11)
	(above f7 f12)
	(above f7 f13)
	(above f7 f8)
	(above f7 f9)
	(above f8 f10)
	(above f8 f11)
	(above f8 f12)
	(above f8 f13)
	(above f8 f9)
	(above f9 f10)
	(above f9 f11)
	(above f9 f12)
	(above f9 f13)
	(board f0 p0)
	(board f0 p1)
	(board f0 p2)
	(board f0 p3)
	(board f0 p4)
	(board f0 p5)
	(board f0 p6)
	(board f10 p0)
	(board f10 p1)
	(board f10 p2)
	(board f10 p3)
	(board f10 p4)
	(board f10 p5)
	(board f10 p6)
	(board f11 p0)
	(board f11 p1)
	(board f11 p2)
	(board f11 p3)
	(board f11 p4)
	(board f11 p5)
	(board f11 p6)
	(board f12 p0)
	(board f12 p1)
	(board f12 p2)
	(board f12 p3)
	(board f12 p4)
	(board f12 p5)
	(board f12 p6)
	(board f13 p0)
	(board f13 p1)
	(board f13 p2)
	(board f13 p3)
	(board f13 p4)
	(board f13 p5)
	(board f13 p6)
	(board f1 p0)
	(board f1 p1)
	(board f1 p2)
	(board f1 p3)
	(board f1 p4)
	(board f1 p5)
	(board f1 p6)
	(board f2 p0)
	(board f2 p1)
	(board f2 p2)
	(board f2 p3)
	(board f2 p4)
	(board f2 p5)
	(board f2 p6)
	(board f3 p0)
	(board f3 p1)
	(board f3 p2)
	(board f3 p3)
	(board f3 p4)
	(board f3 p5)
	(board f3 p6)
	(board f4 p0)
	(board f4 p1)
	(board f4 p2)
	(board f4 p3)
	(board f4 p4)
	(board f4 p5)
	(board f4 p6)
	(board f5 p0)
	(board f5 p1)
	(board f5 p2)
	(board f5 p3)
	(board f5 p4)
	(board f5 p5)
	(board f5 p6)
	(board f6 p0)
	(board f6 p1)
	(board f6 p2)
	(board f6 p3)
	(board f6 p4)
	(board f6 p5)
	(board f6 p6)
	(board f7 p0)
	(board f7 p1)
	(board f7 p2)
	(board f7 p3)
	(board f7 p4)
	(board f7 p5)
	(board f7 p6)
	(board f8 p0)
	(board f8 p1)
	(board f8 p2)
	(board f8 p3)
	(board f8 p4)
	(board f8 p5)
	(board f8 p6)
	(board f9 p0)
	(board f9 p1)
	(board f9 p2)
	(board f9 p3)
	(board f9 p4)
	(board f9 p5)
	(board f9 p6)
	(depart f0 p0)
	(depart f0 p1)
	(depart f0 p2)
	(depart f0 p3)
	(depart f0 p4)
	(depart f0 p5)
	(depart f0 p6)
	(depart f10 p0)
	(depart f10 p1)
	(depart f10 p2)
	(depart f10 p3)
	(depart f10 p4)
	(depart f10 p5)
	(depart f10 p6)
	(depart f11 p0)
	(depart f11 p1)
	(depart f11 p2)
	(depart f11 p3)
	(depart f11 p4)
	(depart f11 p5)
	(depart f11 p6)
	(depart f12 p0)
	(depart f12 p1)
	(depart f12 p2)
	(depart f12 p3)
	(depart f12 p4)
	(depart f12 p5)
	(depart f12 p6)
	(depart f13 p0)
	(depart f13 p1)
	(depart f13 p2)
	(depart f13 p3)
	(depart f13 p4)
	(depart f13 p5)
	(depart f13 p6)
	(depart f1 p0)
	(depart f1 p1)
	(depart f1 p2)
	(depart f1 p3)
	(depart f1 p4)
	(depart f1 p5)
	(depart f1 p6)
	(depart f2 p0)
	(depart f2 p1)
	(depart f2 p2)
	(depart f2 p3)
	(depart f2 p4)
	(depart f2 p5)
	(depart f2 p6)
	(depart f3 p0)
	(depart f3 p1)
	(depart f3 p2)
	(depart f3 p3)
	(depart f3 p4)
	(depart f3 p5)
	(depart f3 p6)
	(depart f4 p0)
	(depart f4 p1)
	(depart f4 p2)
	(depart f4 p3)
	(depart f4 p4)
	(depart f4 p5)
	(depart f4 p6)
	(depart f5 p0)
	(depart f5 p1)
	(depart f5 p2)
	(depart f5 p3)
	(depart f5 p4)
	(depart f5 p5)
	(depart f5 p6)
	(depart f6 p0)
	(depart f6 p1)
	(depart f6 p2)
	(depart f6 p3)
	(depart f6 p4)
	(depart f6 p5)
	(depart f6 p6)
	(depart f7 p0)
	(depart f7 p1)
	(depart f7 p2)
	(depart f7 p3)
	(depart f7 p4)
	(depart f7 p5)
	(depart f7 p6)
	(depart f8 p0)
	(depart f8 p1)
	(depart f8 p2)
	(depart f8 p3)
	(depart f8 p4)
	(depart f8 p5)
	(depart f8 p6)
	(depart f9 p0)
	(depart f9 p1)
	(depart f9 p2)
	(depart f9 p3)
	(depart f9 p4)
	(depart f9 p5)
	(depart f9 p6)
	(destin p0 f4)
	(destin p1 f5)
	(destin p2 f3)
	(destin p3 f2)
	(destin p4 f3)
	(destin p5 f5)
	(destin p6 f11)
	(down f0)
	(down f10)
	(down f11)
	(down f12)
	(down f13)
	(down f1)
	(down f2)
	(down f3)
	(down f4)
	(down f5)
	(down f6)
	(down f7)
	(down f8)
	(down f9)
	(lift-at f0)
	(origin p0 f1)
	(origin p1 f9)
	(origin p2 f1)
	(origin p3 f10)
	(origin p4 f1)
	(origin p5 f2)
	(origin p6 f6)
	(up f0)
	(up f10)
	(up f11)
	(up f12)
	(up f13)
	(up f1)
	(up f2)
	(up f3)
	(up f4)
	(up f5)
	(up f6)
	(up f7)
	(up f8)
	(up f9)
))
        