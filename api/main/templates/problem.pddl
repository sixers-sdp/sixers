(define (problem bar)
    (:domain bartending)
    (:objects
		{% for node in locations %}
			{{ node }} - location
		{% endfor %}

		{{ delivery_order }} - delivery
    )

    (:init
		{% for from, to, direction in edges %}
			(edge {{ from }} {{ to }} {{ direction }})
		{% endfor %}

		(at {{ current_location }} Albert)

		(awaiting {{ delivery_order.table_number }} {{ delivery_order }})
        (holding Albert {{ delivery_order }})

    )

    (:goal (and
        (forall (?c - delivery) (delivered ?c))
        (at {{ chef_location }} Albert)
    ))
)