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
