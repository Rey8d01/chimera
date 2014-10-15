/**
 * Created by rey on 12.05.14.
 */

chimera.helpers = {
    "sleep": function sleep(ms) {
        ms += new Date().getTime();
        while (new Date() < ms) {
        }
    }
};