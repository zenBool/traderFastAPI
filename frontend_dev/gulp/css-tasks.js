const gulp = require('gulp')
const sass = require('gulp-sass')
const concat = require('gulp-concat')
const cleanCSS = require('gulp-clean-css')
const autoprefixer = require('gulp-autoprefixer')
const {argv} = require('yargs')
const config = require('../gulp.config.json')
const sourcemaps = require('gulp-sourcemaps')
const gulpIf = require("gulp-if");

let directory = argv.output
let dev = argv.dev
let mini = argv.mini
if (directory === undefined) {
    directory = config.output
}
if (mini === undefined) {
    mini = config.mini
}
const AUTOPREFIXER_BROWSERS = [
  "ie >= 10",
  "ie_mob >= 10",
  "ff >= 30",
  "chrome >= 34",
  "safari >= 7",
  "opera >= 23",
  "ios >= 7",
  "android >= 4.4",
  "bb >= 10",
];
function styleTaskDev(styles){
    let paths = []
    styles.forEach((js) => {
        paths.push(js.replace('{directory}', directory))
    })

    return gulp
      .src(paths)
      .pipe(sourcemaps.init())
      .pipe(
        sass({
          includePaths: ["./node_modules"],
          outputStyle: "compressed",
        }).on("error", sass.logError)
      )
      .pipe(autoprefixer(AUTOPREFIXER_BROWSERS))
      .pipe(sourcemaps.write("./maps"))
      .pipe(gulp.dest(`./${directory}/assets/css/`));
}

function styleTask(styles) {
    let paths = []
    styles.forEach((js) => {
        paths.push(js.replace('{directory}', directory))
    })
    return gulp
      .src(paths)
      .pipe(
        sass({
          includePaths: ["./node_modules"],
        }).on("error", sass.logError)
      )
      .pipe(autoprefixer(AUTOPREFIXER_BROWSERS))
      .pipe(gulpIf(mini == "true", cleanCSS({ compatibility: "ie9" })))
      .pipe(gulp.dest(`./${directory}/assets/css/`));
    
}

gulp.task('style:main', function () {
    let styles = ['./src/assets/scss/**/*.scss'];
    if (dev == 'true') {
        return styleTaskDev(styles)
    } else { 
        return styleTask(styles)
    }
})

gulp.task('style:libs', function(){
    let styles = config.assets.style;
    let paths = []
    styles.forEach((js) => {
        paths.push(js.replace('{directory}', directory))
    })

    return gulp
      .src(paths)
      .pipe(
        sass({
          includePaths: ["./node_modules"],
          outputStyle: "compressed",
        }).on("error", sass.logError)
      )
      .pipe(cleanCSS())
      .pipe(autoprefixer(AUTOPREFIXER_BROWSERS))
      .pipe(concat("libs.min.css"))
      .pipe(gulp.dest(`./${directory}/assets/css/`));
})

gulp.task('style', gulp.series('style:libs','style:main'));