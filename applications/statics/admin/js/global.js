
// 常量
var status_html = {
    '1':'<div class="layui-table-cell laytable-cell-1-status"><input type="checkbox" name="status" value="1" lay-skin="switch" lay-text="启用|禁用" lay-filter="status" checked=""><div class="layui-unselect layui-form-switch layui-form-onswitch" lay-skin="_switch"><em>启用</em><i></i></div> </div>',
    '0':'<div class="layui-table-cell laytable-cell-1-status"><input type="checkbox" name="status" value="1" lay-skin="switch" lay-text="启用|禁用" lay-filter="status" checked=""><div class="layui-unselect layui-form-switch" lay-skin="_switch"><em>禁用</em><i></i></div></div>',
}

function getCookie(name) {
    var r = document.cookie.match("\\b"+name+"=([^:]*)\\b");
    return r ? r[1] : undefined;
}

layui.define(['element', 'form', 'jquery', 'layer'], function(exports) {
    var form = layui.form
    /* 全选 */
    form.on('checkbox(allChoose)', function(data) {
        var child = $(data.elem).parents('table').find('tbody input.checkbox-ids');
        child.each(function(index, item) {
            item.checked = data.elem.checked;
        });
        form.render('checkbox');
    })
})