;; Create a list of all possible states
(defun make-state (m w g c) (list m w g c))

;; make side of man the m in state
;; side-of-wolf -> w
;; side-of-goat -> g
;; side-of-cabbage -> c 
(defun side-of-man (state)
  (nth 0 state))
(defun side-of-wolf (state)
  (nth 1 state))
(defun side-of-goat (state)
  (nth 2 state))
(defun side-of-cabbage (state)
  (nth 3 state))

;; this just sets the side to the opposite of what it is
(defun opposite (side)
  (cond
	((equal side 'l) 'r)
	((equal side 'r) 'l)))

;; side-of-goat can't be the same as side-of-wolf
;; side-of-cabbage can't be the same as side-of-goat
;; unsafe if those two rules aren't true
(defun safe (state)
  (cond ((and (equal (side-of-goat state) (side-of-wolf state))
	      (not (equal (side-of-man state) (side-of-wolf state)))) nil)
	(( and (equal (side-of-goat state) (side-of-cabbage state))
	       (not (equal (side-of-man state) (side-of-goat state)))) nil)
	(t state)))

;; Just change man's state
(defun man-moves-alone (state)
  (safe (make-state (opposite (side-of-man state))
		    (side-of-wolf state)
		    (side-of-goat state)
		    (side-of-cabbage state))))

;; change man's state and wolf's state
(defun man-moves-wolf (state)
  (cond ((equal (side-of-man state) (side-of-wolf state))
	 (safe (make-state (opposite (side-of-man state))
			   (opposite (side-of-wolf state))
			   (side-of-goat state)
			   (side-of-cabbage state))))
	(t nil)))

;; change man's state and goat's state
(defun man-moves-goat (state)
  (cond ((equal (side-of-man state) (side-of-goat state))
	 (safe (make-state (opposite (side-of-man state))
			   (side-of-wolf state)
			   (opposite (side-of-goat state))
			   (side-of-cabbage state))))
	(t nil)))

;; change man's state and cabbage's state
(defun man-moves-cabbage (state)
  (cond ((equal (side-of-man state) (side-of-cabbage state))
	 (safe (make-state (opposite (side-of-man state))
			   (side-of-wolf state)
			   (side-of-goat state)
			   (opposite (side-of-cabbage state)))))
	(t nil)))

;; the big one. finds a solve that works
(defun solve-1 (state goal been-list)
  (cond ((null state) nil)
	((equal state goal) (reverse (cons state been-list)))
	((not (member state been-list :test #'equal))
	 (or (solve-1 (man-moves-alone state) goal (cons state been-list))
	     (solve-1 (man-moves-wolf state) goal (cons state been-list))
	     (solve-1 (man-moves-goat state) goal (cons state been-list))
	     (solve-1 (man-moves-cabbage state) goal (cons state been-list))))))

;; the big one. finds a solve that works. slightly different.
(defun solve-2 (state goal been-list)
  (cond ((null state) nil)
        ((equal state goal) (reverse (cons state been-list)))
        ((not (member state been-list :test #'equal))
	 (or (solve-2 (man-moves-alone state) goal (cons state been-list))
	     (solve-2 (man-moves-cabbage state) goal (cons state been-list))
	     (solve-2 (man-moves-goat state) goal (cons state been-list))
	     (solve-2 (man-moves-wolf state) goal (cons state been-list))))))

;; the big function that does it all
(defun find-path-1 (state goal) (solve-1 state goal nil))
(defun find-path-2 (state goal) (solve-2 state goal nil))

;; DO IT!
(print (find-path-1 '(l l l l) '(r r r r))) ;; 1
(print (find-path-2 '(l l l l) '(r r r r))) ;; 2 
