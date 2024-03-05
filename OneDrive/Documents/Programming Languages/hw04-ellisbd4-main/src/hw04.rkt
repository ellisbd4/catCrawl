
#lang racket

(provide (all-defined-out)) ; So hw04-test-*.rkt files can access the functions.

; Name: Blakely Ellis
; Email: blakely.d.ellis@vanderbilt.edu
; Date: 3/4/24
; Course: CS 3270 - Vanderbilt University
; Honor statement: I have neither given nor recieved unauthorized aid on this assignment.

; Returns a sum calculation based on a number of predefined rules.
; 1) if the number in the list is a zero, then add one to the sum
; 2) if the number in the list is an even number, then add the double of that number to the sum
; 3) if the number in the list is an odd number, then add the square of that number to the sum
;
; @param  lst  the list of integers that the rules will iterate on
; @return the final sum calculation.
(define (my-sum-tr lst)
  (define (my-sum-helper lst acc)
    (if (null? lst) ;if empty, return accumulator
        acc
        (my-sum-helper (cdr lst) ;move to next element
                       (+ acc ;add the result according to the rules
                          (cond [(= (car lst) 0) 1] ;if 0, add 1
                                [(even? (car lst)) (* 2 (car lst))] ;if even, add double
                                [else (expt (car lst) 2)]))))) ;add the square
  (my-sum-helper lst 0)) ;start the helper w the initial list and 0 as the accumulator

; Counts the number of dates in a given month within a list of dates
; Each date in the list is a sublist with three elements: day, month, and year
;
; @param dates A list of dates, each represented as [day month year]
; @param month  The month to count the dates
; @return  The count of dates within the specified month
(define (number-in-month-tr dates month)
  (define (helper dates month acc)
    (if (null? dates)
        acc
        (let ((current-date (car dates)))
          (helper (cdr dates) 
                  month 
                  (if (= month (cadr current-date))
                      (+ 1 acc)
                      acc)))))
  (helper dates month 0))

; Returns a sum calculation based on a number of predefined rules.
; 1) if the number in the list is a zero, then add one to the sum
; 2) if the number in the list is an even number, then add the double of that number to the sum
; 3) if the number in the list is an odd number, then add the square of that number to the sum
;
; @param lst  list of integers to process
; @return the sum of the transformed list
(define (my-sum-mr lst)
  (define (apply-rules n)
    (cond [(= n 0) 1]
          [(even? n) (* 2 n)]
          [else (expt n 2)]))
  (foldl (lambda (x acc) (+ acc x))
         0
         (map apply-rules lst)))



; Powers-of-two function from class.
; Used to test stream-for-n-steps and stream-add-zero.
(define powers-of-two
  (letrec
      ([f (lambda (x)
            (cons x
                  (lambda () (f (* x 2)))))])
    (lambda () (f 2))))

; Evaluates a stream for a specified number of steps and returns a list of the values produced
;
; @param stream The stream to evaluate
; @param n The num of steps to evaluate the stream for
; @return a list of values produced by the stream up to n steps
(define (stream-for-n-steps stream num)
  (if (= num 0)
      '()
      (cons (car (stream))
            (stream-for-n-steps (cdr (stream)) (- num 1)))))

; Creates a stream where natural numbers are incremented by 1 starting from 1
; and numbers divisible by 5 are negated
;
; @param n The starting point for the stream
; @return A thunk representing the stream of natural numbers with every fifth number negated
(define (make-funky-stream n)
  (lambda ()
    (cons (if (= (modulo n 5) 0) (- n) n)
          (make-funky-stream (+ n 1)))))

(define funky-stream (make-funky-stream 1))

; Creates a stream of strings 'if this' and 'then that' being printed back and fourth,
; starting with 'if this'
;
; @param flag  a bool value to determine the starting string of the stream
; @return  a thunk representing the alternating stream of strings
(define (make-this-then-that flag)
  (lambda ()
    (cons (if flag "If this" "Then that")
          (make-this-then-that (not flag)))))
(define this-then-that (make-this-then-that #t))

; Transforms a given stream by adding a zero to each element by producing pairs of 0 . element
;
; @param strm  the given stream we want to transform
; @return  a new stream, each element is a pair with 0 and the original stream element
(define (stream-add-zero strm)
  (lambda ()
    (let ((next (strm)))
      (cons (cons 0 (car next))
            (stream-add-zero (cdr next))))))

