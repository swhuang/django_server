webpackJsonp([4],{"7Vh4":function(e,t){},Qm9m:function(e,t){},UCIx:function(e,t,o){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=o("pFYg"),n=o.n(r),a=o("Dd8w"),i=o.n(a),s=o("fZjL"),l=o.n(s),c=o("Gu7T"),d=o.n(c),u=o("woOf"),m=o.n(u),h=o("xAvK"),p={props:{selected:{type:Array,default:[]},items:{type:Array,default:[]},single:{type:Boolean,default:!0}},methods:{changeSelected:function(e,t){this.single&&this.selected.fill(!1),this.selected[t]=e,this.$forceUpdate()}}},f={render:function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"enum-selector"},e._l(e.items,function(t,r){return o("span",{key:t.key,staticClass:"enum-selector__item",class:{active:e.selected[r]}},[o("input",{attrs:{type:"checkbox"},domProps:{checked:e.selected[r]},on:{change:function(t){e.changeSelected(t.target.checked,r)}}}),e._v("\n    "+e._s(t.value)+"\n  ")])}))},staticRenderFns:[]};var g={components:{"enum-selector":o("VU/8")(p,f,!1,function(e){o("7Vh4")},null,null).exports},data:function(){var e=this;return{categoryOfGood:h.CATEGORYOFGOOD,goldTypes:h.GOLDTYPE,brandOptions:h.BRANDOPTIONS,seriesOptions:h.SERIESOPTIONS,page:1,pageSize:10,totalCount:0,searchForm:{category:[],model:"",title:"",goldType:[],brand:"",series:""},moreCondModal:!1,moreCondCount:0,moreCondModalForm:{category:[],goldType:[],brand:"",series:""},tableData:[],tableLoading:!1,tableColumns:[{title:"商品ID",key:"productid",sortable:!0,minWidth:150},{title:"商品类别",key:"category",sortable:!0,minWidth:100,render:function(e,t){var o=h.CATEGORYOFGOOD.find(function(e){return t.row.category===e.key});return e("span",o&&o.value)}},{title:"商品型号",key:"model",sortable:!0,minWidth:150},{title:"商品名称",key:"title",sortable:!0,minWidth:100},{title:"品牌",key:"brand",sortable:!0,minWidth:100},{title:"系列",key:"series",sortable:!0,minWidth:100},{title:"镶嵌材质",key:"goldType",filters:h.GOLDTYPE.map(function(e){return{label:e.value,value:e.key}}),filterMultiple:!0,filterMethod:function(e,t){return t.goldType===e},minWidth:100,render:function(e,t){var o=h.GOLDTYPE.find(function(e){return t.row.goldType===e.key});return e("span",o&&o.value)}},{title:"材质纯度",key:"goldPurity",filters:h.GOLDPURITY.map(function(e){return{label:e.value,value:e.key}}),filterMultiple:!0,filterMethod:function(e,t){return t.goldPurity===e},minWidth:100,render:function(e,t){var o=h.GOLDPURITY.find(function(e){return t.row.goldPurity===e.key});return e("span",o&&o.value)}},{title:"含金量（克）",key:"goldContent",sortable:!0,minWidth:100},{title:"钻石重量（克）",key:"diamondWeight",sortable:!0,minWidth:100},{title:"销售价",key:"sellingPrice",sortable:!0,minWidth:100},{title:"租金",key:"rent",sortable:!0,minWidth:100},{title:"押金",key:"deposit",sortable:!0,minWidth:100},{title:"发布状态",key:"releaseStatus",filters:h.RELEASESTATUS.map(function(e){return{label:e.value,value:e.key}}),filterMultiple:!0,filterMethod:function(e,t){return t.releaseStatus===e},minWidth:100,render:function(e,t){var o=h.RELEASESTATUS.find(function(e){return t.row.releaseStatus===e.key});return e("span",o&&o.value)}},{title:"操作",key:"action",width:100,align:"center",render:function(t,o){return t("div",[t("Button",{props:{type:"primary",size:"small"},style:{marginRight:"5px"},on:{click:function(){e.$router.push("goods/"+o.row.productid)}}},"详情")])}}]}},created:function(){this.mockTableData()},methods:{expandMoreCond:function(){this.moreCondModal=!0},saveMoreCond:function(){var e=this.moreCondModalForm,t=e.category,o=e.goldType,r=e.brand,n=e.series;this.searchForm=m()(this.searchForm,{category:[].concat(d()(t)),goldType:[].concat(d()(o)),brand:r,series:n}),this.moreCondCount=this.calMoreCondCount(this.moreCondModalForm),this.moreCondModal=!1},cancelMoreCond:function(){var e=this.searchForm,t=e.category,o=e.goldType,r=e.brand,n=e.series;this.moreCondModalForm={category:[].concat(d()(t)),goldType:[].concat(d()(o)),brand:r,series:n},this.moreCondCount=this.calMoreCondCount(this.moreCondModalForm),this.moreCondModal=!1},filterMethod:function(e,t){return t.includes(e)},calMoreCondCount:function(e){return+l()(e).reduce(function(t,o){return t||(e[o]instanceof Array?e[o].filter(function(e){return e}).length:e[o])},!1)},mockTableData:function(e){var t=this;this.tableLoading=!0;this.$fetch("/product/",e).then(function(e){var o=e.data,r=o.count,n=o.results;t.tableData=n,t.totalCount=r,t.tableLoading=!1}).catch(function(e){t.$Message.error({content:e}),t.tableLoading=!1})},changePage:function(e){this.page=e,this.mockTableData({params:{offset:(e-1)*this.pageSize,limit:this.pageSize}})},changePageSize:function(e){this.pageSize=e,this.mockTableData({params:{offset:0,limit:e}})},search:function(){this.mockTableData({params:i()({offset:(this.page-1)*this.pageSize,limit:this.pageSize},this.formConditions(this.searchForm))})},reset:function(){this.$refs.searchForm.resetFields(),this.moreCondModalForm={category:[],goldType:[],brand:"",series:""},this.searchForm={category:[],goldType:[],brand:"",series:""},this.moreCondCount=0,this.mockTableData({params:{offset:(this.page-1)*this.pageSize,limit:this.pageSize}})},exportCsv:function(){this.$refs.table.exportCsv({filename:"会员信息",columns:this.tableColumns.filter(function(e){return"action"!==e.key}),data:this.tableData})},formConditions:function(e){var t=this,o=l()(e).reduce(function(t,o){return 0!=e[o]&&("object"===n()(e[o])?t[o]=[].concat(d()(e[o])):t[o]=e[o]),t},{});return o.category&&(o.category=o.category.reduce(function(e,o,r){return o&&e.push(t.categoryOfGood[r].key),e},[])),o.goldType&&(o.goldType=o.goldType.reduce(function(e,o,r){return o&&e.push(t.goldTypes[r].key),e},[])),o}}},y={render:function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"goods"},[o("div",{staticClass:"header"},[o("Form",{ref:"searchForm",attrs:{model:e.searchForm,"label-width":80}},[o("FormItem",{attrs:{label:"商品型号",prop:"model"}},[o("Input",{model:{value:e.searchForm.model,callback:function(t){e.$set(e.searchForm,"model",t)},expression:"searchForm.model"}})],1),e._v(" "),o("FormItem",{attrs:{label:"商品名称",prop:"title"}},[o("Input",{model:{value:e.searchForm.title,callback:function(t){e.$set(e.searchForm,"title",t)},expression:"searchForm.title"}})],1),e._v(" "),o("FormItem",[o("Badge",{attrs:{dot:"",count:e.moreCondCount}},[o("Button",{attrs:{type:"ghost",icon:"ios-search"},on:{click:e.expandMoreCond}},[e._v("更多筛选")])],1)],1),e._v(" "),o("FormItem",[o("Button",{attrs:{type:"primary"},nativeOn:{click:function(t){return e.search(t)}}},[e._v("搜索")]),e._v(" "),o("Button",{attrs:{type:"error"},nativeOn:{click:function(t){return e.reset(t)}}},[e._v("清空")]),e._v(" "),o("Button",{attrs:{type:"success"},nativeOn:{click:function(t){return e.exportCsv(t)}}},[e._v("导出")])],1)],1)],1),e._v(" "),o("div",{staticClass:"body"},[o("Table",{ref:"table",attrs:{data:e.tableData,columns:e.tableColumns,loading:e.tableLoading,stripe:""}})],1),e._v(" "),o("div",{staticClass:"footer"},[o("div",{staticClass:"pager",staticStyle:{float:"right"}},[o("Page",{attrs:{total:e.totalCount,current:1,"show-total":"","show-elevator":"","show-sizer":""},on:{"on-change":e.changePage,"on-page-size-change":e.changePageSize}})],1)]),e._v(" "),o("Modal",{staticClass:"edit-field-modal",attrs:{title:"更多筛选条件","mask-closable":!1,width:700},model:{value:e.moreCondModal,callback:function(t){e.moreCondModal=t},expression:"moreCondModal"}},[o("Form",{attrs:{model:e.moreCondModalForm,"label-width":70}},[o("FormItem",{attrs:{label:"商品类别",prop:"category"}},[o("enum-selector",{attrs:{selected:e.moreCondModalForm.category,items:e.categoryOfGood,single:!1}})],1),e._v(" "),o("FormItem",{attrs:{label:"镶嵌材质",prop:"goldType"}},[o("enum-selector",{attrs:{selected:e.moreCondModalForm.goldType,items:e.goldTypes,single:!1}})],1),e._v(" "),o("FormItem",{attrs:{label:"品牌",prop:"brand"}},[o("AutoComplete",{staticStyle:{width:"400px"},attrs:{data:e.brandOptions,"filter-method":e.filterMethod,placeholder:"输入关键字搜索品牌"},model:{value:e.moreCondModalForm.brand,callback:function(t){e.$set(e.moreCondModalForm,"brand",t)},expression:"moreCondModalForm.brand"}})],1),e._v(" "),o("FormItem",{attrs:{label:"系列",prop:"series"}},[o("AutoComplete",{staticStyle:{width:"400px"},attrs:{data:e.seriesOptions,"filter-method":e.filterMethod,placeholder:"输入关键字搜索系列"},model:{value:e.moreCondModalForm.series,callback:function(t){e.$set(e.moreCondModalForm,"series",t)},expression:"moreCondModalForm.series"}})],1),e._v(" "),o("FormItem",[o("Button",{attrs:{type:"success"},on:{click:e.saveMoreCond}},[e._v("保存")]),e._v(" "),o("Button",{staticStyle:{"margin-left":"8px"},attrs:{type:"ghost"},on:{click:e.cancelMoreCond}},[e._v("取消")])],1)],1)],1)],1)},staticRenderFns:[]};var v=o("VU/8")(g,y,!1,function(e){o("Qm9m")},null,null);t.default=v.exports}});
//# sourceMappingURL=4.e77ee8427ed2f00b074a.js.map