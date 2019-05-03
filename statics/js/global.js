
// 常量
var status_html = {
    '1':'<div class="layui-table-cell laytable-cell-1-status"><input type="checkbox" name="status" value="1" lay-skin="switch" lay-text="启用|禁用" lay-filter="status" checked=""><div class="layui-unselect layui-form-switch layui-form-onswitch" lay-skin="_switch"><em>启用</em><i></i></div> </div>',
    '0':'<div class="layui-table-cell laytable-cell-1-status"><input type="checkbox" name="status" value="1" lay-skin="switch" lay-text="启用|禁用" lay-filter="status" checked=""><div class="layui-unselect layui-form-switch" lay-skin="_switch"><em>禁用</em><i></i></div></div>',
}

var $ = function() {}
var get_xsrf = function() {}
// 修改模式下表单自动赋值
var set_form_data = function(){}

layui.define(['element', 'form', 'jquery', 'layer'], function(exports) {
    var form = layui.form
    $ = layui.jquery
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

    get_xsrf = function() {
        return $("input[name='_xsrf']").val()
    }
    set_form_data = function(formData) {
        // console.log('formData', formData)
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

    $(document).ready(function(){
        $('#show_search_box').on('click', function() {
            $('#search_box').slideToggle("slow")
        })
    })
})

function default_error_callback(xhr, res) {
    console.log('xhr ', xhr, 'res ', res)
    if (res && res.msg) {
        layui.layer.msg(res.msg, {icon:2})
    } else if (xhr && xhr.responseJSON && xhr.responseJSON.msg) {
        layui.layer.msg(xhr.responseJSON.msg, {icon:2})
    } else {
        layui.layer.msg('未知错误.', {icon:2})
    }
}
/**
 * [api_ajax description]
 * @param  {[type]}   url            [description]
 * @param  {[type]}   method         get post put delete
 * @param  {[type]}   params         [description]
 * @param  {Function} callback       [description]
 * @param  {[type]}   error_callback [description]
 * @param  {Boolean}  async          async. 默认是true，即为异步方式
 * @return {[type]}                  [description]
 */
function api_ajax(url, method, params, callback, error_callback, async) {
    if (!url) {
        return false
    }
    if (!method) {
        method = 'get'
    }
    if (!params) {
        params = {}
    }

    params._xsrf = get_xsrf()

    async = async===false ? false : true
    $.ajax({
        type: method,
        url: url,
        async: async,
        data: params,
        dataType: 'json',
        success: function(res) {
            // console.log(res)
            if (res.code==0) {
                if (callback) {
                    callback(res)
                }
            } else if(res.code=='990013') {
                current_token('clear')
                location.href = '/passport/login'
            } else {
                if (error_callback) {
                    error_callback(false, res)
                }
            }
        },
        error: function(xhr){
            if (error_callback) {
                error_callback(xhr, false)
            }
        }
    })
}
