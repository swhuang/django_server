/**
 * Created by shengweihuang on 2017/11/12.
 */

$(function () {
    /*$('[data-pjax] a, a[data-pjax]').click(function () {
        alert($(this).attr('href'));
        $.pjax({
            url: $(this).attr('href'),
            container: '#pjax-container',
            maxCacheLength: 0,
            cache: false,
            fragment: "#pjax-container",
            timeout: 8000
        })
    });*/
    $(document).pjax('[data-pjax] a, a[data-pjax]', '#pjax-container');
});
//$(document).pjax('[data-pjax] a, a[data-pjax]', '#pjax-container');