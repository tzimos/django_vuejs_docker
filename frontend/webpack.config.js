const path = require('path'),
  webpack = require('webpack'),
  CleanWebpackPlugin = require('clean-webpack-plugin'),

  // This package generates the webpack-stats.json in the path we want.
  BundleTracker = require('webpack-bundle-tracker'),
  WriteFilePlugin = require('write-file-webpack-plugin'),

  // It allows to load the css files decoupled from js.
  // You have first to import the css file that you want to be included.
  // Usage in template <head>{% render_bundle 'base/main' 'css' %}</head>
  ExtractTextPlugin = require('extract-text-webpack-plugin'),
  VueLoaderPlugin = require('vue-loader/lib/plugin'),

  // Cleans the created files from autoreload.
  CleanObsoleteChunks = require('webpack-clean-obsolete-chunks');


module.exports = {
  mode: 'development',
  entry:
    {
      "fe/tasklist":'./src/tasklist/tasklist.js',
      "fe/login":"./src/home/login/login.js",
      "fe/navbar":"./src/base/navbar.js",
      "fe/create_task":"./src/tasklist/create_task.js",
      "fe/edit_task":"./src/tasklist/create_task.js",
      "fe/sign_up":"./src/home/sign_up/sign_up.js"
    },
  output: {
    path: path.resolve(__dirname, '../backend/static'),
    publicPath: '/static/',
    filename: '[name]/js/[name].js'
  },
  plugins: [
    new VueLoaderPlugin(),

    // The following plugin extracts the webpack-stats.json file to django
    // directory in order to
    new BundleTracker({filename: '../backend/webpack-stats.json'}),

    new WriteFilePlugin(
      // excludes the [hash].hot-update.json autogenerated files
      {test: /^(?!.*(hot)).*/,}
    ),
    bundleExtractCss = new ExtractTextPlugin({filename:"[name]/css/[name].css"}),

    // The following is used to clean the new generated files from webpack
    // hot reload.
    new CleanObsoleteChunks({deep: true}),

    // The following cleans the whole static folder in backend
    // excluded admin assets.
    new CleanWebpackPlugin(
      ['backend/static/fe/**/*.js'],
      {
        root: __dirname+"/../",
        watch:true,
      }
      )
    ,
  ],
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ExtractTextPlugin.extract(
          {
            use: ['css-loader', 'sass-loader']
          })
      },
      {
        test: /\.scss$/,
        use: bundleExtractCss.extract(['css-loader', 'sass-loader'])
      },
      {
        test: /\.sass$/,
        use: [
          'vue-style-loader',
          'css-loader',
          'sass-loader?indentedSyntax'
        ],
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
            // Since sass-loader (weirdly) has SCSS as its default parse mode, we map
            // the "scss" and "sass" values for the lang attribute to the right configs here.
            // other preprocessors should work out of the box, no loader config like this necessary.
            'scss': [
              'vue-style-loader',
              'css-loader',
              'sass-loader'
            ],
            'sass': [
              'vue-style-loader',
              'css-loader',
              'sass-loader?indentedSyntax'
            ]
          }
          // other vue-loader options go here
        }
      },
      {
        enforce: "pre",
        test: /\.js$/,
        exclude: /node_modules/,
        loader: "eslint-loader",
        options: {
          fix: true,
          emitError: true,
          emitWarning: true,
          cache: true
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: 'images/[name].[ext]'
        }
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    },
    extensions: ['*', '.js', '.vue', '.json']
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    overlay: true,
    port: 8080,
    host: '0.0.0.0'
  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map'
}

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map'
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}
