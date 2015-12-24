/**
 * Created by rey on 12.05.14.
 */

chimera.helpers = {
    sleep: function(ms) {
        ms += new Date().getTime();
        while (new Date() < ms) {
        }
    },
    log: function() {
        if (chimera.config.debug) {
            console.log(arguments)
        }
    },
    debug: function() {
        if (chimera.config.debug) {
            console.debug(arguments)
        }
    }
};