(define (problem bar)
    (:domain bartending)
    (:objects
		{% for node in locations %}
			{{ node }} - location
		{% endfor %}

		{% if delivery_order %}
			{{ delivery_order }} - delivery

		{% endif %}
    )

    (:init
		{% for from, to, direction in edges %}
			(edge {{ from }} {{ to }} {{ direction }})
		{% endfor %}

		(at {{ current_location }} Albert)

		(awaiting {{ delivery_order.table_number }} {{ delivery_order }})
		{% if delivery_order %}
	        (holding Albert {{ delivery_order }})
		{% endif %}
    )

    (:goal (and
        (forall (?c - delivery) (delivered ?c))
        (at {{ chef_location }} Albert)
    ))
)