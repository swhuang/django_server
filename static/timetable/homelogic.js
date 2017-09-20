/**
 * Created by shengweihuang on 2017/7/12.
 */

function fileSelected() {
  var file = document.getElementById('inputfile').files[0];
  if (file)
  {
    var fileSize = 0;
    if (file.size > 1024 * 1024)
      fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
    else
      fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';
/*
    document.getElementById('fileName').innerHTML = 'Name: ' + file.name;
    document.getElementById('fileSize').innerHTML = 'Size: ' + fileSize;
    document.getElementById('fileType').innerHTML = 'Type: ' + file.type;
    */
  }
}

function uploadFile() {
    var a = "" || null || 3 || 4;//3
    alert(a)
    if($("#name").val() == "")
    {
        alert("请输入学校名字和排课代码");
        $("#name").focus();
        return 0;
    }
    if($("#inputfile").val() == "")
    {
        alert("请上传文件");
        return 0
    }
  var xhr = new XMLHttpRequest();
    //var fd = new FormData(document.getElementById('main'));//var fd = new FormData($("#inputfile"));
    var form_data = new FormData()
    var file_info = $("#inputfile")[0].files[0];
    var teacher_file = $("#inputfile2")[0].files[0];
    var timetable_file = $("#inputfile3")[0].files[0];
    form_data.append('file',file_info);
    form_data.append('file2',teacher_file);
    form_data.append('file3',timetable_file);
    form_data.append('name',$("#name").val());
  /* event listners */
  xhr.upload.addEventListener("progress", uploadProgress, false);
  xhr.addEventListener("load", uploadComplete, false);
  xhr.addEventListener("error", uploadFailed, false);
  xhr.addEventListener("abort", uploadCanceled, false);
  /* Be sure to change the url below to the url of your upload server side script */
  console.log($("#progressdiv").text());
  $("#progressdiv").toggle();
  //$(".progress .progress-striped .active").toggle();alert("nono");
  xhr.open("POST", "TimeTable");
  xhr.send(form_data);
}

function uploadProgress(evt) {
  if (evt.lengthComputable) {
      console.log(evt.loaded.toString()+":"+evt.total.toString())
    var percentComplete = Math.round(evt.loaded * 100 / evt.total);
    document.getElementById('progressbar').setAttribute("style","width:"+percentComplete.toString() + '%')//.innerHTML = percentComplete.toString() + '%';
  }
  else {
    //document.getElementById('progressNumber').innerHTML = 'unable to compute';
    $(".alert.alert-danger").css("display","block");
  }
}

function uploadComplete(evt) {
  /* This event is raised when the server send back a response */
  //alert(evt.target.responseText);
    setTimeout("$('.alert.alert-success').toggle()", 1000);

    setTimeout("FinishedUpload()",1500);
    console.log($(".alert.alert-success"))
}

function uploadFailed(evt) {
  alert("There was an error attempting to upload the file.");
}

function uploadCanceled(evt) {
  alert("The upload has been canceled by the user or the browser dropped the connection.");
}

function FinishedUpload() {
    $('.close').alert('close');
    $(".operate").empty();
    var html = "<div class='row'><div class='col-md-2'>";
    var mstr = "<button type='button' class='btn btn-default' onclick='tableSortrequest();'>开始排课</button>";
    html += mstr;
    html += "</div><div class='col-md-10'>";
    html += "<div class='alert alert-info' id='ProcessInfo' style='padding: 5px;height: 35px'></div>";
    html += "</div></div>";

    $(".operate").append(html);
}

function tableSortrequest() {
    if($("#name").val() == "")
    {
        alert("请输入学校名字和排课代码");
        $("#name").focus();
        return 0;
    }
    $.ajax({
        url:"SortTable?name="+$("#name").val(),
        type:"GET",
        success:function (result) {
            //alert('finished');
            $("#ProcessInfo").text("排课完成！");
        },
        beforeSend:function (xhr) {
            //alert("pending request")
            $("#ProcessInfo").text("正在排课。。。")
        }
    })
    //$.get("SortTable?name="+$("#name").val());
}