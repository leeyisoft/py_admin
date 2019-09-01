{{# layui.each(d.data, function(index, item){
    if(item.msgtype == 'apply_friend' || item.msgtype == 'apply_group'){ }}
    <li data-id="{{ item.id }}" data-uid="{{ item.from_user.id }}" data-type="{{item.msgtype}}" data-username="{{ item.from_user.username }}" data-sign="{{ item.from_user.sign }}" data-avatar="{{ item.from_user.avatar }}">
        <a href="javascript:void(0)" target="_blank">
            <img src="{{item.from_user.avatar}}" class="layui-circle layim-msgbox-avatar" onerror="javascript:this.src=default_avatar">
        </a>
        <p class="layim-msgbox-user">
            <a href="javascript:void(0)" target="_blank">
                <b>{{ item.from_user.username||'' }}</b>
            </a>
            <span>{{ item.created_at }}</span>
        </p>
        <p class="layim-msgbox-content">
        {{# if(item.msgtype == 'apply_friend'){ }}
        申请添加你为好友
        {{# }else{ }}
        申请加入 {{ item.groupName||'' }} 群
        {{# } }}
        <span>{{ item.message ? '附言: '+item.message : '' }}</span>
         </p>
        <p class="layim-msgbox-btn" friend_id="{{ item.related_id }}">
            <button class="layui-btn layui-btn-small" data-type="agree">同意</button>
            <button class="layui-btn layui-btn-small layui-btn-primary" data-type="refuse">拒绝</button>
        </p>
    </li>

    {{# } else if(item.msgtype == 2) { }}
        {{# if(item.from == d.curr_user_id){ }}
            <li data-id="{{ item.id }}" class="layim-msgbox-system">
                <p><em>系统：</em><b>{{ item.username }}</b>
                {{# if(item.status == 2 || item.status == 4){ }}
                已同意你的好友申请 <button class="layui-btn layui-btn-xs btncolor chat" data-name="{{ item.username }}" data-chattype="friend" data-type="chat" data-uid="{{item.to}}">发起会话</button>
                {{# }else{ }}
                已拒绝你的好友申请
                {{# } }}
                <span>{{ item.readTime }}</span></p>
            </li>
        {{# }else{ }}
            <li data-id="{{ item.id }}" >
              <a href="javascript:void(0)" target="_blank">
                <img src="http://test.guoshanchina.com/uploads/person/{{ item.from }}.jpg" class="layui-circle layim-msgbox-avatar" onerror="javascript:this.src='../../../../../../uploads/person/empty2.jpg'">
              </a>
              <p class="layim-msgbox-user">
                <a href="javascript:void(0)" target="_blank"><b>{{ item.username||'' }}</b></a>
                <span>{{ item.sendTime }}</span>
              </p>
              <p class="layim-msgbox-content">
                申请添加你为好友
                <span>{{ item.remark ? '附言: '+item.remark : '' }}</span>
                {{# if(item.status == 2 || item.status == 4){ }}
                <button class="layui-btn layui-btn-xs btncolor chat" data-name="{{ item.username }}" data-chattype="friend" data-type="chat" data-uid="{{item.from}}">发起会话</button>
                {{# } }}

              </p>
              <p class="layim-msgbox-btn">
                {{# if(item.status == 2 || item.status == 4){ }}
                已同意
                {{# }else{ }}
                已拒绝
                {{# } }}
              </p>
            </li>
        {{# } }}

    {{# }else if(item.msgtype == 4){ }}
        {{# if(item.from == d.curr_user_id){ }}
            <li data-id="{{ item.id }}" class="layim-msgbox-system">
                <p><em>系统：</em> 管理员 {{ item.handle }}
                {{# if(item.status == 2 || item.status == 4){ }}
                已同意你加入群 <b>{{ item.groupName }}</b> <button class="layui-btn layui-btn-xs btncolor chat" data-name="{{ item.groupName }}" data-chattype="group" data-type="chat" data-uid="{{item.to}}">发起会话</button>
                {{# }else{ }}
                已拒绝你加入群 <b>{{ item.groupName }}</b>
                {{# } }}
                <span>{{ item.readTime }}</span></p>
            </li>
        {{# }else{ }}
            <li data-id="{{ item.id }}" class="layim-msgbox-system">
                <p>
                    <em>系统：</em>
                    管理员{{ item.handle }}
                    {{# if(item.status == 2 || item.status == 4){ }}
                    已同意 <b>{{ item.username }}</b> 加入群 <b>{{ item.groupName }}</b>
                    {{# }else{ }}
                    你已拒绝 <b>{{ item.username }}</b> 加入群 <b>{{ item.groupName }}</b>
                    {{# } }}
                    <span>{{ item.readTime }}</span>
                </p>
            </li>
        {{# } }}

    {{# }
}) }}