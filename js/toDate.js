#!/usr/bin/node

var streamIn  = process.stdin;
var streamOut = process.stdout;

var stream = require('stream');
var byline = require('readline-stream');


(function(){
	//we need a node version >=4
	var pkg = require('./package'),
		semver = require('semver');

	if(!semver.satisfies(process.version, pkg.engines.node)) {
		throw new Error('Requires a node version matching ' + pkg.engines.node);
	}
})();

//var fs = require('fs');
//console.log(process.argv);

if(process.argv.length < 2+1){
	var execName = process.argv[1].split("/").slice(-1);
	console.error("usage: "+execName+" path");
	process.exit(-1);
}

var padder = function createPadder(size) {
	return function pad(num){
		var s = num+"";
		while (s.length < size) s = "0" + s;
		return s;
	}
};
var date = process.argv[2]
	.split("/")
	.slice(-3)
	.map(padder(2))
	.join("-");

//console.error(date);


var prependDateTransform = new stream.Transform({
	transform: function(chunk, encoding, next) {
		var out = "'"+date+"',"+chunk;
		this.push(out+"\n");
		next();
	}
});

streamIn.pipe(byline()).pipe(prependDateTransform).pipe(streamOut);
