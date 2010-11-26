;; James Dennis
;; Number Theory
;; 6.7.04
;; 
;; Program code to find z values where: z1^5 + z2^5 + z3^5 + z4^5 = n^5
;; 
;; First set of numbers it finds are 27, 84, 110, and 133

(require (lib "etc.ss"))
(require (lib "list.ss"))

(define max-num 1000000)
(define min-num 2)
(define var-num 4)

(define root5?
  (let ([table (make-hash-table 'equal)]
        [max -1]
        [max-expt -1])
    (define (up-to m)
      (unless (<= m max-expt)
	      (let loop ([i (add1 max)])
		(let ([e (expt i 5)])
		  (hash-table-put! table e #t)
		  (if (< e m)
		      (loop (add1 i))
		      (begin (set! max i)
			     (set! max-expt e)))))))
    (lambda (e)
      (up-to e)
      (hash-table-get table e (lambda () #f)))))

(define (solution? l)
  (root5? (foldl (lambda (n acc) (+ acc (expt n 5))) 0 l)))

(define all-combos
  (letrec ([all-combos
            (lambda (n max so-far)
              (if (zero? n)
		  (let ([ok? (solution? so-far)])
		    (when (zero? (random 10000))
			  (let loop ([l so-far])
			    (if (null? (cdr l))
				(printf "~s...\n" (car l))
				(loop (cdr l)))))
		    (when ok? (printf ">>> ~s -> ~s\n" so-far ok?)))
		  (let loop ([i min-num])
		    (unless (< max i)
			    (all-combos (sub1 n) i (cons i so-far))
			    (loop (add1 i))))))])
    (lambda () (all-combos var-num max-num '()))))

(all-combos)
