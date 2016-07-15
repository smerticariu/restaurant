var $ = require('gulp-load-plugins')();
var argv = require('yargs').argv;
var browser = require('browser-sync');
var compatibility = ['last 2 versions', 'ie >= 9'];
var gulp = require('gulp');
var isProduction = !!(argv.production);
var merge = require('merge-stream');
var panini = require('panini');
var port = 8000;
var rimraf = require('rimraf');
var sequence = require('run-sequence');
var sherpa = require('style-sherpa');

var PATHS = {
  assets: [
    'src/assets/**/*',
    '!src/assets/{!img,js,sass}/**/*'
  ],
  css: [],
  sass: [
    'bower_components/foundation-sites/scss',
    'bower_components/motion-ui/src/'
  ],
  javascript: [
    'bower_components/jquery/dist/jquery.js',
    'static/js/**/*.js'
  ]
};

// Delete the "dist" folder every time a build starts
gulp.task('clean', function(done) {
  rimraf('static/dist', done);
});

// Compiles the sass files and appends the css files from vendors in one app.css file
gulp.task('css', function() {

  var uncss = $.if(isProduction, $.uncss({
    html: ['src/**/*.html'],
    ignore: [
      new RegExp('^meta\..*'),
      new RegExp('^\.is-.*')
    ]
  }));

  var minifycss = $.if(isProduction, $.minifyCss());

  var cssStream =
    gulp
    .src(PATHS.css)
    .pipe($.concat('css-styles.css'));

  var scssStream =
    gulp
    .src('static/app.scss')
    .pipe($.sourcemaps.init())
    .pipe($.sass({
        includePaths: PATHS.sass
      })
      .on('error', $.sass.logError))
    .pipe($.autoprefixer({
      browsers: compatibility
    }))
    // .pipe(uncss)
    .pipe(minifycss)
    .pipe($.if(!isProduction, $.sourcemaps.write()))
    .pipe($.concat('scss-styles.css'));

  var mergedStream =
    merge(cssStream, scssStream)
    .pipe($.concat('app.css'))
    .pipe(gulp.dest('static/dist/assets/css'));

  return mergedStream;
});

// Combine JavaScript
gulp.task('javascript', function() {

  var uglify = $.if(isProduction, $.uglify()
    .on('error', function(e) {
      console.log(e);
    }));

  return gulp
    .src(PATHS.javascript)
    .pipe($.sourcemaps.init())
    .pipe($.concat('app.js'))
    .pipe(uglify)
    .pipe($.if(!isProduction, $.sourcemaps.write()))
    .pipe(gulp.dest('static/dist/assets/js'));
});

// Build the "dist" folder
gulp.task('build', function(done) {
  sequence('clean', [ 'javascript',  'css'], done);
});


// Build the site, run the server, and watch for file changes
gulp.task('default', ['build'], function() {
  gulp.watch(PATHS.assets, ['copy', browser.reload]);
  gulp.watch(['static/**/*.scss'], ['css', browser.reload]);
  gulp.watch(['staticjs/**/*.js'], ['javascript', browser.reload]);

});
