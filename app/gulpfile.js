const gulp = require('gulp'),
    sass = require('gulp-sass'),
    sourcemaps = require('gulp-sourcemaps'),
    babel = require('gulp-babel'),
    ngAnnotate = require('gulp-ng-annotate'),
    concat = require('gulp-concat'),
    livereload = require('gulp-livereload');

// Compile sass into CSS & auto-inject into browser
const paths = {
    html: ['src/scripts/modules/*/views/**/*.html', 'src/index.html'],
    js: ['src/scripts/*.js', 'src/scripts/modules/*.js', 'src/scripts/modules/*/*.js', 'src/scripts/modules/*/**/*.js']

};

gulp.task('watch', function () {
    livereload.listen();
    gulp.watch("src/scss/*.scss", ['sass']);
    gulp.watch(paths.js, ['app']);
    gulp.watch(paths.html, ['html'])
});

gulp.task('html', function () {
    return gulp.src(paths.html)
        .pipe(livereload())
});

gulp.task('app', function () {
    return gulp.src(paths.js)
        .pipe(sourcemaps.init())
        .pipe(ngAnnotate())
        .pipe(babel({
            presets: ['es2015']
        }))
        .on('error', function (e) {
            console.log('>>>>ERROR', e);
            this.emit('end');
        })
        .pipe(concat('app.js'))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('src/'))
        .pipe(livereload());
});

gulp.task('sass', function () {
    return gulp.src("src/scss/styles.scss")
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest("src/css"))
        .pipe(livereload());
});


gulp.task('default', ['build', 'watch']);
gulp.task('build', ['html', 'app', 'sass']);