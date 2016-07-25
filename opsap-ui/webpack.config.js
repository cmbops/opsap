var path = require('path');
var webpack = require('webpack');
var htmlWebpackPlugin = require('html-webpack-plugin')

var config = {
  entry: {
  	vendor: ['jquery','angular','angular-ui-router'],
  	app: './src/main.js'
  },
  output: {
   path: path.join(__dirname,'dist'),
   publicPath: '/dist/',
   filename: '[name].bundle.js'
  },
  module: {
  	//开发减少编译时间
  	noParse: [/(jquery)/],
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
    //uglify压缩
    new webpack.optimize.UglifyJsPlugin({
    	compress: {
    		warnings: false
    	}
    }),
    new webpack.optimize.OccurrenceOrderPlugin(),
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
    	jQuery: 'jquery'
    })
  ],
  resolve: {
  	extensions: ['', '.js'], 
  	alias: {
  	  'srcUrl': path.resolve(__dirname, './src'),
  	  'componentsUrl': path.resolve(__dirname, './src/components'),
  	  'bootstrap': 'bootstrap/dist/css/bootstrap.min.css'
  	}
  },
  devtool: "eval-source-map" 
}

module.exports = config