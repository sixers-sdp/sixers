(define (problem bar)
    (:domain bartending)
    (:objects
		{% for node in locations %}
			{{ node }} - location
		{% endfor %}

		{% for order in ready_orders %}
			{{ order }}	- delivery
		{% endfor %}
		{% for order in delivery_orders %}
			{{ order }}	- delivery
		{% endfor %}

    )

    (:init
		{% for from, to, direction in edges %}
			(edge {{ from }} {{ to }} {{ direction }})
		{% endfor %}

		(at {{ current_location }} Albert)

		{% for order in ready_orders %}
            (at {{ chef_location }} {{ order }})
			(awaiting {{ order.table_number }} {{ order }})
		{% endfor %}

		{% for order in delivery_orders %}
			(awaiting {{ order.table_number }} {{ order }})
	        (holding Albert {{ order }})
		{% endfor %}

    )

    (:goal (and
        (forall (?c - delivery) (delivered ?c))
        (at {{ chef_location }} Albert)
    ))
)