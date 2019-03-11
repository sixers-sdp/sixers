(define (domain bartending)
    (:requirements :adl )

    (:types
        bartender
        location
        delivery
		direction
    )

    (:constants
        Albert - bartender
		north - direction
		east - direction
		west - direction
		south - direction
    )

    (:predicates
        (holding ?x - object ?y - object)
        (delivered ?x - object)
		(awaiting ?x - location ?y - object)
        (at ?x - location ?y - object)
        (edge ?x - location ?y - location ?d - direction)
    )

    (:action PICKUP
        :parameters (?agent - bartender ?targ - delivery ?loc - location)
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
        :parameters (?agent - bartender ?loc - location ?ordr - delivery)
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
        :parameters (?agent - bartender ?dest - location ?from - location ?dir - direction)
        :precondition (and
            (at ?from ?agent)
            (edge ?dest ?from ?dir)
		)
        :effect (and
            (at ?dest ?agent)
            (not (at ?from ?agent))
        )
    )
)