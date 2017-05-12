var Metalsmith = require('metalsmith');
var layouts = require('metalsmith-layouts');
var markdown = require('metalsmith-markdown');
var debug = require('metalsmith-debug');
var ignore = require('metalsmith-ignore');

Metalsmith(__dirname)
    .use(ignore('*~'))
    .source('src')
    .destination('build')
    .clean(true)
    .use(debug())
    .use(markdown())
    .use(layouts({
	engine: 'handlebars'
    }))    
    .build(function(err) {
	if (err) throw err;
    });
