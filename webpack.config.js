const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = (env, options) => ({
  entry: {
    index: ["./frontend/admin/index.ts"],
    tag_form_view: ["./frontend/admin/tag_form_view.ts"],
    trigger_form_view: ["./frontend/admin/trigger_form_view.ts"],
    variable_form_view: ["./frontend/admin/variable_form_view.ts"],
    checkbox_select_multiple: ["./frontend/admin/widgets/checkbox_select_multiple.ts"],
    codearea: ["./frontend/admin/widgets/codearea.ts"],
    wtm: ["./frontend/client/wtm.ts"]
  },
  output: {
    path: path.resolve(__dirname, "src/wagtail_tag_manager/static/wagtail_tag_manager"),
    filename: "[name].bundle.js",
    sourceMapFilename: "sourcemaps/[file].map"
  },
  devtool: options.mode == "production" ? "hidden-source-map" : "source-map",
  module: {
    rules: [
      {
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
            presets: [
              [
                "@babel/preset-env",
                {
                  useBuiltIns: "usage"
                }
              ]
            ],
            plugins: [require("@babel/plugin-proposal-object-rest-spread")]
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
});
