function render_region(ctx, sx, sy, sw, sh) {
    var start = Date.now();
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "/render?sx="+sx+"&sy="+sy+"&sw="+sw+"&sh="+sh, true);
	xhr.responseType = "arraybuffer";
	xhr.onload = function () {
	    console.log("Time", (Date.now() - start) / 1000, "seconds")
		var id = ctx.createImageData(sw, sh);
		var data = new Uint8Array(this.response);
		for (var i = 0; i < data.length; i++) {
				id.data[i] = data[i];
		}
		ctx.putImageData(id, sx, sy);
		update_progress();
	};
	console.log("REQUESTING", sx, sy, sw, sh);
	xhr.send();
};

function render (n, canvas_id) {
    var canvas = document.getElementById(canvas_id);
	var ctx = canvas.getContext("2d");
	var sw = canvas.width / n;
	var sh = canvas.height / n;
	for (var y=0; y<n; y++) {
		for (var x=0; x<n; x++) {
			var sx = sw * x;
			var sy = sh * y;
			render_region(ctx, sx, sy, sw, sh);
		}
	}
};

total = 0;
function update_progress() {
    total += 1;
    $bar = $('#bar');
    $bar.width(total / (8*8) * 100 + '%');
};
