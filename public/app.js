var vm = new Vue({
    el:"#app",
    data:{
        loginStatus: false,
        cookieStatus: false,
        cid:"",
        type: 0,
        qrStatus: false,
        qrCodeUrl:"",
        okl_token:"", 
        cookies:"", 
        token:"",
        imgPath:"",
        timer: "",//定时器
        msg: "",
        explain:"",//使用说明
        logs:"",

    },
    created:function(){
        //获取公告
        axios.get("/explain").then(function(res){
            vm.explain = res.data.data
        })
        if(this.getCookie("cid")!=null&&this.getCookie("cid")!=""){
            this.cid= this.getCookie("cid")
            this.loginStatus= true
            this.cookieStatus= true
            this.checkCookie()
            //获取日志
            axios.post("/log",{
                cid:this.cid
            }).then(function(res){
                vm.logs = res.data.data
            })
        }else{
            this.loginStatus= false
            this.cookieStatus= false
        }

    },
    methods:{
        //请求二维码
        getQrCode(){
            axios.get("/qrcode").then(function(res){
                vm.qrCodeUrl = res.data.qrCodeUrl
                vm.okl_token = res.data.okl_token
                vm.cookies = res.data.cookies
                vm.token = res.data.token

                vm.imgPath = "/qr.png"
                vm.qrStatus = true
                if(vm.type == 0){
                    vm.check()
                }else{
                    vm.del()
                }

            })
        },
        //获取登录状态
        check(){
            //设置定时器
            this.timer = setInterval(this.checkReq, 1000);
        },
        checkReq(){
            axios.post("/check",{
                okl_token : this.okl_token,
                cookies : this.cookies,
                token : this.token
            }).then(function(res){
                if(res.data.code == 0){
                    clearInterval(vm.timer)
                    var inst = new mdui.Dialog('#dialog');
                    vm.msg = res.data.data
                    inst.open()
                    vm.loginStatus= true
                    vm.cookieStatus= true
                    vm.cid= vm.getCookie("cid")
                    //获取日志
                    axios.post("/log",{
                        cid:vm.cid
                    }).then(function(res){
                        vm.logs = res.data.data
                    })
                }else{
                    
                }
            })
        },
        //删除账号定时器
        del(){
            var instD = new mdui.Dialog('#delete');
            instD.open()
        },
        checkDel(){
            axios.post("/delete",{
                cid : this.cid,
            }).then(function(res){
                console.log(vm.cid)
                var inst = new mdui.Dialog('#dialog');
                vm.msg = res.data.data
                inst.open()
                if(res.data.code==0){
                    vm.clearCookie()
                }
            })
        },
        //状态转换
        typeChage(){
            if(this.type == 0){
                this.type = 1
                this.icon = "add"
            }else{
                this.type = 0
                this.icon = "delete"
            }
            this.qrStatus = false
            clearInterval(vm.timer)
        },
        //获取cookie
        getCookie: function (cname) {
            var name = cname + "=";
            var ca = document.cookie.split(';');
            for (var i = 0; i < ca.length; i++) {
             var c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1);
            if (c.indexOf(name) != -1){
             return c.substring(name.length, c.length);
             }
            }
            return "";
        },
        //设置cookie
        setCookie: function (cname, cvalue, exdays) {
            var d = new Date();
            d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
            var expires = "expires=" + d.toUTCString();
            document.cookie = cname + "=" + cvalue + "; " + expires;
         },
        //清除cookie
        clearCookie: function () {
            this.setCookie("cid", "", -1)
            //改变状态
            this.loginStatus= false
            this.cookieStatus= false
        },
        //检测cookie状态
        checkCookie(){
            axios.post("/checkcookie",{
                cid : this.cid,
            }).then(function(res){
                if(res.data.status==0){
                    vm.cookieStatus=true
                    return true
                }else{
                    vm.cookieStatus=false
                    return false
                }
            })
        }

    }
})