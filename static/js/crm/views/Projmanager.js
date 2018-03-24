/**
 * Created by shengweihuang on 2017/11/24.
 */
/**
 * Created by shengweihuang on 2017/11/8.
 */
/**
 * Created by shengweihuang on 2017/11/6.啊实打实
 */

$(function () {
    var oTable = new TableInit();
    //2.初始化Button的点击事件
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();


});

//var taskService = abp.services.app.task;
var _table = $('#tb-tasks');

//bootstrap-table工具栏按钮事件初始化


//bootstrap-table工具栏按钮事件初始化
var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        console.log("button init!")
        //初始化页面上面的按钮事件
        $("#btn-add")
            .click(function () {
                console.log('add-btn clicked')
                $("#exampleModal").modal("show");
            });

        $("#btn-edit")
            .click(function () {
                var selectedRaido = _table.bootstrapTable('getSelections');
                if (selectedRaido.length === 0) {
                    abp.notify.warn("请先选择要编辑的行！");
                } else {
                    editTask(selectedRaido[0].Id);
                }
            });

        $("#btn-delete")
            .click(function () {
                var selectedRaido = _table.bootstrapTable('getSelections');
                if (selectedRaido.length === 0) {
                    abp.notify.warn("请先选择要删除的行！");
                } else {
                    deleteTask(selectedRaido[0].Id);
                }
            });

        $("#btn-query")
            .click(function () {
                /*_table.bootstrapTable('refresh');*/
                $('#tb-tasks').bootstrapTable('refresh');
                console.log("clicked!");
            });

        $("#btn_new").click(function() {
            $.ajax(
                {
                    type: 'POST',
                    url: '/local/CreateProject/',
                    data: {
                        'projname': $("#id_projname").val()
                    },
                    dataType: 'json',
                    async:false,
                    success: function (data) {
                        if(data.ok) {
                            make_warning("#newPrjWarning", "添加成功");
                            /*$("#exampleModal").modal("hide");*/
                            $('#tb-tasks').bootstrapTable('refresh');
                        }
                        else
                        {
                            make_warning("#newPrjWarning", data.msg);
                        }
                    },
                    error: function (XmlHttprequest, textStatus, errorThrown) {
                        make_warning('#newPrjWarning', '发生错误，请稍后再试');
                    }
                }
            )
        });
        
        $("#order_new").click(function (e) {

            $(this).parent().parent().append("<div class='form-group' id='new1'></div>");
            $('#new1').load('/local/CreateOrder')
        })

        $("#exampleModal").on('hidden.bs.modal', function(e){
            $('#newPrjWarning').text('');
            $('#id_projname').val('');
            $('#new1').remove();
        })

    };
    return oInit;
};

//指定table表体操作事件
window.operateEvents = {
    'click .like': function (e, value, row, index) {
        alert('You click like icon, row: ' + JSON.stringify(row));
        console.log(value, row, index);
    },
    'click .edit': function (e, value, row, index) {
        editTask(row.Id);
    },
    'click .remove': function (e, value, row, index) {
        deleteTask(row.Id);
    }
};

queryParams = function (params) {
    var temp = { //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
        limit: params.limit,
        //页面大小
        offset: params.offset,
        //页码
        sortfiled: params.sort,
        //排序字段
        sortway: params.order,
        //升序降序
        search: {
            'proj_name': $("#id_projname").val(),
            'proj_id': $("#id_projid").val()
        },
        //自定义传参-任务名称
        status: $("#txt-search-status").val(),
        //自定义传参-任务状态
        table_name: 'project'

    };
    return temp;
};


var TableInit = function () {
    showState = function (value, row, index) {
        return value
    }
    showDate = function (data) {
        return data
    }
    $('#tb-tasks').bootstrapTable({
        url: '/local/GetTableData/', //请求后台的URL（*）
        method: 'post', //请求方式（*）
        toolbar: '#toolbar', //工具按钮用哪个容器
        striped: true, //是否显示行间隔色
        cache: false, //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pagination: true, //是否显示分页（*）
        sortable: true, //是否启用排序
        sortOrder: "asc", //排序方式
        queryParams: queryParams, //传递参数（*）
        sidePagination: "server", //分页方式：client客户端分页，server服务端分页（*）
        pageNumber: 1, //初始化加载第一页，默认第一页
        pageSize: 5, //每页的记录行数（*）
        pageList: [10, 25, 50, 100], //可供选择的每页的行数（*）
        search: false, //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
        strictSearch: true,
        showColumns: true, //是否显示所有的列
        showRefresh: true, //是否显示刷新按钮
        minimumCountColumns: 2, //最少允许的列数
        clickToSelect: true, //是否启用点击选中行
        //height: 500, //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
        contentType: "application/x-www-form-urlencoded",
        uniqueId: "Id", //每一行的唯一标识，一般为主键列
        showToggle: true, //是否显示详细视图和列表视图的切换按钮
        cardView: false, //是否显示详细视图
        detailView: false, //是否显示父子表
        columns: [
            {
                radio: true
            }, {
                field: 'proj_id',
                title: '项目编号'
            },{
                field: 'name',
                title: '商户名称',
                sortable: true
            }, {
                field: 'memberid',
                title: '用户编号'
            }, {
                field: 'id_name',
                title: '身份证姓名'
            },{
                field: 'id_type',
                title: '证件类型'
            },
            {
                field: 'id_no',
                title: '证件号'
            },
            {
                field: 'phone',
                title: '电话',
                formatter: showDate
            },{
                field: 'proj_name',
                title: '项目名称'
            },{
                field: 'proj_id',
                title: '项目编号'
            },{
                field: 'payment_status',
                title: '订单状态'
            },{
                field: 'paytime',
                title: '支付时间'
            },{
                field: 'orderamount',
                title: '订单金额'
            },{
                field: 'payedamount',
                title: '已支付金额'
            },
            {
                field: 'operate',
                title: '操作',
                align: 'center',
                valign: 'middle',
                clickToSelect: false,
                //formatter: operateFormatter,
                events: operateEvents
            }
        ]
    });
};

