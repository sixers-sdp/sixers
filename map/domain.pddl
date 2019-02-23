(define (domain bartending)
    (:requirements :adl )

    (:types
        bartender
        location
        glass
        customer
        broom
    )

    (:constants
        ;; You should not need to add any additional constants
        Agent - bartender
        BAR - location
    )

    (:predicates
        ;; Example:
        ;; (Contains ?x - object ?c - container)

        (empty ?x - glass)
        (holding ?x - object ?y - object)
        (served ?x - customer)
        (at ?x - location ?y - object)
        (adj ?x - location ?y - location)
        (broken-glass ?x - location)
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

    (:action DROP
        :parameters (?targ - object ?loc - location ?agent - bartender)
        :precondition (and
            (at ?loc ?agent)
            (holding ?agent ?targ)
        )
        :effect (and
            (not (holding ?agent ?targ))
            (at ?loc ?targ))
    )


    (:action HANDOVER
        :parameters (?c - customer ?l - location ?g - glass ?a - bartender)
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
    (:action POUR
        :parameters (?g - glass ?a - bartender)
        :precondition (and
            (at BAR ?a)
            (holding ?a ?g)
            (empty ?g))
        :effect (and
            (not (empty ?g))
        )
    )
    (:action MOVE
        :parameters (?dest - location ?from - location ?agent - bartender)
        :precondition (and
            (not (broken-glass ?from))
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

    (:action SWEEP
        :parameters (?target - location ?from - location ?agent - bartender ?brm - broom)
        :precondition (and
            (broken-glass ?target)
            (at ?from ?agent)
            (or
                (adj ?target ?from )
                (adj ?from ?target))

            (holding ?agent ?brm)
        )
        :effect (and
            (not (broken-glass ?target))
        )
    )
)