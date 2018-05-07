
// 常量
var status_html = {
    '1':'<div class="layui-table-cell laytable-cell-1-status"><input type="checkbox" name="status" value="1" lay-skin="switch" lay-text="启用|禁用" lay-filter="status" checked=""><div class="layui-unselect layui-form-switch layui-form-onswitch" lay-skin="_switch"><em>启用</em><i></i></div> </div>',
    '0':'<div class="layui-table-cell laytable-cell-1-status"><input type="checkbox" name="status" value="1" lay-skin="switch" lay-text="启用|禁用" lay-filter="status" checked=""><div class="layui-unselect layui-form-switch" lay-skin="_switch"><em>禁用</em><i></i></div></div>',
}

function get_xsrf() {
    return $("input[name='_xsrf']").val()
}

// 修改模式下表单自动赋值
var set_form_data = function(formData) {
    var input = ''
    if (formData) {
        for (var i in formData) {
            switch($('.field-'+i).attr('type')) {
                case 'select':
                    input = $('.field-'+i).find('option[value="'+formData[i]+'"]');
                    input.prop("selected", true);
                    break;
                case 'radio':
                    input = $('.field-'+i+'[value="'+formData[i]+'"]');
                    input.prop('checked', true);
                    break;
                case 'checkbox':
                    for(var j in formData[i]) {
                        input = $('.field-'+i+'[value="'+formData[i][j]+'"]');
                        input.prop('checked', true);
                    }
                    break;
                case 'img':
                    input = $('.field-'+i);
                    input.attr('src', formData[i]);
                default:
                    input = $('.field-'+i);
                    input.val(formData[i]);
                    break;
            }
            if (input.attr('data-disabled')) {
                input.prop('disabled', true);
            }
            if (input.attr('data-readonly')) {
                input.prop('readonly', true);
            }
        }
    }
}

layui.define(['element', 'form', 'jquery', 'layer'], function(exports) {
    var form = layui.form
    var $ = layui.jquery
    var element = layui.element
    var layer = layui.layer
    /* 全选 */
    form.on('checkbox(allChoose)', function(data) {
        var child = $(data.elem).parents('table').find('tbody input.checkbox-ids');
        child.each(function(index, item) {
            item.checked = data.elem.checked;
        });
        form.render('checkbox');
    })

    /*iframe弹窗*/
    $('.j-iframe-pop').click(function(){
        var that = $(this),
            _url = that.attr('href'),
            _title = that.attr('title'),
            _width = that.attr('width') ? that.attr('width') : 750,
            _height = that.attr('height') ? that.attr('height') : 500
        if (!_url) {
            layer.msg('请设置href参数')
            return false
        }
        layer.open({type:2, title:_title, content:_url, area: [_width+'px', _height+'px']})
        return false
    })
})