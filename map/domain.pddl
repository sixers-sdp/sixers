(define (domain bartending)
    (:requirements :adl )

    (:types
        bartender
        location
        order
        customer
    )

    (:constants
        Albert - bartender
        BAR - location
    )

    (:predicates
        (empty ?x - order)
        (holding ?x - object ?y - object)
        (served ?x - customer)
        (at ?x - location ?y - object)
        (adj ?x - location ?y - location)
    )

    (:action PICKUP
        :parameters (?targ - object ?loc - location ?agent - bartender)
        :precondition (and
            (at ?loc ?targ)
            (at ?loc ?agent)
            (not (exists (?any_item - object) (holding ?agent ?any_item)))
        )
        :effect (and
            (holding ?agent ?targ)
            (not (at ?loc ?targ)))
    )

    (:action HANDOVER
        :parameters (?c - customer ?l - location ?g - order ?a - bartender)
        :precondition (and
            (at ?l ?c)
            (at ?l ?a)
            (holding ?a ?g)
            (not (empty ?g))
            (not (served ?c)))
        :effect (and
            (served ?c)
            (not (holding ?a ?g))
        )
    )

    (:action MOVE
        :parameters (?dest - location ?from - location ?agent - bartender)
        :precondition (and
            (at ?from ?agent)
            (or
                (adj ?dest ?from )
                (adj ?from ?dest))
            )
        :effect (and
            (at ?dest ?agent)
            (not (at ?from ?agent))
        )
    )
)