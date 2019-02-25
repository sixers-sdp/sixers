(define (problem bar-32)
    (:domain bartending)
    (:objects
		{% for node in locations %}
			{{ node.name }} - location
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
            (at BAR {{ order }})
			(awaiting {{ order.location }} {{ order }})
		{% endfor %}
    )

    (:goal (and
        (forall (?c - order) (delivered ?c))
        (at BAR Agent)
    ))
)