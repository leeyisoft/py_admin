<fieldset class="layui-elem-field layui-field-title">
    <legend>{{ d.legend }}</legend>
</fieldset>
<div class="layui-row ">
    {{# if(d.type == 'friend'){ }}
        {{#  layui.each(d.data, function(index, item){ }}
        <div class="layui-col-xs3 layui-find-list">
            <li layim-event="add" data-type="friend" data-index="0" data-uid="{{ item.id }}" data-name="{{item.username}}">
                <img src="{{item.avatar}}" onerror="javascript:this.src=default_avatar" >
                <span>{{item.username}}</span>
                <p>{{item.sign}}  {{#  if(item.sign == ''){ }}我很懒，懒得写签名{{#  } }} </p>
                <button class="layui-btn layui-btn-xs btncolor add" data-type="friend" username="{{item.username}}" avatar="{{item.avatar}}" user_id="{{item.id}}">
                    <i class="layui-icon">&#xe654;</i>加好友
                </button>
            </li>
        </div>
        {{#  }) }}
    {{# }else{ }}
        {{#  layui.each(d.data, function(index, item){ }}
        <div class="layui-col-xs3 layui-find-list">
            <li layim-event="add" data-type="group" data-approval="{{ item.approval }}" data-index="0" data-uid="{{ item.groupIdx }}" data-name="{{item.groupName}}">
                <img src="{{item.avatar}}" onerror="javascript:this.src=default_avatar" >
                <span>{{item.groupName}}</span>
                <p>{{item.des}}  {{#  if(item.des == ''){ }}无{{#  } }} </p>
                <button class="layui-btn layui-btn-xs btncolor add" data-type="group"><i class="layui-icon">&#xe654;</i>加群</button>
            </li>
        </div>
        {{#  }) }}
    {{# } }}
</div>