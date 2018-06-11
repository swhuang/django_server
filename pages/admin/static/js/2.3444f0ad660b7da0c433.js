webpackJsonp([2,8],{"/5yd":function(e,t){},B7tt:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=a("fZjL"),o=a.n(r),s=a("d7EF"),i=a.n(s),l=a("Dd8w"),n=a.n(l),c=a("xAvK"),d={props:{imageMaxNum:{type:Number,default:6},imageMaxSize:{type:Number,default:2048,validator:function(e){return!(e%1024)}},showUploadList:{type:Boolean,default:!1},imageList:{type:Array,default:function(){return[]}},multiple:{type:Boolean,default:!1},action:{type:String,required:!0},uploadImage:{type:Function,default:function(){}},removeImage:{type:Function,default:function(){}},data:{type:Object,default:function(){return{}}},withCredentials:{type:Boolean,default:!1},headers:{type:Object,default:function(){return{}}}},data:function(){return{imgName:"",visible:!1,defaultList:this.imageList.map(function(e){return n()({},e)}),uploadList:[],rawImgUrl:""}},watch:{imageList:{handler:function(e,t){var a=this;e.forEach(function(e,t){e&&!e.local&&(a.uploadList[t]=n()({},e,{percentage:100,status:"finished"}))}),this.$forceUpdate()},deep:!0}},mounted:function(){this.uploadList=this.$refs.upload&&this.$refs.upload.fileList||[]},beforeDestroy:function(){this.uploadList.filter(function(e){return e.local}).forEach(function(e){window.URL.revokeObjectURL(e.url)})},methods:{handleSuccess:function(e,t){this.uploadImage()},handleRemove:function(e){var t=this.uploadList.indexOf(e);this.uploadList.splice(t,1),this.imageList.splice(t,1),this.removeImage()},handleView:function(e){this.rawImgUrl=this.uploadList.find(function(t){return t.name===e}).url,this.visible=!0},handleFormatError:function(e){this.$Notice.warning({title:"图片格式错误",desc:e.name+" 格式错误, 请选择.jpg, .jpeg, .png文件."})},handleMaxSize:function(e){var t=this.imageMaxSize<1024?"KB":"M";this.$Notice.warning({title:"图片过大",desc:e.name+" 大小不能超过"+(this.imageMaxSize/1024||this.imageMaxSize)+t})},handleBeforeUpload:function(e){var t=this.uploadList.length<this.imageMaxNum;if(!t)return this.$Notice.warning({title:"最多上传"+this.imageMaxNum+"张图片"}),t;if("javascript(void)"===this.action){if(Math.ceil(e.size/1024)>this.imageMaxSize)return this.handleMaxSize(e),!1;var a=this,r=new Image;return r.src=window.URL.createObjectURL(e),r.onload=function(){a.uploadList.push({name:e.name,percentage:100,status:"finished",url:this.src,local:!0}),a.imageList.push({name:e.name,file:e,local:!0})},!1}return!0}}},m={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"image-uploader"},[e._l(e.uploadList,function(t){return a("div",{key:t.url,staticClass:"upload-list"},["finished"===t.status?[a("img",{attrs:{src:t.avatar||t.url}}),e._v(" "),a("div",{staticClass:"upload-list-cover"},[a("Icon",{attrs:{type:"ios-eye-outline"},nativeOn:{click:function(a){e.handleView(t.name)}}}),e._v(" "),a("Icon",{attrs:{type:"ios-trash-outline"},nativeOn:{click:function(a){e.handleRemove(t)}}})],1)]:[t.showProgress?a("Progress",{attrs:{percent:t.percentage,"hide-info":""}}):e._e()]],2)}),e._v(" "),e.uploadList.length<e.imageMaxNum?a("Upload",{ref:"upload",staticClass:"upload",attrs:{"show-upload-list":e.showUploadList,"default-file-list":e.defaultList,"on-success":e.handleSuccess,format:["jpg","jpeg","png"],accept:"image/*","max-size":e.imageMaxSize,"on-format-error":e.handleFormatError,"on-exceeded-size":e.handleMaxSize,"before-upload":e.handleBeforeUpload,multiple:e.multiple,type:"drag",action:e.action,data:e.data,"with-credentials":e.withCredentials,headers:e.headers}},[a("div",{staticClass:"upload-icon"},[a("Icon",{attrs:{type:"camera"}})],1)]):e._e(),e._v(" "),a("Modal",{attrs:{width:700,title:"查看原图"},model:{value:e.visible,callback:function(t){e.visible=t},expression:"visible"}},[e.visible?a("img",{staticClass:"raw-image",attrs:{src:e.rawImgUrl}}):e._e()])],2)},staticRenderFns:[]};var u={components:{"image-uploader":a("VU/8")(d,m,!1,function(e){a("T0Qu")},null,null).exports},props:{modeType:{type:Number,default:0}},data:function(){return{mode:this.modeType,categoryOfGood:c.CATEGORYOFGOOD,brandOptions:c.BRANDOPTIONS,seriesOptions:c.SERIESOPTIONS,releaseStatus:c.RELEASESTATUS,certificates:c.CERTIFICATES,MainImageNum:c.MAINIMAGENUM,imageMaxSize:c.MAINIMAGEMAXSIZE,goldTypePurity:c.GOLDTYPEPURITY,formBak:{},form:{productid:"",category:"",model:"",title:"",goldType:"",goldPurity:"",releaseStatus:"",brand:"",series:"",certificate:"",size:"",goldContent:"",diamondWeight:"",sellingPrice:"",deposit:"",rent:"",rentcycle:0,reletcycle:0,desc:"",remark:"",createdDate:"",createdBy:"",MainImage0:[],MainImage1:[],MainImage2:[],MainImage3:[],MainImage4:[],MainImage5:[],detailImages:[]},ruleValidate:{category:[{required:!0,message:"商品类别不能为空",trigger:"blur"}],model:[{required:!0,message:"商品型号不能为空",trigger:"blur"}],title:[{required:!0,message:"商品名称不能为空",trigger:"blur"}],releaseStatus:[{required:!0,message:"发布状态不能为空",trigger:"blur"}],goldType:[{required:!0,message:"镶嵌材质不能为空",trigger:"blur"}],certificate:[{required:!0,message:"证书不能为空",trigger:"blur"}],size:[{required:!0,message:"尺寸不能为空",trigger:"blur"}],goldContent:[{trigger:"change",validator:function(e,t,a){var r=parseFloat(t,10);isNaN(r)&&a(new Error("输入必须为数值")),r<=0&&a(new Error("含金量不能小于0")),a()}}],diamondWeight:[{trigger:"change",validator:function(e,t,a){isNaN(+t)&&a(new Error("输入必须为数值")),parseFloat(t,10)<=0&&a(new Error("钻石重量不能小于0")),a()}}],sellingPrice:[{required:!0,message:"销售价不能为空",trigger:"blur"},{trigger:"change",validator:function(e,t,a){isNaN(+t)&&a(new Error("输入必须为数值")),parseFloat(t,10)<=0&&a(new Error("销售价不能小于0")),a()}}],deposit:[{required:!0,message:"押金不能为空",trigger:"blur"},{trigger:"change",validator:function(e,t,a){isNaN(+t)&&a(new Error("输入必须为数值")),parseFloat(t,10)<=0&&a(new Error("押金不能小于0")),a()}}],rent:[{required:!0,message:"租金不能为空",trigger:"blur"},{trigger:"change",validator:function(e,t,a){isNaN(+t)&&a(new Error("输入必须为数值")),parseFloat(t,10)<=0&&a(new Error("租金不能小于0")),a()}}],rentcycle:[{required:!0,trigger:"blur",validator:function(e,t,a){var r=parseFloat(t,10),o=parseInt(t,10);(isNaN(+t)||r!==o)&&a(new Error("输入必须为整数")),o<1&&a(new Error("起租周期至少1天")),a()}},{trigger:"change",validator:function(e,t,a){var r=parseFloat(t,10),o=parseInt(t,10);(isNaN(+t)||r!==o)&&a(new Error("输入必须为整数")),o<1&&a(new Error("起租周期至少1天")),a()}}],reletcycle:[{required:!0,trigger:"blur",validator:function(e,t,a){var r=parseFloat(t,10),o=parseInt(t,10);(isNaN(+t)||r!==o)&&a(new Error("输入必须为整数")),o<1&&a(new Error("续租周期至少1天")),a()}},{trigger:"change",validator:function(e,t,a){var r=parseFloat(t,10),o=parseInt(t,10);(isNaN(+t)||r!==o)&&a(new Error("输入必须为整数")),o<1&&a(new Error("续租周期至少1天")),a()}}],desc:[{trigger:"change",type:"string",max:500,message:"商品描述至多500字符"}],remark:[{trigger:"change",type:"string",max:500,message:"备注至多500字符"}]}}},created:function(){var e=this;if(!this.modeType){this.form.productid=this.$route.params.id,this.$fetch("/product/",{params:{productid:this.form.productid}}).then(function(t){var a=t.data.results;if(a&&a.length){for(var r=a[0],o=0;o<e.MainImageNum;++o)r["MainImage"+o]=r["MainImage"+o]&&[n()({},r["MainImage"+o])]||[];r.detailImages=r.detailImages&&[n()({},r.detailImages)]||[],e.form=n()({},r),e.formBak=n()({},r)}else e.$Message.error({content:"未找到该商品的详细信息"})}).catch(function(t){e.$Message.error({content:"未找到该商品的详细信息"})})}},methods:{changeGoldTypePurity:function(e,t){var a=i()(e,2),r=a[0],o=a[1];this.form.goldType=r,this.form.goldPurity=o},formPostdata:function(){var e=this,t=new FormData;return o()(this.form).forEach(function(a){var r=e.form[a];a.includes("Image")?(r&&r[0]&&r[0].file&&t.append(a,r[0].file,r[0].name),r&&!r.length&&t.append(a,"")):t.append(a,r)}),t},save:function(){var e=this;this.$refs.goodsForm.validate(function(t){if(t){e.$fetch("/productupdate/",{headers:{"Content-Type":"multipart/form-data"},data:e.formPostdata(),method:"post"}).then(function(t){for(var a=t.data,r=0;r<e.MainImageNum;++r)a["MainImage"+r]=a["MainImage"+r]&&[n()({},a["MainImage"+r])]||[];a.detailImages=a.detailImages&&[n()({},a.detailImages)]||[],e.form=n()({},a),e.formBak=n()({},a),e.$Message.success({content:"保存成功"})}).catch(function(t){e.$Message.error({content:"保存失败"})})}else e.$Message.error({content:"保存失败"})})},cancel:function(){this.form=n()({},this.formBak),this.$Message.success({content:"重置成功"})},filterMethod:function(e,t){return t.includes(e)}}},p={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"goods-detail"}},[a("Form",{ref:"goodsForm",attrs:{model:e.form,"label-width":150,rules:e.ruleValidate}},[a("section",[a("header",[e._v("基本信息")]),e._v(" "),a("div",{staticClass:"section-body"},[e.mode?e._e():a("FormItem",{attrs:{label:"商品ID",prop:"productid"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("p",[e._v(e._s(e.form.productid))])])],1)],1),e._v(" "),a("FormItem",{attrs:{label:"商品型号",prop:"model"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[e.mode?a("Input",{attrs:{placeholder:"输入商品型号"},model:{value:e.form.model,callback:function(t){e.$set(e.form,"model",t)},expression:"form.model"}}):a("p",[e._v(e._s(e.form.model))])],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"商品类别",prop:"category"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Select",{model:{value:e.form.category,callback:function(t){e.$set(e.form,"category",t)},expression:"form.category"}},e._l(e.categoryOfGood,function(t){return a("Option",{key:t.key,attrs:{value:t.key}},[e._v("\n                "+e._s(t.value)+"\n              ")])}))],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"商品名称",prop:"title"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Input",{attrs:{placeholder:"输入商品名称"},model:{value:e.form.title,callback:function(t){e.$set(e.form,"title",t)},expression:"form.title"}})],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"是否发布",prop:"releaseStatus"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Select",{model:{value:e.form.releaseStatus,callback:function(t){e.$set(e.form,"releaseStatus",t)},expression:"form.releaseStatus"}},e._l(e.releaseStatus,function(t){return a("Option",{key:t.key,attrs:{value:t.key}},[e._v("\n                "+e._s(t.label)+"\n              ")])}))],1)],1)],1)],1)]),e._v(" "),a("section",[a("header",[e._v("\n        品质信息\n      ")]),e._v(" "),a("div",{staticClass:"section-body"},[a("FormItem",{attrs:{label:"品牌",prop:"brand"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("AutoComplete",{attrs:{data:e.brandOptions,"filter-method":e.filterMethod,placeholder:"输入品牌名称"},model:{value:e.form.brand,callback:function(t){e.$set(e.form,"brand",t)},expression:"form.brand"}})],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"系列",prop:"series"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("AutoComplete",{attrs:{data:e.seriesOptions,"filter-method":e.filterMethod,placeholder:"输入系列名称"},model:{value:e.form.series,callback:function(t){e.$set(e.form,"series",t)},expression:"form.series"}})],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"证书",prop:"certificate"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Select",{model:{value:e.form.certificate,callback:function(t){e.$set(e.form,"certificate",t)},expression:"form.certificate"}},e._l(e.certificates,function(t){return a("Option",{key:t.key,attrs:{value:t.key}},[e._v("\n                "+e._s(t.value)+"\n              ")])}))],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"镶嵌材质",prop:"goldType"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Cascader",{attrs:{data:e.goldTypePurity,trigger:"hover"},on:{"on-change":e.changeGoldTypePurity}})],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"尺寸",prop:"size"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Input",{attrs:{placeholder:"输入钻石重量"},model:{value:e.form.size,callback:function(t){e.$set(e.form,"size",t)},expression:"form.size"}})],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"钻石重量",prop:"diamondWeight"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Input",{attrs:{placeholder:"输入钻石重量"},model:{value:e.form.diamondWeight,callback:function(t){e.$set(e.form,"diamondWeight",t)},expression:"form.diamondWeight"}},[a("span",{attrs:{slot:"append"},slot:"append"},[e._v("克")])])],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"含金量",prop:"goldContent"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Input",{attrs:{placeholder:"输入含金量"},model:{value:e.form.goldContent,callback:function(t){e.$set(e.form,"goldContent",t)},expression:"form.goldContent"}},[a("span",{attrs:{slot:"append"},slot:"append"},[e._v("克")])])],1)],1)],1)],1)]),e._v(" "),a("section",[a("header",[e._v("\n        销售信息\n      ")]),e._v(" "),a("div",{staticClass:"section-body"},[a("FormItem",{attrs:{label:"销售价",prop:"sellingPrice"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Input",{attrs:{placeholder:"输入销售价"},model:{value:e.form.sellingPrice,callback:function(t){e.$set(e.form,"sellingPrice",t)},expression:"form.sellingPrice"}},[a("span",{attrs:{slot:"append"},slot:"append"},[e._v("元")])])],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"押金",prop:"deposit"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Input",{attrs:{placeholder:"输入押金"},model:{value:e.form.deposit,callback:function(t){e.$set(e.form,"deposit",t)},expression:"form.deposit"}},[a("span",{attrs:{slot:"append"},slot:"append"},[e._v("元")])])],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"租金",prop:"rent"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Input",{attrs:{placeholder:"输入租金"},model:{value:e.form.rent,callback:function(t){e.$set(e.form,"rent",t)},expression:"form.rent"}},[a("span",{attrs:{slot:"append"},slot:"append"},[e._v("元")])])],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"起租周期",prop:"rentcycle"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Input",{attrs:{placeholder:"输入起租周期"},model:{value:e.form.rentcycle,callback:function(t){e.$set(e.form,"rentcycle",t)},expression:"form.rentcycle"}},[a("span",{attrs:{slot:"append"},slot:"append"},[e._v("天")])])],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"续租周期",prop:"reletcycle"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Input",{attrs:{placeholder:"输入续租周期"},model:{value:e.form.reletcycle,callback:function(t){e.$set(e.form,"reletcycle",t)},expression:"form.reletcycle"}},[a("span",{attrs:{slot:"append"},slot:"append"},[e._v("天")])])],1)],1)],1)],1)]),e._v(" "),a("section",[a("header",[e._v("\n        描述信息\n      ")]),e._v(" "),a("div",{staticClass:"section-body"},[a("FormItem",{staticClass:"main-images",attrs:{label:"商品图片"}},e._l(e.MainImageNum,function(t){return a("image-uploader",{key:t-1,attrs:{"image-list":e.form["MainImage"+(t-1)],"image-max-num":1,"image-max-size":e.imageMaxSize,action:"javascript(void)"}})})),e._v(" "),a("FormItem",{attrs:{label:"商品详情图片",prop:"detailImages"}},[a("image-uploader",{attrs:{"image-list":e.form.detailImages,"image-max-num":1,"image-max-size":e.imageMaxSize,action:"javascript(void)"}})],1),e._v(" "),a("FormItem",{attrs:{label:"商品描述",prop:"desc"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Input",{attrs:{type:"textarea",autosize:{minRows:3},maxlength:500,placeholder:"输入商品描述信息(不超过500字符)"},model:{value:e.form.desc,callback:function(t){e.$set(e.form,"desc",t)},expression:"form.desc"}})],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"备注",prop:"remark"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("Input",{attrs:{type:"textarea",autosize:{minRows:3},maxlength:500,placeholder:"输入商品备注信息(不超过500字符)"},model:{value:e.form.remark,callback:function(t){e.$set(e.form,"remark",t)},expression:"form.remark"}})],1)],1)],1),e._v(" "),e.mode?a("FormItem",[a("Button",{attrs:{type:"success"},on:{click:e.save}},[e._v("保存")]),e._v(" "),a("Button",{staticStyle:{"margin-left":"8px"},attrs:{type:"ghost"},on:{click:e.cancel}},[e._v("重置")])],1):e._e()],1)]),e._v(" "),e.mode?e._e():a("section",[a("header",[e._v("\n        其他信息\n      ")]),e._v(" "),a("div",{staticClass:"section-body"},[a("FormItem",{attrs:{label:"创建时间",prop:"createdDate"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("p",[e._v(e._s(e.form.createdDate))])])],1)],1),e._v(" "),a("FormItem",{attrs:{label:"创建人",prop:"createdBy"}},[a("Row",[a("Col",{attrs:{xs:24,md:16,lg:12}},[a("p",[e._v(e._s(e.form.createdBy))])])],1)],1),e._v(" "),a("FormItem",[a("Button",{attrs:{type:"success"},on:{click:e.save}},[e._v("保存")]),e._v(" "),a("Button",{staticStyle:{"margin-left":"8px"},attrs:{type:"ghost"},on:{click:e.cancel}},[e._v("重置")])],1)],1)])])],1)},staticRenderFns:[]};var f=a("VU/8")(u,p,!1,function(e){a("dsU8")},null,null);t.default=f.exports},T0Qu:function(e,t){},dsU8:function(e,t){},lVdz:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r={components:{"goods-detail":a("B7tt").default},data:function(){return{}}},o={render:function(){var e=this.$createElement;return(this._self._c||e)("goods-detail",{attrs:{"mode-type":1}})},staticRenderFns:[]};var s=a("VU/8")(r,o,!1,function(e){a("/5yd")},null,null);t.default=s.exports}});