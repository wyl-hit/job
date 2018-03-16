//if("complete"==document.readyState) {
//	parse();
    
//}
//else{
	//document.onreadystatechange = function() {
	//	if("complete"==document.readyState)	{
		//	parse();
	//	}
        //alert(document.readyState)
//	}
//}

function traversal_dom(parent,node){
    var watch_var = new Array();
    watch_var[0] = 0;
    watch_var[1] = 0;
    watch_var[2] = 0;
    watch_var[3] = 0;
    
    if (typeof(node.childNodes) != "undefined" && typeof(node.getBoundingClientRect) != "undefined") {
        var style = window.getComputedStyle(node)
        if (style['background-image'] != 'none'){
            python.add_background(style['background-image'])
        }
        var node_id = -1
        r = node.getBoundingClientRect();
        //alert(node.nodeName);
        if (node.nodeName == "A"){
            //alert("A");
            var origin = window.top.location.host.split('.').slice(-2)
            origin = origin[0]+'.'+origin[1]
            //alert(node.href+"\n"+origin);
            if (node.href.indexOf('http') == 0){
                var index_t = node.href.indexOf(origin)
                if(index_t < 20 && index_t > 0)
                    watch_var[0] = 1;
                else{
                    //alert("watch_var[1] = 1;")
                    watch_var[1] = 1;
                }
            }
            else
                watch_var[0] = 1;
        }
        else if (node.nodeName == "IMG")
            watch_var[2] = (r.bottom-r.top) * (r.right-r.left);
        else if (node.nodeName == "INPUT")
            watch_var[3] = 1;
        else if (node.nodeName == "SELECT")
            watch_var[3] = 1;
        if(r){
            //node.style.border = "solid 2px red";
            node_id = python.add_node(parent,node.nodeName,r.top,r.left,r.bottom-r.top,r.right-r.left,node)
        }
        var childrens = node.childNodes;
        for(var i=0; i<childrens.length; i++) {
            rwv = traversal_dom(node_id,childrens[i]);
            //alert("1"+watch_var[0]+" "+watch_var[1]+" "+watch_var[2])
            watch_var[0] += rwv[0];
            watch_var[1] += rwv[1];
            watch_var[2] += rwv[2];
            watch_var[3] += rwv[3];
        }
        //alert("2"+" "+watch_var[0]+" "+watch_var[1]+" "+watch_var[2]+" "+watch_var[3])
        python.set_watch_var(node_id,watch_var[0],watch_var[1],watch_var[2],watch_var[3])
    }
    return watch_var;
}
function parse(){
    traversal_dom(0,document.getElementsByTagName('html')[0]);
    python.save();
}
parse();

