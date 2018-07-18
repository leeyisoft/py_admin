
//建立WebSocket通讯
// var heartCheck.ws

//心跳检测
var heartCheck = {
    timeout: 120000 //120秒
    , timeoutObj: null
    , serverTimeoutObj: null
    , onmessage: null // 接受消息处理的函数
    , ws: null //websocket实例
    , lockReconnect: false //避免重复连接
    , _reconnect: function(ws_host) {
        var self = this
        console.log('hc _reconnect')
        if(this.lockReconnect) {
            return
        }
        this.lockReconnect = true

        // 没连接上会一直重连，设置延迟避免请求过多
        setTimeout(function () {
            self.init(ws_host, self.onmessage)
            self.lockReconnect = false
        }, 2000)
    }

    , _reset: function(){
        console.log('hc _reset')
        clearTimeout(this.timeoutObj)
        clearTimeout(this.serverTimeoutObj)
        return this
    }

    , start: function(){
        console.log('hc start')
        var self = this
        this.timeoutObj = setTimeout(function(){
            //这里发送一个心跳，后端收到后，返回一个心跳消息，
            //onmessage拿到返回的心跳就说明连接正常
            // self.ws.send("HeartBeat")
            // 如果超过一定时间还没重置，说明后端主动断开了
            self.serverTimeoutObj = setTimeout(function(){
                // 如果onclose会执行 _reconnect ，我们执行ws.close()就行了.
                // 如果直接执行 _reconnect 会触发onclose导致重连两次
                self.ws.close()
            }, self.timeout)
        }, this.timeout)
    }

    , init: function(ws_host, onmessage){
        var self = this
        this.onmessage = onmessage
        try {
            console.log('hc init')
            this.ws = new WebSocket(ws_host)

            this.ws.onclose = function () {
                self._reconnect(ws_host)
            }

            this.ws.onerror = function () {
                self._reconnect(ws_host)
            }
            this.ws.onopen = function () {
                // 心跳检测重置
                self._reset().start()
            }
            this.ws.onmessage = function (event) {
                console.log('hc ws onmessage')
                // 如果获取到消息，心跳检测重置
                // 拿到任何消息都说明当前连接是正常的
                self._reset().start()
                console.log('hc ws onmessage2')
                // 调用指定的消息处理函数
                self.onmessage(event)
            }
        } catch (e) {
           self._reconnect(url)
        }
    }
}

var layim

