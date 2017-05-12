var Metalsmith = require('metalsmith');
var layouts = require('metalsmith-layouts');
var markdown = require('metalsmith-markdown');
var debug = require('metalsmith-debug');
var ignore = require('metalsmith-ignore');
//var permalinks  = require('metalsmith-permalinks');

Metalsmith(__dirname)          // instantiate Metalsmith in the cwd
    .use(ignore('*~'))
    .source('src')        // specify source directory
    .destination('build2')     // specify destination directory
    .use(debug())
    .use(markdown())             // transpile markdown into html
    .use(layouts({               // wrap a handlebars-layout
	engine: 'handlebars'       // around transpiled html-files
    }))    
    .build(function(err) {       // this is the actual build process
	if (err) throw err;    // throwing errors is required
    });
