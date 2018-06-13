const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    entry: {
        tag_form_view: './frontend/admin/tag_form_view.js',
        variable_form_view: './frontend/admin/variable_form_view.js',
        wtm: './frontend/client/wtm.js'
    },
    output: {
        path: path.resolve(__dirname, 'src/wagtail_tag_manager/static/'),
        filename: '[name].bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, "css-loader"]
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "[name].css",
            chunkFilename: "[id].css"
        })
    ]
};
