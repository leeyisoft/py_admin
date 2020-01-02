/*
*@Name: layuiUniversalCompany - 通用企业公司网站模板
*@Author: xuzhiwen
*@Copyright:layui.com
*/


layui.define(['jquery','element','util','laytpl','layer'],function(exports){

  var $ = layui.jquery
          ,element = layui.element
          ,layer = layui.layer
          ,util = layui.util
          ,laytpl = layui.laytpl;
          // var off = false;
  var gather = {
    json:function(url,data,func,options){
      var that = this, type = typeof data === 'function';
      if(type){
        options = func
        func =  data;
        data = {};
      }
      options = options || {};
      // console.log(off)
      // if(off){
        return $.ajax({
          type: options.type || 'get',
          dataType: options.dataType || 'json',
          data : data,
          url: url,
          success: function(res){
            func && func(res);
          },error:function(e){
            layer.msg('请求异常,请重试',{shift:6});
            options.error && options.error(e);
          }
        });
      // }
    },
  };
  exports('common',gather)
});

/**
 * Parse the time to string
 * @param {(Object|string|number)} time
 * @param {string} cFormat
 * @returns {string | null}
 */
function parseTime(time, cFormat, def) {
  if (arguments.length === 0) {
    return null
  }
  if (time == 0 && def) {
    return def
  } else if (time == 0) {
    return ''
  }
  const format = cFormat || '{y}-{m}-{d} {h}:{i}:{s}'
  let date
  if (typeof time === 'object') {
    date = time
  } else {
    if ((typeof time === 'string') && (/^[0-9]+$/.test(time))) {
      time = parseInt(time)
    }
    if ((typeof time === 'number') && (time.toString().length === 10)) {
      time = time * 1000
    }
    date = new Date(time)
  }
  const formatObj = {
    y: date.getFullYear(),
    m: date.getMonth() + 1,
    d: date.getDate(),
    h: date.getHours(),
    i: date.getMinutes(),
    s: date.getSeconds(),
    a: date.getDay()
  }
  const time_str = format.replace(/{([ymdhisa])+}/g, (result, key) => {
    const value = formatObj[key]
    // Note: getDay() returns 0 on Sunday
    if (key === 'a') { return ['日', '一', '二', '三', '四', '五', '六'][value ] }
    return value.toString().padStart(2, '0')
  })
  return time_str
}
