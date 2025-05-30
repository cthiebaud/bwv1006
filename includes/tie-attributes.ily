% tie-attributes.ily - Fixed with global unique IDs + debug logs

#(define global-tie-counter 0)

#(define (find-note-head-in-bound bound-obj)
   "Find a NoteHead grob within or associated with a bound object"
   (cond
    ((not (ly:grob? bound-obj)) #f)
    ((memq 'note-head-interface (ly:grob-interfaces bound-obj))
     bound-obj)
    ((memq 'note-column-interface (ly:grob-interfaces bound-obj))
     (let ((note-heads (ly:grob-object bound-obj 'note-heads)))
       (if (ly:grob-array? note-heads)
           (let ((heads-list (ly:grob-array->list note-heads)))
             (if (pair? heads-list)
                 (car heads-list)
                 #f))
           #f)))
    (else
     (let ((elements (ly:grob-property bound-obj 'elements #f)))
       (if (ly:grob-array? elements)
           (let ((elements-list (ly:grob-array->list elements)))
             (find (lambda (elem) 
                     (and (ly:grob? elem)
                          (memq 'note-head-interface (ly:grob-interfaces elem))))
                   elements-list))
           #f)))))

#(define (safe-add-attribute attrs key value)
   "Add attribute to alist, replacing if it already exists"
   (let ((existing (assoc key attrs)))
     (if existing
         (acons key value (alist-delete key attrs))
         (acons key value attrs))))

#(define (make-tie-grob-engraver)
   "Create an engraver that intercepts Tie grobs with globally unique IDs"
   (lambda (context)
     (let ((note-to-ids (make-hash-table 31)))
       (make-engraver
        (end-acknowledgers
         ((tie-interface engraver grob source-engraver)
          (let* ((left-bound (ly:spanner-bound grob LEFT))
                 (right-bound (ly:spanner-bound grob RIGHT)))
            
            (display (format #f ">>> Tie grob: ~a\n" grob))
            (display (format #f ">>> Left bound: ~a\n" left-bound))
            (display (format #f ">>> Right bound: ~a\n" right-bound))
            
            (when (and left-bound right-bound
                       (ly:grob? left-bound)
                       (ly:grob? right-bound))
              (let ((left-note-head (find-note-head-in-bound left-bound))
                    (right-note-head (find-note-head-in-bound right-bound)))
                
                (display (format #f ">>> Found note heads: left=~a, right=~a\n" left-note-head right-note-head))
                
                (when (and left-note-head right-note-head
                           (ly:grob? left-note-head)
                           (ly:grob? right-note-head))
                  
                  ;; Get globally unique IDs
                  (set! global-tie-counter (+ global-tie-counter 1))
                  (let ((tie-id global-tie-counter))
                    
                    (let ((left-start-id (or (hash-ref note-to-ids left-note-head)
                                             (let ((new-id (format #f "tie-note-~a-start" tie-id)))
                                               (hash-set! note-to-ids left-note-head new-id)
                                               new-id)))
                          (right-end-id (format #f "tie-note-~a-end" tie-id)))
                      
                      (hash-set! note-to-ids right-note-head right-end-id)
                      
                      (display (format #f ">>> Adding tie (global counter=~a): ~a -> ~a\n" global-tie-counter left-start-id right-end-id))
                      
                      (let ((left-attrs (ly:grob-property left-note-head 'output-attributes '())))
                        (set! left-attrs (safe-add-attribute left-attrs "id" left-start-id))
                        (set! left-attrs (safe-add-attribute left-attrs "data-tie-role" 
                                                           (if (assoc "data-tie-role" left-attrs) "both" "start")))
                        (set! left-attrs (safe-add-attribute left-attrs "data-tie-to" (string-append "#" right-end-id)))
                        (ly:grob-set-property! left-note-head 'output-attributes left-attrs))
                      
                      (let ((right-attrs (ly:grob-property right-note-head 'output-attributes '())))
                        (set! right-attrs (safe-add-attribute right-attrs "id" right-end-id))
                        (set! right-attrs (safe-add-attribute right-attrs "data-tie-role"
                                                            (if (assoc "data-tie-role" right-attrs) "both" "end")))
                        (set! right-attrs (safe-add-attribute right-attrs "data-tie-from" (string-append "#" left-start-id)))
                        (ly:grob-set-property! right-note-head 'output-attributes right-attrs))))))))))))))

Tie_grob_engraver = #(make-tie-grob-engraver)