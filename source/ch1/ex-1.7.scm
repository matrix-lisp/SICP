(define (sqrt-iter old_guess new_guess x)
  (if (good-enough? old_guess new_guess)
      new_guess
      (sqrt-iter new_guess (improve new_guess x) x)))

(define (improve guess x)
  (average guess (/ x guess)))

(define (average x y)
  (/ (+ x y) 2))

(define (good-enough? old_guess new_guess)
  (< (/ (abs (- old_guess new_guess))
        old_guess)
     0.0001))

(define (squre x)
  (* x x))

(define (sqrt x)
  (sqrt-iter 1.0 (improve 1.0 x) x))
