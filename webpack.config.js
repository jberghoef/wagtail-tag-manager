const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  entry: {
    tag_form_view: ["@babel/polyfill", "./frontend/admin/tag_form_view.ts"],
    trigger_form_view: ["@babel/polyfill", "./frontend/admin/trigger_form_view.ts"],
    variable_form_view: ["@babel/polyfill", "./frontend/admin/variable_form_view.ts"],
    wtm: ["@babel/polyfill", "./frontend/client/wtm.ts"]
  },
  output: {
    path: path.resolve(__dirname, "src/wagtail_tag_manager/static/"),
    filename: "[name].bundle.js"
  },
  module: {
    rules: [{
        test: /\.tsx?$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "ts-loader"
        }
      },
      {
        test: /\.m?jsx?$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env", {
              "useBuiltIns": "entry"
            }],
            plugins: [
              require("@babel/plugin-proposal-object-rest-spread"),
            ]
          }
        }
      },
      {
        test: /\.scss$/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"]
      }
    ]
  },
  resolve: {
    extensions: [".tsx", ".ts", ".jsx", ".js"]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].bundle.css",
      chunkFilename: "[id].chunk.css"
    })
  ]
};