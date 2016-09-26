var path = require('path');
var webpack = require('webpack');
var htmlWebpackPlugin = require('html-webpack-plugin');

var env = process.env.NODE_ENV ? process.env.NODE_ENV : 'dev';

var config = {
  entry: {
  	vendor: ['jquery','angular','angular-ui-router', 'echarts'],
  	app: './src/main.js'
  },
  output: {
   path: path.join(__dirname,'dist'),
   publicPath: '/dist/',
   filename: '[name].bundle.js'
  },
  module: {
  	loaders: [
  	{
  	  test: /\.html$/,
  	  loader: 'raw'
  	},
  	{
  	  test: /\.css$/,
  	  loader: 'style!css'
  	},
  	{
      test: /\.(png|jpe?g|gif|svg|cur)(\?.*)?$/,
      loader: 'url',
      query: {
        limit: 10000
      }
     },
     {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
        loader: 'url',
        query: {
          limit: 10000
        }
      },
     {
       test: /\.js$/,
       loader: 'babel',
       exclude: '/node_modules/',
       query: {
       	   presets:['es2015','stage-2']
       }
     }
     ]
  },
  plugins: [
    //提取公共模块
    new webpack.optimize.CommonsChunkPlugin({
    	name: 'vendor',
    	minChunks: Infinity,
    }),
    //生成html,默认单页面
    new htmlWebpackPlugin({
    	filename: 'index.html',
    	template: 'index.html'
    }),
    //暴露全局变量
    new webpack.ProvidePlugin({
    	$: 'jquery',
    	jQuery: 'jquery',
      'window.jQuery': 'jquery',
      'window.$': 'jquery'
    })
  ],
  resolve: {
  	extensions: ['', '.js'], 
  	alias: {
  	  'srcUrl': path.resolve(__dirname, './src'),
  	  'componentsUrl': path.resolve(__dirname, './src/components'),
  	  'bootstrap': 'bootstrap/dist/css/bootstrap.min.css'
  	}
  } 
}

if(env === 'product') {
  var minify = [    //uglify压缩
    new webpack.optimize.UglifyJsPlugin({
    	compress: {
    		warnings: false
    	}
    }),
    new webpack.optimize.OccurrenceOrderPlugin()];
  var jqueryExpose = [{
       test: require.resolve('jquery'),
       loader: 'expose?$!expose?jQuery'
     }];
  config.module.concat(jqueryExpose);
  config.plugins.concat(minify);
} else {
  config.noParse = [/(jquery)/];
  config.devtool = "eval-source-map";
}

module.exports = config