define("torabot/yandere/0.1.0/yandere",["./create_tag_search_regex","./retrieve_tag_search","./reorder_search_results","./split_result","main/ut","main/search","main/handlebars-v1.3.0"],function(a,b,c){var d={create_tag_search_regex:a("./create_tag_search_regex"),retrieve_tag_search:a("./retrieve_tag_search"),reorder_search_results:a("./reorder_search_results"),split_result:a("./split_result"),complete_tag:function(a){var b=d.create_tag_search_regex(a,{global:!0}),c=d.retrieve_tag_search(b,d.options.source,{max_results:100});c=d.reorder_search_results(a,c);var e=c;return d.bubble_rating_tags(e,a),e=e.slice(0,null!=d.options.max_results?d.options.max_results:10),d.split_result(e)},bubble_rating_tags:function(a,b){-1!="sqe".indexOf(b)&&a.unshift("0`"+b+"` ")},match:function(b,c){var e=b.split(" ").slice(-1)[0];if(e){var f=d.complete_tag(e);c($.map(a("main/ut").zip(f[0],f[1]),function(a){return{value:a[0],alias:a[1].map(function(a){return{value:a}})}}))}},init:function(a){d.options=a},activate:function(){var b=null,c=function(c,d){d=$.extend({query:null,set:function(b){return a("main/search").$q.val(b)}},d);var e=d.query;e||(b=e=a("main/search").$q.typeahead("val"));var f=e.split(" ").slice(0,-1);return f.push(c.value),d.set(f.join(" "))};a("main/search").$q.typeahead({hint:!0,highlight:!0,minLength:1},{name:"yandere",displayKey:"value",source:d.match,templates:{suggestion:a("main/handlebars-v1.3.0").compile(["<p class=completion-item>","<strong class=ellipsis>{{value}}</strong>","{{#if alias}}<br>{{#each alias}}<span class='ellipsis label label-default'>{{value}}</span> {{/each}}{{/if}}","</p>"].join(""))}}).on("typeahead:cursorchanged",function(a,b){c(b),a.preventDefault()}).on("typeahead:selected",function(a,d){var e=$(this);c(d,{query:b,set:function(a){return e.typeahead("val",a)}}),a.preventDefault()})},deactivate:function(){a("main/search").$q.typeahead("destroy")}};c.exports={init:d.init,activate:d.activate,deactivate:d.deactivate}}),define("torabot/yandere/0.1.0/create_tag_search_regex",[],function(a,b,c){c.exports=function(a,b){var c=a.split(""),d=[],e="(([^`]*_)?";if($.map(c,function(a){var b=RegExp.escape(a);e+=b}),e+=")",d.push(e),-1!=a.indexOf("_")){var f=a.split("_",1)[0],g=a.slice(f.length+1);f=RegExp.escape(f),g=RegExp.escape(g);var e="(";e+="("+f+"[^`]*_"+g+")",e+="|",e+="("+g+"[^`]*_"+f+")",e+=")",d.push(e)}if(!b.top_results_only){var e="(";$.map(c,function(a){var b=RegExp.escape(a);e+=b,e+="[^`]*"}),e+=")",d.push(e)}var h=d.join("|");return h="(\\d+)[^ ]*`("+h+")[^`]*`[^ ]* ",new RegExp(h,b.global?"g":"")}}),define("torabot/yandere/0.1.0/retrieve_tag_search",[],function(a,b,c){c.exports=function(a,b,c){var d=[],e=10;for(null!=c.max_results&&(e=c.max_results);d.length<e;){var f=a.exec(b);if(!f)break;var g=f[0];-1==g.indexOf(":deletethistag:")&&-1==d.indexOf(g)&&d.push(g)}return d}}),define("torabot/yandere/0.1.0/reorder_search_results",["torabot/yandere/0.1.0/create_tag_search_regex"],function(a,b,c){c.exports=function(b,c){var d=a("torabot/yandere/0.1.0/create_tag_search_regex")(b,{top_results_only:!0,global:!1}),e=[],f=[];return $.map(c,function(a){d.test(a)?e.push(a):f.push(a)}),e.concat(f)}}),define("torabot/yandere/0.1.0/split_result",[],function(a,b,c){c.exports=function(a){var b=[],c=[];return $.map(a,function(a){var d=a.match(/(\d+)`([^`]*)`(([^ ]*)`)? /);if(!d)throw ReportError("Unparsable cached tag: '"+a+"'",null,null,null,null),"Unparsable cached tag: '"+a+"'";var a=d[2],e=d[4];e=d[4]?e.split("`"):[],-1==b.indexOf(a)&&(b.push(a),c.push(e))}),[b,c]}});
