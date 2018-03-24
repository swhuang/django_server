/**
 * Created by shengweihuang on 2017/11/12.
 */

$(function () {
    $(document).pjax('[data-pjax] a, a[data-pjax]', '#pjax-container');
});
function strip(value){
        return value.replace(/(^\s+|\s+$)/, '');
    }

function get_csrf(){
        return $('input[name=csrfmiddlewaretoken]').attr('value');
    }


function make_warning(obj, text) {
        $(obj).text(text);
        $(obj).show(100);
    }

function poptip(obj, text) {
        var _type = arguments[2]?arguments[2]:'alert';
        $(obj).popover('destroy');
        $(obj).popover({'content': text, 'container': 'body'});
        $(obj).popover('show');
    }