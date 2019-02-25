(define (domain bartending)
    (:requirements :adl )

    (:types
        bartender
        location
        order
    )

    (:constants
        Albert - bartender
        BAR - location
    )

    (:predicates
        (holding ?x - object ?y - object)
        (delivered ?x - order)
		(awaiting ?x - location ?y - order)
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
        :parameters (?loc - location ?order - order ?agent - bartender)
        :precondition (and
            (at ?loc ?agent)
            (holding ?agent ?order)
			(awaiting ?loc ?order)
            (not (delivered ?order)))
        :effect (and
            (delivered ?order)
            (not (awaiting ?loc ?order))
            (not (holding ?agent ?order))
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