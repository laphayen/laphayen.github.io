
console.time('duration_time');

var result = 0;
for (var i = 0; i < 10000; i++) {
	result += i;
}

console.timeEnd('duration_time');
