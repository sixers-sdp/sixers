(define (domain bartending)
    (:requirements :adl )

    (:types
        bartender
        location
        delivery
    )

    (:constants
        Albert - bartender
    )

    (:predicates
        (holding ?x - object ?y - object)
        (delivered ?x - object)
		(awaiting ?x - location ?y - object)
        (at ?x - location ?y - object)
        (adj ?x - location ?y - location)
    )

    (:action PICKUP
        :parameters (?targ - delivery ?loc - location ?agent - bartender)
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
        :parameters (?loc - location ?ordr - delivery ?agent - bartender)
        :precondition (and
            (at ?loc ?agent)
            (holding ?agent ?ordr)
			(awaiting ?loc ?ordr)
            (not (delivered ?ordr)))
        :effect (and
            (delivered ?ordr)
            (not (awaiting ?loc ?ordr))
            (not (holding ?agent ?ordr))
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