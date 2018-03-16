function traversal_dom(parent,node){
    if (typeof(node.childNodes) != "undefined" && typeof(node.getBoundingClientRect) != "undefined") {
        r = node.getBoundingClientRect();
        if(r){
            
            //node.style.border = "solid 2px red";
            
            var node_id = python.add_node(parent,node.nodeName,r.top,r.left,r.bottom-r.top,r.right-r.left,node)
            var childrens = node.childNodes;
            for(var i=0; i<childrens.length; i++) {
                traversal_dom(node_id,childrens[i]);
            }
        }
    }
}
function parse(){
    traversal_dom(0,document.getElementsByTagName('html')[0]);
    python.save();
}
parse();