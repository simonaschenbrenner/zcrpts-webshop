﻿(function (s){	var w = new Window( 'palette{ preferredSize:[200,100] }' ),	    m = w.add( 'statictext{ alignment:["fill","fill"], properties:{multiline:true} }' ),	    i,n; 				w.show();	for( i=0,n=s.length; i<n; 		w.update( m.text+='--',$.sleep(60),m.text+=s[i++],$.sleep(60),m.text=m.text.replace('--','') ) 	);	$.sleep(1500);	w.close();	})( "Hello World!\r\rMein Name ist\r"+(File($.fileName)).name.replace('_dummy','') )