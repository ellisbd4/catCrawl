#lang racket

(require "../tests/hw04-test-01.rkt")
(require "../tests/hw04-test-02.rkt")
(require "../tests/hw04-test-03.rkt")
(require "../tests/hw04-test-04.rkt")
(require "../tests/hw04-test-05.rkt")
(require "../tests/hw04-test-06.rkt")
(require "../tests/hw04-test-07.rkt")

(require rackunit)
(require rackunit/text-ui)

; CS 3270 instructor
; Vanderbilt University

; Set up test suite for all tests.
(define all-tests
  (test-suite
   "Homework 4"
   test-exercise-01
   test-exercise-02
   test-exercise-03
   test-exercise-04
   test-exercise-05
   test-exercise-06
   test-exercise-07))

; Run tests.
(run-tests all-tests)