webpackJsonp([7],{T0N6:function(e,t){},ep0M:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=a("Dd8w"),i=a.n(r),n=a("xAvK"),o={data:function(){var e=this;return{idTypes:n.IDTYPE,gender:n.GENDER,totalCount:0,page:1,pageSize:10,searchForm:{name:"",idType:"0",idNo:"",phone:""},tableData:[],tableLoading:!1,tableColumns:[{title:"会员号",key:"memberId",sortable:!0,minWidth:150},{title:"姓名",key:"name",sortable:!0,minWidth:100},{title:"性别",key:"gender",filters:n.GENDER.map(function(e){return{label:e.value,value:e.key}}),filterMultiple:!0,filterMethod:function(e,t){return t.gender===e},minWidth:100,render:function(e,t){var a=n.GENDER.find(function(e){return t.row.gender===e.key});return e("span",a&&a.value)}},{title:"证件类型",key:"idType",filters:n.IDTYPE.map(function(e){return{label:e.value,value:e.key}}),filterMultiple:!0,filterMethod:function(e,t){return t.idType===e},minWidth:100,render:function(e,t){var a=n.IDTYPE.find(function(e){return t.row.idType===e.key});return e("span",a&&a.value)}},{title:"证件号码",key:"idNo",sortable:!0,minWidth:150},{title:"手机号",key:"phone",sortable:!0,minWidth:120},{title:"操作",key:"action",width:100,align:"center",render:function(t,a){return t("div",[t("Button",{props:{type:"primary",size:"small"},style:{marginRight:"5px"},on:{click:function(){e.$router.push("member/"+a.row.memberId)}}},"详情")])}}]}},created:function(){this.mockTableData()},methods:{mockTableData:function(e){var t=this;this.tableLoading=!0;this.$fetch("/member/",e).then(function(e){var a=e.data,r=a.count,i=a.results;t.tableData=i,t.totalCount=r,t.tableLoading=!1}).catch(function(e){t.$Message.error(e),t.tableLoading=!1})},changePage:function(e){this.page=e,this.mockTableData({params:{offset:(e-1)*this.pageSize,limit:this.pageSize}})},changePageSize:function(e){this.pageSize=e,this.mockTableData({params:{offset:0,limit:e}})},search:function(){this.mockTableData({params:i()({offset:(this.page-1)*this.pageSize,limit:this.pageSize},this.searchForm)})},reset:function(){this.$refs.searchForm.resetFields(),this.mockTableData({params:{offset:(this.page-1)*this.pageSize,limit:this.pageSize}})}}},s={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"member"},[a("div",{staticClass:"header"},[a("Form",{ref:"searchForm",attrs:{model:e.searchForm,"label-width":80}},[a("FormItem",{attrs:{label:"姓名",prop:"name"}},[a("Input",{model:{value:e.searchForm.name,callback:function(t){e.$set(e.searchForm,"name",t)},expression:"searchForm.name"}})],1),e._v(" "),a("FormItem",{attrs:{prop:"idNo"}},[a("Input",{model:{value:e.searchForm.idNo,callback:function(t){e.$set(e.searchForm,"idNo",t)},expression:"searchForm.idNo"}},[a("Select",{staticStyle:{width:"80px"},attrs:{slot:"prepend"},slot:"prepend",model:{value:e.searchForm.idType,callback:function(t){e.$set(e.searchForm,"idType",t)},expression:"searchForm.idType"}},e._l(e.idTypes,function(t,r){return a("Option",{key:r,attrs:{value:t.key}},[e._v("\n            "+e._s(t.value)+"\n          ")])}))],1)],1),e._v(" "),a("FormItem",{attrs:{label:"手机号",prop:"phone"}},[a("Input",{model:{value:e.searchForm.phone,callback:function(t){e.$set(e.searchForm,"phone",t)},expression:"searchForm.phone"}})],1),e._v(" "),a("FormItem",[a("Button",{attrs:{type:"primary"},nativeOn:{click:function(t){return e.search(t)}}},[e._v("搜索")]),e._v(" "),a("Button",{attrs:{type:"error"},nativeOn:{click:function(t){return e.reset(t)}}},[e._v("清空")])],1)],1)],1),e._v(" "),a("div",{staticClass:"body"},[a("Table",{attrs:{data:e.tableData,columns:e.tableColumns,loading:e.tableLoading,stripe:""}})],1),e._v(" "),a("div",{staticClass:"footer"},[a("div",{staticClass:"pager",staticStyle:{float:"right"}},[a("Page",{attrs:{total:e.totalCount,current:1,"show-total":"","show-elevator":"","show-sizer":""},on:{"on-change":e.changePage,"on-page-size-change":e.changePageSize}})],1)])])},staticRenderFns:[]};var l=a("VU/8")(o,s,!1,function(e){a("T0N6")},null,null);t.default=l.exports}});
//# sourceMappingURL=7.440d534874abe630fe33.js.map