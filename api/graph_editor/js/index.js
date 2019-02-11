var data = {
    "nodes": [
        {
            "id": 0,
            "x": 80,
            "y": 98,
            "width": 20,
            "height": 20,
            "shape": {
                "aspect": 2,
                "class": "Rect"
            },
            "title": "1",
            "data": {}
        },
        {
            "id": 1,
            "x": 398,
            "y": 89,
            "width": 28,
            "height": 19.350000381469727,
            "shape": {
                "aspect": 2,
                "class": "Rect"
            },
            "title": " table 2",
            "data": {}
        },
        {
            "id": 2,
            "x": 285,
            "y": 399,
            "width": 20,
            "height": 20,
            "shape": {
                "aspect": 2,
                "class": "Rect"
            },
            "title": "3",
            "data": {}
        }
    ],
    "links": [
        {
            "id": "0-1",
            "source": 0,
            "target": 1,
            "title": "red",
            "data": {},
            "shape": null
        },
        {
            "id": "1-2",
            "source": 1,
            "target": 2,
            "title": "blue",
            "data": {},
            "shape": null
        },
        {
            "id": "0-2",
            "source": 2,
            "target": 0,
            "title": "red",
            "data": {},
            "shape": null
        }
    ]
};

var options = {
	directed: false,
	zoom: false
};

var graph = new ge.GraphEditor('#graph', data, options);
graph.zoomEvents = null;
var shift = false;

graph
	.on('click', function(pos) {
		if(shift) {
			graph.add({x: pos[0], y: pos[1]});
		}
		else {
			graph.select(null);
			updateSelection();
		}
	})
	.on('node-click', function(node) {
		graph.select(node);
		updateSelection();
	})
	.on('link-click', function(link) {
		graph.select(link);
		updateSelection();
	})
	.on('new-link-end', function(source, target) {
		graph.add({source: source, target: target});
	});

document.body.addEventListener('keydown', function(ev) {
	switch(ev.key) {
		case 'Shift':
			shift = true;
			graph.dragToLink(true);

			break;
		case 'Delete':
			var selection = graph.select();
			if(selection.node) {
				graph.remove(selection.node);
			}
			if(selection.link) {
				graph.remove(selection.link);
			}
			updateSelection();
			break;
	}
});
document.body.addEventListener('keyup', function(ev) {
	switch(ev.key) {
		case 'Shift':
			shift = false;
			graph.dragToLink(false);
			break;
	}
});
d3.select('#node-title').on('keydown', function(ev) {
	d3.event.stopPropagation();
});
d3.select('#link-color').on('keydown', function(ev) {
	d3.event.stopPropagation();
});
d3.select('#data').on('keydown', function(ev) {
	d3.event.stopPropagation();
});

function updateSelection() {
	var selection = graph.select();
	var node = d3.select('#selected-node').classed('hide', !selection.node);
	var link = d3.select('#selected-link').classed('hide', !selection.link);
	if(selection.node) {
		d3.select('#node-title').property(
			'value',
			selection.node.title
		);
		d3.select('#node-type').property(
			'value',
			selection.node.data.type
		);
	}
	if(selection.link) {
		d3.select('#link-color').property('value', selection.link.title);
	}
}

function openModal(modal) {
	if(typeof modal === 'string') {
		modal = d3.select(modal);
	}
	modal.classed('hide', false);
	setTimeout(function() { modal.classed('active', true); }, 100);
}

function closeModal(modal) {
	if(typeof modal === 'string') {
		modal = d3.select(modal);
	}
	modal.classed('active', false);
	setTimeout(function() { modal.classed('hide', true); }, 300);
}

function importModal() {
	var modal = d3.select('.modal-bg');
	var data = '{\n    "nodes": [],\n    "links": []\n}';
	var textarea = modal.select('textarea')
		.property('value', data);
	var error = modal.select('.error').classed('hide', true);
	modal.select('.modal-title').text('Import');
	modal.select('.modal-ok').on('click.modal', function() {
		try {
			d3.event.preventDefault();
			var data = JSON.parse(textarea.property('value'));
			graph.clear();
			if(data.nodes) {
				graph.addNodes(data.nodes);
			}
			if(data.links) {
				graph.addLinks(data.links);
			}
			closeModal(modal);
		}
		catch(err) {
			var msg = err.toString();
			if(err.stack) {
				msg += '\n';
				msg += err.stack.toString();
			}
			error.classed('hide', false).text(msg);
		}
	});
	openModal(modal);
}

function exportModal() {
	var modal = d3.select('.modal-bg');
	var data = JSON.stringify(graph.toJson(), null, 4);
	modal.select('.error').classed('hide', true);
	modal.select('.modal-title').text('Export');
	modal.select('textarea').property('value', data);
	modal.select('.modal-ok').on('click.modal', function() {
		d3.event.preventDefault();
		closeModal(modal);
	});
	openModal(modal);
}

var modal = d3.select('.modal-bg');
modal.on('click.modal', function() {
	closeModal(modal);
});
modal.select('.modal').on('click.modal', function() {
	d3.event.stopPropagation();
});
modal.select('.modal-cancel').on('click.modal', function() {
	d3.event.preventDefault();
	closeModal(modal);
});
modal.select('#copy').on('click.modal', function() {
	d3.event.preventDefault();
	var textarea = modal.select('textarea').node();
	textarea.focus();
	textarea.select();
	document.execCommand('copy');
});


d3.select('#import').on('click', function() {
	d3.event.preventDefault();
	importModal();
});
d3.select('#export').on('click', function() {
	d3.event.preventDefault();
	exportModal();
});
d3.select('#node-title').on('input', function() {
	var node = graph.selectNode();
	node.title = this.value;
	graph.updateNode(node);
});
d3.select('#node-type').on('change', function() {
	var node = graph.selectNode();
	node.title = this.value;
	graph.updateNode(node);


	node.shape = shape;
	node.prevTitle = null;
	graph.updateNode(node);
});
d3.select('#link-color').on('input', function() {
	var link = graph.selectLink();
	link.title = this.value;
	graph.updateLink(link);
});