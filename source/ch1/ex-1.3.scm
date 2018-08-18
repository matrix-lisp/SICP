;; 定义求最小值的函数, 采用 if 方式实现
(define (min-num a b c)
  (if (< a b)
      (if (< a c) a c)
      (if (< b c) b c)))

;; 利用前面的函数和 cond 表达式实现
(define (sum-max a b c)
  (cond ((= (min-sum a b c) a) (sum-of-squares b c))
        ((= (min-sum a b c) b) (sum-of-squares a c))
        (else (sum-of-squares a b))))
