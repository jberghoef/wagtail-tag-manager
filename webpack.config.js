const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  entry: {
    cookie_declaration_form_view: "./frontend/admin/cookie_declaration_form_view.ts",
    tag_form_view: "./frontend/admin/tag_form_view.ts",
    variable_form_view: "./frontend/admin/variable_form_view.ts",
    wtm: "./frontend/client/wtm.ts"
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
            presets: ["@babel/preset-env"],
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