webpackJsonp([4],{OS4j:function(e,t){},W9QU:function(e,t,r){"use strict";var a={props:{selected:{type:Array,default:[]},items:{type:Array,default:[]},single:{type:Boolean,default:!0}},methods:{changeSelected:function(e,t){this.single&&this.selected.fill(!1),this.selected[t]=e,this.$forceUpdate()}}},o={render:function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"enum-selector"},e._l(e.items,function(t,a){return r("span",{key:t.key,staticClass:"enum-selector__item",class:{active:e.selected[a]}},[r("input",{attrs:{type:"checkbox"},domProps:{checked:e.selected[a]},on:{change:function(t){e.changeSelected(t.target.checked,a)}}}),e._v("\n    "+e._s(t.value)+"\n  ")])}))},staticRenderFns:[]};var n=r("VU/8")(a,o,!1,function(e){r("OS4j")},null,null);t.a=n.exports},kDlu:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=r("pFYg"),o=r.n(a),n=r("Dd8w"),i=r.n(n),s=r("fZjL"),l=r.n(s),c=r("Gu7T"),d=r.n(c),u=r("woOf"),m=r.n(u),h=r("xAvK"),f={components:{"enum-selector":r("W9QU").a},data:function(){var e=this;return{serviceType:h.SERVICETYPE,leaseholdStatus:h.LEASEHOLDSTATUS,creditStatus:h.CREDITSTATUS,deliveryMode:h.DELIVERYMODE,page:1,pageSize:10,totalCount:0,searchForm:{serviceNo:"",name:"",phone:"",createDate:[],finishDate:[],leaseholdStatus:[],creditStatus:[],deliveryStore:"",deliveryMode:[]},moreCondModal:!1,moreCondCount:0,moreCondModalForm:{createDate:[],finishDate:[],leaseholdStatus:[],creditStatus:[],deliveryStore:"",deliveryMode:[]},tableData:[],tableLoading:!1,tableColumns:[{title:"服务单号",key:"serviceNo",sortable:!0,minWidth:150},{title:"服务类型",key:"serviceType",sortable:!0,minWidth:120,render:function(e,t){var r=h.SERVICETYPE.find(function(e){return t.row.serviceType===e.key});return e("span",r&&r.value||h.SERVICETYPE[0].value)}},{title:"会员ID",key:"memberId",sortable:!0,minWidth:150},{title:"姓名",key:"name",sortable:!0,minWidth:120},{title:"手机号",key:"phone",sortable:!0,minWidth:100},{title:"租赁时长(天)",key:"rentPeriod",sortable:!0,minWidth:140},{title:"服务单创建时间",key:"createDate",sortable:!0,minWidth:150},{title:"服务单结束时间",key:"finishDate",sortable:!0,minWidth:150},{title:"实际计费时长",key:"realChargingTime",sortable:!0,minWidth:130},{title:"预约商品ID",key:"reservedProductid",sortable:!0,minWidth:150},{title:"物品状态",key:"leaseholdStatus",filters:h.LEASEHOLDSTATUS.map(function(e){return{label:e.value,value:e.key}}),filterMultiple:!0,filterMethod:function(e,t){return t.leaseholdStatus===e},minWidth:130,render:function(e,t){var r=h.LEASEHOLDSTATUS.find(function(e){return t.row.leaseholdStatus===e.key});return e("span",r&&r.value)}},{title:"信用状态",key:"creditStatus",filters:h.CREDITSTATUS.map(function(e){return{label:e.value,value:e.key}}),filterMultiple:!0,filterMethod:function(e,t){return t.creditStatus===e},minWidth:130,render:function(e,t){var r=h.CREDITSTATUS.find(function(e){return t.row.creditStatus===e.key});return e("span",r&&r.value)}},{title:"取货门店",key:"deliveryStore",sortable:!0,minWidth:120},{title:"提货方式",key:"deliveryMode",filters:h.DELIVERYMODE.map(function(e){return{label:e.value,value:e.key}}),filterMultiple:!0,filterMethod:function(e,t){return t.deliveryMode===e},minWidth:130,render:function(e,t){var r=h.DELIVERYMODE.find(function(e){return t.row.deliveryMode===e.key});return e("span",r&&r.value)}},{title:"操作",key:"action",width:100,align:"center",render:function(t,r){return t("div",[t("Button",{props:{type:"primary",size:"small"},style:{marginRight:"5px"},on:{click:function(){e.$router.push("rent-service/"+r.row.serviceNo)}}},"详情")])}}]}},created:function(){this.mockTableData()},methods:{expandMoreCond:function(){this.moreCondModal=!0},saveMoreCond:function(){var e=this.moreCondModalForm,t=e.createDate,r=e.finishDate,a=e.leaseholdStatus,o=e.creditStatus,n=e.deliveryStore,i=e.deliveryMode;this.searchForm=m()(this.searchForm,{createDate:[].concat(d()(t)),finishDate:[].concat(d()(r)),leaseholdStatus:[].concat(d()(a)),creditStatus:[].concat(d()(o)),deliveryStore:n,deliveryMode:[].concat(d()(i))}),this.moreCondCount=this.calMoreCondCount(this.moreCondModalForm),this.moreCondModal=!1},cancelMoreCond:function(){var e=this.searchForm,t=e.createDate,r=e.finishDate,a=e.leaseholdStatus,o=e.creditStatus,n=e.deliveryStore,i=e.deliveryMode;this.moreCondModalForm={createDate:[].concat(d()(t)),finishDate:[].concat(d()(r)),leaseholdStatus:[].concat(d()(a)),creditStatus:[].concat(d()(o)),deliveryStore:n,deliveryMode:[].concat(d()(i))},this.moreCondCount=this.calMoreCondCount(this.moreCondModalForm),this.moreCondModal=!1},filterMethod:function(e,t){return t.includes(e)},calMoreCondCount:function(e){return+l()(e).reduce(function(t,r){return t||(e[r]instanceof Array?e[r].filter(function(e){return e}).length:e[r])},!1)},changecreateDate:function(e){this.moreCondModalForm.createDate=[].concat(d()(e))},changefinishDate:function(e){this.moreCondModalForm.changefinishDate=[].concat(d()(e))},mockTableData:function(e){var t=this;this.tableLoading=!0;this.$fetch("/RentalService/",e).then(function(e){var r=e.data,a=r.count,o=r.results;t.tableData=o,t.totalCount=a,t.tableLoading=!1}).catch(function(e){t.$Message.error({content:"查询失败"}),t.tableLoading=!1})},changePage:function(e){this.page=e,this.mockTableData({params:i()({offset:(e-1)*this.pageSize,limit:this.pageSize},this.formConditions(this.searchForm))})},changePageSize:function(e){this.pageSize=e,this.mockTableData({params:i()({offset:0,limit:e},this.formConditions(this.searchForm))})},search:function(){this.mockTableData({params:i()({offset:(this.page-1)*this.pageSize,limit:this.pageSize},this.formConditions(this.searchForm))})},reset:function(){this.$refs.searchForm.resetFields(),this.moreCondModalForm={createDate:[],finishDate:[],leaseholdStatus:[],creditStatus:[],deliveryStore:"",deliveryMode:[]},this.searchForm=m()(this.searchForm,{createDate:[],finishDate:[],leaseholdStatus:[],creditStatus:[],deliveryStore:"",deliveryMode:[]}),this.moreCondCount=0,this.mockTableData({params:{offset:(this.page-1)*this.pageSize,limit:this.pageSize}})},exportCsv:function(){this.$refs.table.exportCsv({filename:"租赁服务信息",columns:this.tableColumns.filter(function(e){return"action"!==e.key}),data:this.tableData})},formConditions:function(e){var t=this,r=l()(e).reduce(function(t,r){return 0!=e[r]&&("object"===o()(e[r])?t[r]=[].concat(d()(e[r])):t[r]=e[r]),t},{});return r.leaseholdStatus&&(r.leaseholdStatus=r.leaseholdStatus.reduce(function(e,r,a){return r&&e.push(t.leaseholdStatuss[a].key),e},[])),r.creditStatus&&(r.creditStatus=r.creditStatus.reduce(function(e,r,a){return r&&e.push(t.creditStatuss[a].key),e},[])),r.deliveryMode&&(r.deliveryMode=r.deliveryMode.reduce(function(e,r,a){return r&&e.push(t.deliveryModes[a].key),e},[])),r}}},v={render:function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"rent-service"},[r("div",{staticClass:"header"},[r("Form",{ref:"searchForm",attrs:{model:e.searchForm,"label-width":80}},[r("FormItem",{attrs:{label:"服务单号",prop:"serviceNo"}},[r("Input",{model:{value:e.searchForm.serviceNo,callback:function(t){e.$set(e.searchForm,"serviceNo",t)},expression:"searchForm.serviceNo"}})],1),e._v(" "),r("FormItem",{attrs:{label:"姓名",prop:"name"}},[r("Input",{model:{value:e.searchForm.name,callback:function(t){e.$set(e.searchForm,"name",t)},expression:"searchForm.name"}})],1),e._v(" "),r("FormItem",{attrs:{label:"手机号",prop:"phone"}},[r("Input",{model:{value:e.searchForm.phone,callback:function(t){e.$set(e.searchForm,"phone",t)},expression:"searchForm.phone"}})],1),e._v(" "),r("FormItem",[r("Badge",{attrs:{dot:"",count:e.moreCondCount}},[r("Button",{attrs:{type:"ghost",icon:"ios-search"},on:{click:e.expandMoreCond}},[e._v("更多筛选")])],1)],1),e._v(" "),r("FormItem",[r("Button",{attrs:{type:"primary"},nativeOn:{click:function(t){return e.search(t)}}},[e._v("搜索")]),e._v(" "),r("Button",{attrs:{type:"error"},nativeOn:{click:function(t){return e.reset(t)}}},[e._v("清空")]),e._v(" "),r("Button",{attrs:{type:"success"},nativeOn:{click:function(t){return e.exportCsv(t)}}},[e._v("导出")])],1)],1)],1),e._v(" "),r("div",{staticClass:"body"},[r("Table",{ref:"table",attrs:{data:e.tableData,columns:e.tableColumns,loading:e.tableLoading,stripe:""}})],1),e._v(" "),r("div",{staticClass:"footer"},[r("div",{staticClass:"pager",staticStyle:{float:"right"}},[r("Page",{attrs:{total:e.totalCount,current:1,"show-total":"","show-elevator":"","show-sizer":""},on:{"on-change":e.changePage,"on-page-size-change":e.changePageSize}})],1)]),e._v(" "),r("Modal",{staticClass:"edit-field-modal",attrs:{title:"更多筛选条件","mask-closable":!1,width:600,closable:!1},model:{value:e.moreCondModal,callback:function(t){e.moreCondModal=t},expression:"moreCondModal"}},[r("Form",{attrs:{model:e.moreCondModalForm,"label-width":100}},[r("FormItem",{attrs:{label:"服务单创建时间",prop:"createDate"}},[r("DatePicker",{attrs:{type:"datetimerange",format:"yyyy-MM-dd HH:mm:ss",placement:"bottom-end",placeholder:"选择服务单创建时间区间"},on:{"on-change":e.changecreateDate}})],1),e._v(" "),r("FormItem",{attrs:{label:"服务单结束时间",prop:"finishDate"}},[r("DatePicker",{attrs:{type:"datetimerange",format:"yyyy-MM-dd HH:mm:ss",placement:"bottom-end",placeholder:"选择服务单结束时间区间"},on:{"on-change":e.changefinishDate}})],1),e._v(" "),r("FormItem",{attrs:{label:"物品状态",prop:"leaseholdStatus"}},[r("enum-selector",{attrs:{selected:e.moreCondModalForm.leaseholdStatus,items:e.leaseholdStatus,single:!1}})],1),e._v(" "),r("FormItem",{attrs:{label:"信用状态",prop:"creditStatus"}},[r("enum-selector",{attrs:{selected:e.moreCondModalForm.creditStatus,items:e.creditStatus,single:!1}})],1),e._v(" "),r("FormItem",{attrs:{label:"取货门店",prop:"deliveryStore"}},[r("Input",{model:{value:e.moreCondModalForm.deliveryStore,callback:function(t){e.$set(e.moreCondModalForm,"deliveryStore",t)},expression:"moreCondModalForm.deliveryStore"}})],1),e._v(" "),r("FormItem",{attrs:{label:"提货方式",prop:"deliveryMode"}},[r("enum-selector",{attrs:{selected:e.moreCondModalForm.deliveryMode,items:e.deliveryMode,single:!1}})],1),e._v(" "),r("FormItem",[r("Button",{attrs:{type:"success"},on:{click:e.saveMoreCond}},[e._v("保存")]),e._v(" "),r("Button",{staticStyle:{"margin-left":"8px"},attrs:{type:"ghost"},on:{click:e.cancelMoreCond}},[e._v("取消")])],1)],1)],1)],1)},staticRenderFns:[]};var p=r("VU/8")(f,v,!1,function(e){r("wlCC")},null,null);t.default=p.exports},wlCC:function(e,t){}});