layui.use(['layim', 'laytpl'], function(){
    var laytpl = layui.laytpl;
    layim = layui.layim;
    //基础配置
    layim.config({

        //初始化接口
        init: {
            url: user_list_url
            ,data: {}
        }
        , title: im_name
         //我的信息
        , mine: {
            username: curr_uname //我的昵称
            ,id: curr_uuid //我的ID
            ,status: "online" //在线状态 online：在线、hide：隐身
            ,sign: curr_sign //我的签名
            ,avatar: curr_avatar //我的头像
        }
        //查看群员接口
        ,members: {
            url: member_list_url
            ,data: {}
        }

        ,uploadImage: {
            url: upload_img_url//（返回的数据格式见下文）
          ,type: '' //默认post
        }
        ,uploadFile: {
          url: upload_file_url //（返回的数据格式见下文）
          ,type: '' //默认post
        }

        // ,isAudio: true //开启聊天工具栏音频
        // ,isVideo: true //开启聊天工具栏视频

        //扩展工具栏
        ,tool: [{
          alias: 'code'
          ,title: '代码'
          ,icon: '&#xe64e;'
        }]

        // ,brief: false //是否简约模式（若开启则不显示主面板）

        //,title: 'WebIM' //自定义主面板最小化时的标题
        //,right: '100px' //主面板相对浏览器右侧距离
        //,minRight: '90px' //聊天面板最小化时相对浏览器右侧距离
        ,initSkin: '1.jpg' //1-5 设置初始背景
        //,skin: ['aaa.jpg'] //新增皮肤
        //,isfriend: false //是否开启好友
        //,isgroup: false //是否开启群组
        //,min: true //是否始终最小化主面板，默认false
        ,notice: true //是否开启桌面消息提醒，默认false
        ,voice: false //声音提醒，默认开启，声音文件为：default.mp3

        ,msgbox: msg_box_url//消息盒子页面地址，若不开启，剔除该项即可
        ,msg_url: msg_url //
        ,find: find_url //发现页面地址，若不开启，剔除该项即可
        ,chatLog: chatlog_url //聊天记录页面地址，若不开启，剔除该项即可
        ,copyright: 'Leeyi'
    })

    //外部自定义我的事件
    im_events = {
        //进入好友的空间
        enterZone: function (othis, e) {
            var friend_id = othis.parent().attr('data-id')
            layer.alert('<a href="/userzone/friend_id/' + friend_id + '"  target="_blank">点击，进入他的空间</a>', {
                title: false
                , icon: 6
                , btn: ''
            })
        }

        //将用户加入黑名单
        , joinBlack: function(othis, e){
            var friend_id = othis.parent().attr('data-id')
            //询问框
            layer.confirm('确定要将他加入黑名单？', {
                btn: ['是的', '算了'],
                title: '友情提示',
                icon: 3,
                closeBtn: 0
            }, function(){
                $.getJSON("/index/Tools/joinBlack/fid/" + friend_id, function(res){
                    if(1 == res.code){
                        layer.msg(res.msg, {time:1500})
                        layim.removeList({
                            type: 'friend'
                            ,id: res.data.to_id
                        })

                        //通知被加入黑名单的用户，删除我
                        var black_data = '{"type":"black","to_id":"' + res.data.to_id + '", "del_id":"' + res.data.del_id + '"}';
                        heartCheck.ws.send(black_data)
                    }else{
                        layer.msg(res.msg, {time:1500})
                    }
                })
            }, function(){

            })
        }

        //改变用户的群组
        , changeGroup: function(othis, e){
            //改变群组模板
            var elemAddTpl = ['<div class="layim-add-box">'
                , '<div class="layim-add-img"><img class="layui-circle" src="{{ d.data.avatar }}"><p>' +
                '{{ d.data.name||"" }}</p></div>'
                , '<div class="layim-add-remark">'
                , '{{# if(d.data.type === "friend" && d.type === "setGroup"){ }}'
                , '<p>选择分组</p>'
                , '{{# } if(d.data.type === "friend"){ }}'
                , '<select class="layui-select" id="LAY_layimGroup">'
                , '{{# layui.each(d.data.group, function(index, item){ }}'
                , '<option value="{{ item.id }}">{{ item.groupname }}</option>'
                , '{{# }) }}'
                , '</select>'
                , '{{# } }}'
                , '{{# if(d.data.type === "group"){ }}'
                , '<p>请输入验证信息</p>'
                , '{{# } if(d.type !== "setGroup"){ }}'
                , '<textarea id="LAY_layimRemark" placeholder="验证信息" class="layui-textarea"></textarea>'
                , '{{# } }}'
                , '</div>'
                , '</div>'].join('')

            var friend_id = othis.parent().attr('data-id')
            $.getJSON('/index/Tools/getNowUser/fid/' + friend_id, function(res){
                if(1 == res.code){
                    var index = layer.open({
                        type: 1,
                        skin: 'layui-layer-rim', //加上边框
                        area: ['430px', '260px'], //宽高
                        btn:   ['确认', '取消'],
                        title: '移动分组',
                        content: laytpl(elemAddTpl).render({
                            data: {
                                name: res.data.user_name
                                , avatar: res.data.avatar
                                , group: parent.layui.layim.cache().friend
                                , type: 'friend'
                            }
                            , type: 'setGroup'
                        })
                        , yes: function (index, layero) {
                            var groupElem = layero.find('#LAY_layimGroup')
                            var group_id = groupElem.val() //群组id
                            $.post('/index/Tools/changeGroup', {'group_id' : group_id, 'user_id' : res.data.id},
                                function(data) {
                                    if (1 == data.code) {
                                        layer.msg(data.msg, {time: 1500})
                                        //先从旧组移除，然后加入新组
                                        layim.removeList({
                                            type: 'friend'
                                            ,id: res.data.id
                                        })
                                        //加入新组
                                        layim.addList({
                                            type: 'friend'
                                            ,avatar: res.data.avatar
                                            ,username: res.data.user_name
                                            ,groupid: group_id
                                            ,id: res.data.id
                                            ,sign: res.data.sign
                                        })
                                        layer.close(index)
                                    } else {
                                        layer.msg(data.msg, {time: 2000})
                                    }
                            }, 'json')
                        }
                    })
                }else{
                    layer.msg(res.msg, {time: 2000})
                }
            })
        }

        // 申请好友
        , applyFriend: function(){
            var that = this
            //实际使用时数据由动态获得
            layim.add({
                type: 'friend'
                ,username: $(that).attr('username')
                ,avatar: $(that).attr('avatar')
                ,submit: function(group_id, remark, index){
                    layer.msg('好友申请已发送，请等待对方确认', {
                        icon: 1
                        ,shade: 0.5
                    }, function(){
                        layer.close(index)
                    })

                    //通知对方
                    $.post(
                        '/friend/apply',
                        {
                            to_user_id: $(that).attr('user_id'),
                            group_id: group_id,
                            remark: remark,
                            _xsrf: get_xsrf(),
                        },
                        function(res){
                            if(res.code != 0){
                                return layer.msg(res.msg)
                            }
                            layer.msg('好友申请已发送，请等待对方确认', {
                                icon: 1
                                ,shade: 0.5
                            }, function(){
                                layer.close(index)
                            })
                        }
                    )
                }
            })
        }
        // 添加好友
        , addFriend: function(action){
            var that = this
            var friend_id = $(that).parent().attr('friend_id')
            var _doAddFriend = function(friend_id, action, group_id, callback) {
                $.ajax({
                    type: "POST",
                    url: '/friend/add',
                    data: {
                        friend_id: friend_id,
                        action: action,
                        group_id: group_id,
                        '_xsrf':get_xsrf()
                    },
                    success: function(res) {
                        if(res.code != 0){
                            return layer.msg(res.msg)
                        }
                        // console.log('_doAddFriend callback', res)
                        callback && callback(res)
                    },
                    error: function(xhr){
                        if (xhr.responseJSON && xhr.responseJSON.msg) {
                            layer.msg(xhr.responseJSON.msg)
                        } else {
                            layer.msg("{{ _('未知错误') }}")
                        }
                    }
                })
            }
            // console.log('action', action)
            // console.log('that', $(that).parent().attr('friend_id'))
            if (action=='agree') {
                var li = that.parents('li')
                var uid = li.data('uid')
                var username = li.data('username')
                var sign = li.data('sign')
                var avatar = $(li).children().children('img').attr('src')
                //选择分组
                parent.layui.layim.setFriendGroup({
                    type: 'friend'
                    ,username: username
                    ,avatar: avatar
                    ,group: layim.cache().friend //获取好友分组数据
                    ,submit: function(group, index){
                        _doAddFriend(friend_id, action, group, function(res) {
                            // console.log('submit')
                            //将好友追加到主面板
                            parent.layui.layim.addList({
                                type: 'friend'
                                ,avatar: avatar //好友头像
                                ,username: username //好友昵称
                                ,groupid: group //所在的分组id
                                ,id: uid //好友ID
                                ,sign: sign //好友签名
                            })
                            parent.layer.close(index)
                            that.parent().html('已同意')
                        })
                    }
                })
            } else {
                layer.confirm('确定拒绝吗？', function (index) {
                    _doAddFriend(friend_id, action, '0', function(res) {
                        if(res.code != 0){
                            return layer.msg(res.msg)
                        }
                        layer.close(index)
                        that.parent().html('<em>已拒绝</em>')
                    })
                })
            }
        }
        //删除好友
        , removeFriend: function(othis, e){
            var friend_id = othis.parent().attr('data-id')
            //询问框
            layer.confirm('确定删除该好友？', {
                btn: ['确定', '取消'],
                title: '友情提示',
                closeBtn: 0,
                icon: 3
            }, function(){
                $.post('/index/Tools/removeFriend', {'user_id' : friend_id}, function(res){
                    if(1 == res.code){
                        layer.msg(res.msg, {time: 1500})
                        layim.removeList({
                            type: 'friend'
                            , id: res.data.to_id
                        })
                        //通知被删除的用户，删除我
                        var black_data = '{"type":"delFriend","to_id":"' + res.data.to_id + '", "del_id":"' + res.data.del_id + '"}';
                        heartCheck.ws.send(black_data)
                    }else{
                        layer.msg(res.msg, {time: 1500})
                    }
                }, 'json')
            }, function(){

            })
        }
        , readMsg: function(ids) {
            // console.log('readmsg othis: ', othis)
            console.log('readmsg ids: ', ids)
            // $.post('/chat/msg/', {action:'set_allread'}, function (res) {
            // });
        }
        //举报好友
        , reportFriend: function(othis, e){
            var friend_id = othis.parent().attr('data-id')

            layer.open({
                type: 2,
                title: '举报好友',
                shadeClose: true,
                skin: 'layui-layer-molv', //加上边框
                shade: 0.3,
                area: ['400px', '400px'],
                content: '/index/Tools/reportFriend/user_id/' + friend_id
            })
        }

        //退出群组
        , leaveOut: function(othis, e){
            var group_id = othis.parent().attr('data-id')
            var index = layer.confirm('确定退出该群组？', {
                btn: ['确定', '取消'],
                title: '友情提示',
                closeBtn: 0,
                icon: 3
            }, function(){
                $.post('/index/Tools/leaveGroup', {'group_id' : group_id}, function(res){
                    if(1 == res.code){
                        layer.msg(res.msg, {time: 1500})
                        layim.removeList({
                            type: 'group'
                            , id: res.data.group_id
                        })

                        // 退出讨论组
                        var leave_data = '{"type": "leaveGroup", "leave_id":"' + res.data.uid + '", "group_id":"' + res.data.group_id + '"}';
                        heartCheck.ws.send(leave_data)
                    }else{
                        layer.msg(res.msg, {time: 1500})
                    }
                    layer.close(index)
                }, 'json')
            }, function(){

            })
        }
    }

    heartCheck.init(
        ws_host,
        //监听收到的消息
        function(message){
            var data = JSON.parse(message.data)
            // console.log('onmessage data: ', data)
            var message = {
                token: token,
            }
            // console.log('data type: ', data['type'])
            switch(data['type']){
                // 服务端ping客户端
                case 'ping':
                    message.type = "pong"
                    heartCheck.ws.send(JSON.stringify(message))
                    break
                // 用户在线状态： online offline hide
                case 'online':
                    layim.setFriendStatus(data.uid, data.status)
                    break
                // 检测聊天数据
                case 'dialog':
                    // console.log('case dialog data.to: ', data.to)
                    if (data.to.id!=curr_uuid) {
                        layim.getMessage(data.to)
                    }
                    break
                // 离线消息推送
                case 'logMessage':
                    // setTimeout(function(){layim.getMessage(data.data)}, 3000)
                    break
                // 用户退出 更新用户列表
                case 'logout':
                    layim.setFriendStatus(data.id, 'offline')
                    break
                // 添加好友
                case 'addFriend':
                    console.log(data.data)
                    layim.addList(data.data)
                    break
                //加入黑名单
                case 'black':
                    console.log(data.data)
                    layim.removeList({
                        type: 'friend'
                        , id: data.data.id //好友或者群组ID
                    })
                    break
                //删除好友
                case 'delFriend':
                    console.log(data.data)
                    layim.removeList({
                        type: 'friend'
                        , id: data.data.id //好友或者群组ID
                    })
                    break
                // 添加 分组信息
                case 'addGroup':
                    console.log(data.data)
                    layim.addList(data.data)
                    break
                // 申请加入群组
                case 'applyGroup':
                    console.log(data.data)
                    //询问框
                    var index = layer.confirm(
                        data.data.joinname + ' 申请加入 ' + data.data.groupname + "<br/> 附加信息： " + data.data.remark , {
                        btn: ['同意', '拒绝'], //按钮
                        title: '加群申请',
                        closeBtn: 0,
                        icon: 3
                    }, function(){
                        $.post(join_group_url,
                            {
                                'user_id': data.data.joinid,
                                'user_name': data.data.joinname,
                                'user_avatar': data.data.joinavatar,
                                'user_sign': data.data.joinsign,
                                'group_id': data.data.groupid
                            },
                            function(res){
                                if(0 == res.code){

                                    var join_data = '{"type":"joinGroup", "join_id":"' + data.data.joinid + '"' +
                                        ', "group_id": "' + data.data.groupid + '", "group_avatar": "' + data.data.groupavatar + '"' +
                                        ', "group_name": "' + data.data.groupname + '"}';
                                    heartCheck.ws.send(join_data)
                                }else{
                                    layer.msg(res.msg, {time:2000})
                                }
                        }, 'json')
                        layer.close(index)
                    }, function(){

                    })
                    break
                // 删除面板的群组
                case 'delGroup':
                    console.log(data.data)
                    layim.removeList({
                        type: 'group'
                        ,id: data.data.id //群组ID
                    })
                    break
            }
        }
    )

    //监听签名修改
    layim.on('sign', function(value){
        $.post(change_sign_url, {'sign' : value}, function(res){
            if(1 == res.code){
                layer.msg(res.msg, {time:1500})
            }else{
                layer.msg(res.msg, {time:1500})
            }
        }, 'json')
    })

    //监听自定义工具栏点击录音
    layim.on('tool(voice)', function(insert, send){

        layui.use(['layer'], function(){
            var layer = layui.layer;

            var box = layer.open({
                type: 1,
                title: '发送语音',
                maxmin: false, //开启最大化最小化按钮
                skin: 'layui-layer-molv',
                anim: 3,
                area: ['200px', '250px'],
                content: $("#audio_box"),
                cancel: function(index){
                    $("#tips").text('')
                    $("#a_pic").attr('src', '/static/common/images/audio.png')
                    layer.close(index)
                    return false;
                }
            })

            //点击开始录音
            $("#say").bind('click', function(){
                $("#tips").text('说话中......')
                $("#a_pic").attr('src', '/static/common/images/audio.gif')
                $("#over—say").removeClass('layui-btn-disabled')
                $(this).addClass('layui-btn-disabled')
            })
            var isSend = false;
            //结束录音
            $("#over—say").bind('click', function(){
                if(!isSend){
                    $("#tips").text('')
                    $("#a_pic").attr('src', '/static/common/images/audio.png')
                    $("#say").removeClass('layui-btn-disabled')
                    $(this).addClass('layui-btn-disabled')
                    layer.close(box)

                    var index = layer.load(1, {
                        shade: [0.1,'#fff'] //0.1透明度的白色背景
                    })
                    setTimeout(function(){
                        var audioSrc = $("#audio_src").val()
                        if('' == audioSrc){
                            layer.msg('您没有发送语音', {time:1000})
                        }else{
                            insert('audio[' + audioSrc + ']')
                            send() //自动发送
                        }
                        layer.close(index)
                    }, 1500)
                    isSend = true;
                }
            })
        })

    })

    //layim建立就绪
    layim.on('ready', function(res){
        //模拟消息盒子有新消息，实际使用时，一般是动态获得
        // layim.msgbox(1)
        //点击头像操作
        $(".layui-layim-user").click(function(){
            layui.use(['layer'], function(){
                var layer = layui.layer;
                layer.open({
                    type: 2,
                    title: '修改个人资料',
                    maxmin: false, //开启最大化最小化按钮
                    area: ['800px', '600px'],
                    content: chat_user_url
                })
            })
        })
        //发送消息
        layim.on('sendMessage', function(res){
            console.log('sendMessage res', res)
            // 发送消息
            // var mine = JSON.stringify(res.mine)
            // var to = JSON.stringify(res.to)
            var message = {
                token: token,
                'type': 'dialog',
                'mine': res.mine,
                'to': res.to,
            }

            if(res.to.type === 'friend'){
                layim.setChatStatus('<span style="color:#FF5722;">对方正在输入。。。</span>')
            }
            var json = JSON.stringify(message)
            console.log('sendMessage json: ', json)
            heartCheck.ws.send(json)
        })

        //在线状态切换
        layim.on('online', function(status){
            var message = {
                token: token,
                'type': 'online',
                'status': status,
                'uid': curr_uuid,
            }
            // console.log('online status ', status)
            heartCheck.ws.send(JSON.stringify(message))
        })
    })

    if (get_noread_url) {
        //获取未读的消息 40s读取一次
        setInterval(function(){
            $.getJSON(get_noread_url, function(res){
                if(res.data > 0){
                    layim.msgbox(res.data)
                }
            })
        }, parseInt(40) * 1000)
    }
    $('.layim-btn').on('click', function(){
        var type = $(this).data('type')
        im_events[type] ? im_events[type].call(this) : '';
    })
})
