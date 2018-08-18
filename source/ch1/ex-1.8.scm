(define (square x) (* x x))

(define (cube x) (* x x x))

(define (good-enough old_guess new_guess)
  (< (/ (abs (- old_guess new_guess))
        old_guess)
     0.0001))

(define (improve guess x)
  (/ (+ (/ x (square guess)) (* 2 guess)) 3))

(define (cube-root-iter old_guess new_guess x)
  (if (good-enough old_guess new_guess)
      new_guess
      (cube-root-iter new_guess (improve new_guess x) x)))

(define (cube-root x)
  (cube-root-iter 1.0 (improve 1.0 x) x))
