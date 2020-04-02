let indexes_en = require('./indexes-en.json');
let indexes_zh = require('./indexes-zh.json');
window.exports = {
    'cpp': {
        mode: 'doc',
        args: {
            indexes: indexes_en.concat(indexes_zh)
        }
    },
    'cpp-en': {
        mode: 'doc',
        args: {
            indexes: indexes_en
        }
    },
    'cpp-cn': {
        mode: 'doc',
        args: {
            indexes: indexes_zh
        }
    }
};
