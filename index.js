var Metalsmith = require('metalsmith');
var layouts = require('metalsmith-layouts');
var markdown = require('metalsmith-markdown');
var debug = require('metalsmith-debug');
var ignore = require('metalsmith-ignore');
var assets = require('metalsmith-assets');

Metalsmith(__dirname)
    .use(ignore('*~'))
    .source('src')
    .destination('build')
    .clean(true)
    .use(assets({
	source: './assets',
	destination: './assets'
    }))
    .use(debug())
    .use(markdown())
    .use(layouts({
	engine: 'handlebars'
    }))    
    .build(function(err) {
	if (err) throw err;
    });
