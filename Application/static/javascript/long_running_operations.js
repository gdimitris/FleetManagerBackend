$.long_running_queue = {
    _timer: null,
    _queue: [],
    add: function(fn, context, time) {
        var setTimer = function(time) {
            $.long_running_queue._timer = setTimeout(function() {
                time = $.long_running_queue.add();
                if ($.long_running_queue._queue.length) {
                    setTimer(time);
                }
            }, time || 150);
        }

        if (fn) {
            $.long_running_queue._queue.push([fn, context, time]);
            if ($.long_running_queue._queue.length == 1) {
                setTimer(time);
            }
            return;
        }

        var next = $.long_running_queue._queue.shift();
        if (!next) {
            return 0;
        }
        next[0].call(next[1] || window);
        return next[2];
    },
    clear: function() {
        clearTimeout($.long_running_queue._timer);
        $.long_running_queue._queue = [];
    }
};

function createPartitionsForArray(array,map){
    var partitions = 100;
    var arLength = array.length;

    if (arLength < 300){
       var callback = partial(addMarkersForLocationsInMap, array, map ,0,arLength-1);
       $.long_running_queue.add(callback);
       hideProgressBar();
       return;
    }

    var step = Math.floor(arLength/partitions);
    var remainder = arLength % partitions;

    for(var cur_step = 0; cur_step<partitions;cur_step++){
        var start_index = cur_step * step;
        var end_index = (cur_step + 1) * step;
        var callback = partial(addMarkersForLocationsInMap, array, map ,start_index,end_index);
        $.long_running_queue.add(callback)
    }
    var rem_start_index  = partitions * step;
    var rem_end_index = rem_start_index + remainder;
    var callback = partial(addMarkersForLocationsInMap, array, map ,rem_start_index,rem_end_index);
    $.long_running_queue.add(callback)
}

function doPartition(array,start_range,end_range){
    var bar = document.getElementById('locations-bar');
    for(var i = start_range; i<end_range;i++){
        //console.log(i);
    }
    var w = parseInt(bar.style.width);
    w += 1;
    bar.style.width = w + "%";
    if (w > 99) {
        var barContainer = document.getElementById('barContainer')
        barContainer.style.visibility = "hidden";
    }
}

function partial(func /*, 0..n args */) {
  var args = Array.prototype.slice.call(arguments, 1);
  return function() {
    var allArguments = args.concat(Array.prototype.slice.call(arguments));
    return func.apply(this, allArguments);
  };
}