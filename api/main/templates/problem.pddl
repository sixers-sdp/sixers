(define (problem bar)
    (:domain bartending)
    (:objects
		{% for node in locations %}
			{{ node }} - location
		{% endfor %}

		{% for order in orders %}
			{{ order }}	- order
		{% endfor %}
    )

    (:init
		{% for a,b in edges.keys %}
			(adj {{ a }} {{ b }})
		{% endfor %}

		(at {{ current_location }} Albert)

		{% for order in orders %}
            (at {{ chef_location }} {{ order }})
			(awaiting {{ order.location }} {{ order }})
		{% endfor %}
    )

    (:goal (and
        (forall (?c - order) (delivered ?c))

    ))
)