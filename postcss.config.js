module.exports = {
    plugins: [
        require('autoprefixer')({ 
            overrideBrowserslist: [
                'last 5 version',
                '>5%'
            ]
        }),
        require('postcss-minify'),
    ],
}