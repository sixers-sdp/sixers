(define (problem bar-32)
    (:domain bartending)
    (:objects
        BAR - location
        UF - location
        UB - location
        MB - location
        LB  - location
        LF - location
        MF - location

        Customer1 - customer
        Glass1 - glass
        Broom1 - broom
    )

    (:init
        (adj BAR UF)
        (adj UF UB)
        (adj UB MB)
        (adj MB LB)
        (adj LB LF)
        (adj LF MF)
        (adj MF UF)

        (at BAR Agent)
        (at BAR Glass1)
        (at BAR Broom1)
        (empty Glass1)
        (broken-glass MF)
        (broken-glass MB)
        (at LB Customer1)
    )

    (:goal (and
        (forall (?c - customer) (served ?c))
        (forall (?l - location) (not (broken-glass ?l)))
        (at BAR Agent)
    ))
)