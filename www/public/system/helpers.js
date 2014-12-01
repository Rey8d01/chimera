/**
 * Created by rey on 12.05.14.
 */

chimera.helpers = {
    "sleep": function(ms) {
        ms += new Date().getTime();
        while (new Date() < ms) {
        }
    },
    "pagination": function(currentPage) {
    	console.log(currentPage);

     //    listPages = [];
     //    lastPage = 0;
        
    	// for (page in pageData.pages) {
     //        if (pageData.pages[page] != lastPage + 1) {
     //        	listPages.push("...");
     //        } 
     //        if (pageData.pages[page] == pageData.currentPage) {
     //        	listPages.push("["+pageData.pages[page]+"]");
     //        } else {
     //        	listPages.push(String(pageData.pages[page]));
     //        }
     //        lastPage = pageData.pages[page];
    	// }

     //    return listPages;
    }
};